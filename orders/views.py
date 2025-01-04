from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Order, OrderItem, OrderChangeHistory
from .serializers import (
    OrderSerializer,
    OrderItemSerializer,
    OrderChangeHistorySerializer
)
from .permissions import IsOrderOwnerOrStaff, IsStaffOrReadOnly


@extend_schema(tags=["Orders"])
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    @extend_schema(
        summary="Change order status",
        description="Updates the status of an order. Staff only."
    )
    @action(detail=True, methods=['patch'], url_path='change-status')
    def change_status(self, request, pk=None):
        order = self.get_object()

        if not request.user.is_staff:
            return Response(
                {"error": "Only staff can change order status."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {"error": "Invalid status."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        old_status = order.status
        order.status = new_status
        order.save()

        OrderChangeHistory.objects.create(
            order=order,
            changed_by=request.user,
            field_name="status",
            old_value=old_status,
            new_value=new_status
        )

        return Response({"message": "Status updated successfully."})

@extend_schema(tags=["Orders"])
class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated, IsOrderOwnerOrStaff]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__user=user)

@extend_schema(tags=["Orders"])
class OrderChangeHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = OrderChangeHistorySerializer
    permission_classes = [IsAuthenticated, IsOrderOwnerOrStaff]
    http_method_names = ['get', 'head', 'options']  # Read-only

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return OrderChangeHistory.objects.all()
        return OrderChangeHistory.objects.filter(order__user=user)
