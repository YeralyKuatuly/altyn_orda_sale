from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent_category = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.parent_category.name} -> {self.name}" if self.parent_category else self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_entries")
    quantity = models.IntegerField(default=0)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Warehouse(models.Model):
    name = models.CharField(
        max_length=255,
        help_text='Название склада'
    )
    address = models.TextField(
        help_text='Адрес склада'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='warehouse_entries',
        help_text='Ссылка на товар'
    )
    quantity = models.IntegerField(
        help_text='Количество на складе'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Дата последнего обновления'
    )

    def __str__(self):
        return f"{self.name} - {self.product.name}"

    class Meta:
        db_table = 'warehouse'


class WarehouseLog(models.Model):
    OPERATION_CHOICES = [
        ('arrival', 'Прибытие'),
        ('expense', 'Расход')
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='warehouse_logs',
        help_text='Ссылка на товар'
    )
    quantity = models.IntegerField(
        help_text='Количество (прибавлено или убавлено)'
    )
    operation_type = models.CharField(
        max_length=20,
        choices=OPERATION_CHOICES,
        help_text='Тип операции (прибытие, расход)'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Дата операции'
    )

    def __str__(self):
        return f"{self.operation_type} - {self.product.name} ({self.quantity})"

    class Meta:
        db_table = 'warehouse_logs'
