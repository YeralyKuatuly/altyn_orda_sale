import factory
from factory.django import DjangoModelFactory
from django.utils import timezone
from accounts.models import User
from procurement.models import Purchaser, Procurement
from inventory.tests.test_factories import ProductFactory, WarehouseFactory
from delivery.tests.test_factories import CourierFactory  # You'll need to create this


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'testuser_{n}')  # Changed to ensure uniqueness
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')


class PurchaserFactory(DjangoModelFactory):
    class Meta:
        model = Purchaser

    user = factory.SubFactory(UserFactory)
    created_at = factory.LazyFunction(timezone.now)


class ProcurementFactory(DjangoModelFactory):
    class Meta:
        model = Procurement

    purchaser = factory.SubFactory(PurchaserFactory)
    warehouse_courier = factory.SubFactory('delivery.tests.factories.CourierFactory')
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker('random_int', min=1, max=100)
    price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    warehouse = factory.SubFactory(WarehouseFactory)
