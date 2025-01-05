from django.db.models import Sum, Count
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import Purchaser, Procurement
from .serializers import PurchaserSerializer, ProcurementSerializer


@extend_schema(tags=['procurement'])
class PurchaserViewSet(ModelViewSet):
    queryset = Purchaser.objects.all()
    serializer_class = PurchaserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def procurement_history(self, request, pk=None):
        """Get procurement history for a specific purchaser"""
        purchaser = self.get_object()
        procurements = Procurement.objects.filter(purchaser=purchaser)
        serializer = ProcurementSerializer(procurements, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get procurement statistics for a specific purchaser"""
        purchaser = self.get_object()
        stats = Procurement.objects.filter(purchaser=purchaser).aggregate(
            total_procurements=Count('id'),
            total_spent=Sum('price'),
            total_items=Sum('quantity')
        )
        return Response(stats)


@extend_schema(tags=['procurement'])
class ProcurementViewSet(ModelViewSet):
    queryset = Procurement.objects.all()
    serializer_class = ProcurementSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print("Received data:", request.data)  # Debug print
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # Update warehouse stock when procurement is created
        procurement = serializer.save()
        warehouse = procurement.warehouse
        warehouse.quantity += procurement.quantity
        warehouse.save()

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent procurements"""
        recent = Procurement.objects.all().order_by('-created_at')[:10]
        serializer = self.get_serializer(recent, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get overall procurement statistics"""
        stats = Procurement.objects.aggregate(
            total_procurements=Count('id'),
            total_spent=Sum('price'),
            total_items=Sum('quantity')
        )
        return Response(stats)

    def get_queryset(self):
        queryset = Procurement.objects.all()

        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date and end_date:
            queryset = queryset.filter(
                created_at__range=[start_date, end_date]
            )

        # Filter by purchaser
        purchaser_id = self.request.query_params.get('purchaser_id', None)
        if purchaser_id:
            queryset = queryset.filter(purchaser_id=purchaser_id)

        # Filter by product
        product_id = self.request.query_params.get('product_id', None)
        if product_id:
            queryset = queryset.filter(product_id=product_id)

        return queryset
