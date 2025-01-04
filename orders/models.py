from django.db import models
from django.core.validators import MinValueValidator
from django.utils.crypto import get_random_string
from inventory.models import Product
from accounts.models import User


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="orders",
        help_text='Пользователь, обработавший заказ'
    )
    order_number = models.CharField(
        max_length=10, 
        unique=True, 
        editable=False
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        help_text='Статус заказа (pending, completed, canceled)'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0.0)],
        help_text='Итоговая стоимость'
    )
    delivery_address = models.TextField(
        help_text='Адрес доставки'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Дата создания заказа'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Дата последнего обновления'
    )

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def _generate_order_number(self):
        """Generate a unique order number"""
        while True:
            order_number = f"ORD-{get_random_string(6).upper()}"
            if not Order.objects.filter(order_number=order_number).exists():
                return order_number

    def __str__(self):
        return f"Order #{self.order_number} by {self.user.username}"

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE, 
        related_name="items",
        help_text='Ссылка на заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE, 
        related_name="order_items",
        help_text='Ссылка на товар'
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text='Количество товаров'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0)],
        help_text='Цена за единицу'
    )

    def __str__(self):
        return f"{self.product.name} x{self.quantity}"

    class Meta:
        db_table = 'order_items'


class OrderChangeHistory(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name="change_history",
        help_text='Ссылка на заказ'
    )
    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, 
        null=True,
        related_name="order_changes",
        help_text='Ссылка на пользователя, который внёс изменения'
    )
    field_name = models.CharField(
        max_length=50,
        help_text='Изменённое поле (status, address, courier)'
    )
    old_value = models.TextField(
        null=True,
        blank=True,
        help_text='Старое значение поля'
    )
    new_value = models.TextField(
        null=True,
        blank=True,
        help_text='Новое значение поля'
    )
    changed_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Дата и время изменения'
    )

    def __str__(self):
        return f"Change in Order #{self.order.order_number} by {self.changed_by.username}"

    class Meta:
        db_table = 'order_change_history'
        ordering = ['-changed_at']
