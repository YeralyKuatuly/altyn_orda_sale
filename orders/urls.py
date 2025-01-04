from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrderViewSet,
    OrderItemViewSet,
    OrderChangeHistoryViewSet
)

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='order')
router.register('items', OrderItemViewSet, basename='orderitem')
router.register('history', OrderChangeHistoryViewSet, basename='orderhistory')

urlpatterns = [
    path('', include(router.urls)),
]
