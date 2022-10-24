from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register("references", BeerList, basename="beer_list")
router.register("bars", BarList, basename="bar_list")
router.register("stocks", StockList, basename="stock_list")
router.register("statistics", Statistics, basename="statistics")
router.register("orders", OrderList, basename="order_detail")
