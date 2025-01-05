from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PaymentProviderViewSet,
    PaymentViewSet,
    PaymentLogViewSet,
    ReceiptViewSet
)

router = DefaultRouter()
router.register(r'providers', PaymentProviderViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'logs', PaymentLogViewSet)
router.register(r'receipts', ReceiptViewSet)


urlpatterns = router.urls
