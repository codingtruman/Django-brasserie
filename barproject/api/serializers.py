from rest_framework import serializers
from .models import *


class BeerSerializer(serializers.ModelSerializer):
    availability = serializers.SerializerMethodField()

    def get_availability(self, obj):
        if Stock.objects.filter(reference=obj.id, stock__gt=0):
            return "available"
        return "outofstock"

    class Meta:
        model = Beer
        fields = ("pk", "ref", "name", "description", "availability")


class BarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bar
        fields = ("pk", "name")


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ("reference", "bar", "stock")


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ("reference", "count")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True)

    def validate(self, data):
        order_items = data["items"]
        if not order_items:
            raise serializers.ValidationError({"warning": "Empty order."})

        errors = []

        for order_item in order_items:
            try:
                available_stock = Stock.objects.get(
                    bar=data["bar"], reference=order_item["reference"]
                ).stock
            except Stock.DoesNotExist:
                available_stock = 0

            if order_item["count"] > available_stock:
                errors.append(
                    f"Reference {order_item['reference'].pk} is insufficient, only has {available_stock}."
                )

        if errors:
            raise serializers.ValidationError({"error": errors})

        return data

    def create(self, validated_data):
        order_items_data = validated_data.pop("items")
        # create 1 entry in Orders table
        order = Orders.objects.create(**validated_data)
        # create multiple entries in OrderItems table
        for order_item_data in order_items_data:
            OrderItems.objects.create(order=order, **order_item_data)

        return order

    class Meta:
        model = Orders
        fields = ("pk", "bar", "items")
