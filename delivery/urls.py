from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourierViewSet,
    DeliveryViewSet,
    DeliveryStatusHistoryViewSet
)

router = DefaultRouter()
router.register(r'couriers', CourierViewSet)
router.register(r'deliveries', DeliveryViewSet)
router.register(r'status-history', DeliveryStatusHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
