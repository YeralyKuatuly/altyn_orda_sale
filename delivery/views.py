from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import Courier, Delivery, DeliveryStatusHistory, DeliveryLog, CourierDeliveryHistory
from .serializers import (
    CourierSerializer,
    DeliverySerializer,
    DeliveryStatusHistorySerializer,
    DeliveryLogSerializer,
    CourierDeliveryHistorySerializer
)


@extend_schema(tags=['Delivery'])
class CourierViewSet(ModelViewSet):
    queryset = Courier.objects.all()
    serializer_class = CourierSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def update_location(self, request, pk=None):
        courier = self.get_object()
        location = request.data.get('location')

        if location:
            courier.current_location = location
            courier.save()
            return Response({'status': 'location updated'})
        return Response({'error': 'location is required'}, status=400)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        courier = self.get_object()
        status = request.data.get('status')

        if status in dict(Courier.STATUS_CHOICES):
            courier.status = status
            courier.save()
            return Response({'status': 'courier status updated'})
        return Response({'error': 'invalid status'}, status=400)


@extend_schema(tags=['Delivery'])
class DeliveryViewSet(ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        delivery = self.get_object()
        status = request.data.get('status')
        notes = request.data.get('notes')
        location = request.data.get('location')

        if status not in dict(Delivery.STATUS_CHOICES):
            return Response({'error': 'invalid status'}, status=400)

        delivery.status = status
        delivery.save()

        # Create status history entry
        DeliveryStatusHistory.objects.create(
            delivery=delivery,
            status=status,
            location=location,
            notes=notes,
            created_by=request.user
        )

        return Response({'status': 'delivery status updated'})

    @action(detail=True, methods=['post'])
    def assign_courier(self, request, pk=None):
        delivery = self.get_object()
        courier_id = request.data.get('courier_id')

        if not courier_id:
            return Response({'error': 'courier_id is required'}, status=400)

        courier = get_object_or_404(Courier, id=courier_id)
        delivery.courier = courier
        delivery.status = 'assigned'
        delivery.save()

        DeliveryStatusHistory.objects.create(
            delivery=delivery,
            status='assigned',
            notes=f'Assigned to courier {courier.user.username}',
            created_by=request.user
        )

        return Response({'status': 'courier assigned successfully'})


@extend_schema(tags=['Delivery'])
class DeliveryStatusHistoryViewSet(ModelViewSet):
    queryset = DeliveryStatusHistory.objects.all()
    serializer_class = DeliveryStatusHistorySerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Delivery'])
class DeliveryLogViewSet(ModelViewSet):
    queryset = DeliveryLog.objects.all()
    serializer_class = DeliveryLogSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Delivery'])
class CourierDeliveryHistoryViewSet(ModelViewSet):
    queryset = CourierDeliveryHistory.objects.all()
    serializer_class = CourierDeliveryHistorySerializer
    permission_classes = [IsAuthenticated]
