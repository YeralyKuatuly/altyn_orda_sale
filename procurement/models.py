from django.db import models
from accounts.models import User
from inventory.models import Product, Warehouse
from delivery.models import Courier


class Purchaser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='purchaser_profile',
        help_text='Ссылка на пользователя из таблицы users'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Дата регистрации закупщика'
    )

    def __str__(self):
        return f"Purchaser: {self.user.username}"

    class Meta:
        db_table = 'purchasers'


class Procurement(models.Model):
    purchaser = models.ForeignKey(
        Purchaser,
        on_delete=models.PROTECT,
        related_name='procurements',
        help_text='Ссылка на закупщика'
    )
    warehouse_courier = models.ForeignKey(
        Courier,
        on_delete=models.PROTECT,
        related_name='warehouse_deliveries',
        help_text='Ссылка на курьера, доставившего на склад'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='procurements',
        help_text='Ссылка на товар'
    )
    quantity = models.IntegerField(
        help_text='Количество закупленного товара'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Цена закупки'
    )
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        related_name='procurements',
        help_text='Ссылка на склад'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Дата закупки'
    )

    def __str__(self):
        return f"Procurement #{self.id} by {self.purchaser.user.username}"

    class Meta:
        db_table = 'procurement'
