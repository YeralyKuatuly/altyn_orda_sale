from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import User
from orders.models import Order


class Courier(models.Model):
    COURIER_TYPE_CHOICES = [
        ('client', 'Client Courier'),
        ('warehouse', 'Warehouse Courier'),
        ('both', 'Both Types')
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('on_delivery', 'On Delivery'),
        ('offline', 'Offline')
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='courier_profile',
        help_text='Связанный пользователь'
    )
    courier_type = models.CharField(
        max_length=20,
        choices=COURIER_TYPE_CHOICES,
        default='client',
        help_text='Тип курьера (client, warehouse, both)'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        help_text='Статус курьера'
    )
    phone = models.CharField(
        max_length=15,
        help_text='Контактный телефон курьера'
    )
    current_location = models.TextField(
        null=True,
        blank=True,
        help_text='Текущее местоположение курьера'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Дата регистрации курьера'
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_courier_type_display()}"

    class Meta:
        db_table = 'couriers'


class Delivery(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Assignment'),
        ('assigned', 'Assigned to Courier'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled')
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='delivery',
        help_text='Связанный заказ'
    )
    courier = models.ForeignKey(
        Courier,
        on_delete=models.SET_NULL,
        null=True,
        related_name='deliveries',
        help_text='Назначенный курьер'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text='Статус доставки'
    )
    pickup_location = models.TextField(
        help_text='Адрес получения заказа'
    )
    delivery_location = models.TextField(
        help_text='Адрес доставки'
    )
    estimated_delivery_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Ожидаемое время доставки'
    )
    actual_delivery_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Фактическое время доставки'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Дата последнего обновления'
    )

    def __str__(self):
        return f"Delivery for Order #{self.order.order_number}"

    class Meta:
        db_table = 'deliveries'
        ordering = ['-created_at']


class DeliveryStatusHistory(models.Model):
    delivery = models.ForeignKey(
        Delivery,
        on_delete=models.CASCADE,
        related_name='status_history',
        help_text='Связанная доставка'
    )
    status = models.CharField(
        max_length=20,
        choices=Delivery.STATUS_CHOICES,
        help_text='Статус доставки'
    )
    location = models.TextField(
        null=True,
        blank=True,
        help_text='Местоположение при смене статуса'
    )
    notes = models.TextField(
        null=True,
        blank=True,
        help_text='Дополнительные заметки'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Время создания записи'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='delivery_status_updates',
        help_text='Кто создал запись'
    )

    def __str__(self):
        return f"{self.delivery} - {self.status}"

    class Meta:
        db_table = 'delivery_status_history'
        ordering = ['-created_at']
