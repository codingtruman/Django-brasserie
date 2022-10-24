from datetime import datetime
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Stock, OrderItems

logger = logging.getLogger(__name__)

@receiver(post_save, sender=OrderItems)
def update_stock(sender, instance, created, **kwargs):

    if created:
        stock_instance = Stock.objects.get(reference=instance.reference, bar=instance.order.bar)
        stock_instance.stock -= instance.count
        stock_instance.save()

    if stock_instance.stock < 2:
        logger.warning(f"stock of {stock_instance.reference} on {stock_instance.bar} drops below to {stock_instance.stock}, at {datetime.now()}.")
