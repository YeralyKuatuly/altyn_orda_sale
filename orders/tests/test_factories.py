import factory
from factory.django import DjangoModelFactory
from decimal import Decimal
from django.contrib.auth import get_user_model
from orders.models import Order, OrderItem
from inventory.models import Category, Product

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user_{n}')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'Category {n}')


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f'Product {n}')
    price = Decimal('10.00')
    stock = 50
    category = factory.SubFactory(CategoryFactory)


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    order_number = factory.Sequence(lambda n: f'ORD-{n:06}')
    user = factory.SubFactory('accounts.tests.factories.UserFactory')
    status = 'pending'
    total_price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    delivery_address = factory.Faker('address')

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product in extracted:
                OrderItemFactory(order=self, product=product)


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 2
    price = Decimal('10.00')
