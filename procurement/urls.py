from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PurchaserViewSet, ProcurementViewSet

router = DefaultRouter()
router.register('purchasers', PurchaserViewSet, basename='purchaser')
router.register('procurements', ProcurementViewSet, basename='procurement')

urlpatterns = [
    path('', include(router.urls)),
]