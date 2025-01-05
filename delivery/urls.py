from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourierViewSet,
    DeliveryViewSet,
    DeliveryStatusHistoryViewSet,
    DeliveryLogViewSet,
    CourierDeliveryHistoryViewSet
)

router = DefaultRouter()
router.register(r'couriers', CourierViewSet)
router.register(r'deliveries', DeliveryViewSet)
router.register(r'status-history', DeliveryStatusHistoryViewSet)
router.register(r'delivery-logs', DeliveryLogViewSet, basename='delivery-log')
router.register(r'courier-history', CourierDeliveryHistoryViewSet, basename='courier-history')

urlpatterns = [
    path('', include(router.urls)),
]
