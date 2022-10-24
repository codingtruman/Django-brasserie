from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .models import *
from .serializers import *
from .permissions import *


class Index(TemplateView):
    def get_template_names(self):
        return ["index.html"]


class BeerList(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BeerSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = ("ref", "name")
    search_fields = ("$ref", "$name", "$description")

    def get_queryset(self):

        is_available = self.request.query_params.get("available")
        # check all available beers
        if is_available and is_available.lower() == "true":
            return Beer.objects.filter(stock__stock__gt=0).distinct()
        # check all unavailable beers
        elif is_available and is_available.lower() == "false":
            return Beer.objects.filter(stock__stock=0).distinct()

        # specify a bar counter to see all available refs in that bar
        bar_var = self.request.query_params.get("bar")
        if bar_var:
            return Beer.objects.filter(stock__bar=int(bar_var), stock__stock__gt=0).distinct()

        return Beer.objects.all()


class BarList(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ("pk", "name")


class StockList(viewsets.ModelViewSet):

    permission_classes = [AuthenticatedReadOnly]
    serializer_class = StockSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ("reference", "bar", "stock")

    def get_queryset(self):

        # get stocks based on beer reference id
        ref_var = self.request.query_params.get("reference")
        if ref_var:
            return Stock.objects.filter(reference=int(ref_var))
        # get stocks based on bar counter id
        bar_var = self.request.query_params.get("bar")
        if bar_var:
            return Stock.objects.filter(bar=int(bar_var))

        return Stock.objects.all()


class Statistics(viewsets.ModelViewSet):

    permission_classes = [AuthenticatedReadOnly]

    def list(self, request):

        miss_query = Stock.objects.filter(stock=0).values_list("bar").distinct()
        non_miss_query = Bar.objects.values_list("pk").exclude(pk__in=miss_query)
        
        return Response(
            {
                "all_stocks": {
                    "description": "Liste des comptoirs qui ont toutes les références en stock",
                    "bars": [bar[0] for bar in non_miss_query],
                },
                "miss_at_least_one": {
                    "description": "Liste des comptoirs qui ont au moins une référence épuisée",
                    "bars": [bar[0] for bar in miss_query],
                },
            }
        )


class OrderList(viewsets.ModelViewSet):

    permission_classes = [AnonCreateOrAdminRead]
    queryset = Orders.objects.all()
    serializer_class = OrderSerializer
