from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import PaymentProvider, Payment, PaymentLog, Receipt
from .serializers import (
    PaymentProviderSerializer,
    PaymentSerializer,
    PaymentLogSerializer,
    ReceiptSerializer
)


@extend_schema(tags=['Payments'])
class PaymentProviderViewSet(ModelViewSet):
    queryset = PaymentProvider.objects.all()
    serializer_class = PaymentProviderSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Payments'])
class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        payment = self.get_object()
        # Here you would integrate with actual payment providers
        # This is just a mock implementation
        success = True  # In real implementation, this would depend on provider response

        if success:
            payment.status = 'completed'
            payment.save()

            # Create payment log
            PaymentLog.objects.create(
                payment=payment,
                provider=payment.provider,
                request_body="Payment process request",
                response_body="Payment successful",
                status_code=200
            )

            # Generate receipt
            Receipt.objects.create(
                order=payment.order,
                payment=payment,
                total_amount=payment.amount
            )

            return Response({'status': 'payment processed successfully'})
        return Response({'error': 'payment processing failed'}, status=400)

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        payment = self.get_object()
        if payment.status != 'completed':
            return Response({'error': 'Can only refund completed payments'}, status=400)

        payment.status = 'refunded'
        payment.save()

        PaymentLog.objects.create(
            payment=payment,
            provider=payment.provider,
            request_body="Refund request",
            response_body="Refund processed",
            status_code=200
        )

        return Response({'status': 'refund processed'})

    @action(detail=True, methods=['get'])
    def logs(self, request, pk=None):
        payment = self.get_object()
        logs = payment.logs.all()
        serializer = PaymentLogSerializer(logs, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Payments'])
class PaymentLogViewSet(ModelViewSet):
    queryset = PaymentLog.objects.all()
    serializer_class = PaymentLogSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Payments'])
class ReceiptViewSet(ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        receipt = self.get_object()
        # Here you would generate a PDF receipt
        # This is just a mock implementation
        return Response({
            'receipt_number': receipt.receipt_number,
            'amount': receipt.total_amount,
            'date': receipt.created_at,
            'order_number': receipt.order.order_number
        })
