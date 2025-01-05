from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    ProductViewSet,
    StockViewSet,
    WarehouseViewSet,
    WarehouseLogViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'stocks', StockViewSet, basename='stock')
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')
router.register(r'warehouse-logs', WarehouseLogViewSet, basename='warehouse-log')


urlpatterns = router.urls
