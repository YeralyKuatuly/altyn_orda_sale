from django.db import models
from orders.models import Order
from procurement.models import Procurement


class PaymentProvider(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text='Название платёжного провайдера (например, Kaspi Pay, Halyk Bank)'
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text='Описание провайдера'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Дата добавления провайдера'
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'payment_providers'


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded')
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('kaspi', 'Kaspi Pay'),
        ('halyk', 'Halyk Pay')
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name='payments',
        help_text='Ссылка на заказ'
    )
    provider = models.ForeignKey(
        PaymentProvider,
        on_delete=models.SET_NULL,
        null=True,
        related_name='payments',
        help_text='Ссылка на платёжного провайдера'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Сумма платежа'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        help_text='Метод оплаты (наличные, карта, Kaspi Pay и т.д.)'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text='Статус платежа'
    )
    transaction_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        help_text='Уникальный идентификатор транзакции для провайдера'
    )
    provider_signature = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Подпись от платёжного провайдера для верификации'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Дата создания платежа'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Дата последнего обновления'
    )

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.order_number}"

    class Meta:
        db_table = 'payments'


class PaymentLog(models.Model):
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='logs',
        help_text='Ссылка на платеж'
    )
    provider = models.ForeignKey(
        PaymentProvider,
        on_delete=models.SET_NULL,
        null=True,
        related_name='logs',
        help_text='Ссылка на платёжного провайдера'
    )
    request_body = models.TextField(
        null=True,
        blank=True,
        help_text='Тело запроса от системы'
    )
    response_body = models.TextField(
        null=True,
        blank=True,
        help_text='Ответ от провайдера'
    )
    status_code = models.IntegerField(
        null=True,
        blank=True,
        help_text='HTTP статус ответа'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Дата и время запроса'
    )

    def __str__(self):
        return f"Log for Payment {self.payment.id}"

    class Meta:
        db_table = 'payment_logs'


class Receipt(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name='receipts',
        help_text='Ссылка на заказ'
    )
    payment = models.ForeignKey(
        Payment,
        on_delete=models.PROTECT,
        related_name='receipts',
        help_text='Ссылка на платеж'
    )
    procurement = models.ForeignKey(
        Procurement,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='receipts',
        help_text='Ссылка на закупку'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Общая сумма чека'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Дата создания чека'
    )
    receipt_number = models.CharField(
        max_length=50,
        unique=True,
        help_text='Уникальный номер чека'
    )
    
    def save(self, *args, **kwargs):
        if not self.receipt_number:
            # Generate a unique receipt number
            last_receipt = Receipt.objects.order_by('-id').first()
            last_number = int(last_receipt.receipt_number.split('-')[1]) if last_receipt else 0
            self.receipt_number = f'RCP-{str(last_number + 1).zfill(8)}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Receipt {self.receipt_number} for Order {self.order.order_number}"

    class Meta:
        db_table = 'receipts'
