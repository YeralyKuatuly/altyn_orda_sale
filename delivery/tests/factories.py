import factory
from factory.django import DjangoModelFactory
from django.utils import timezone
from delivery.models import Courier, Delivery, DeliveryStatusHistory, DeliveryLog, CourierDeliveryHistory
from accounts.models import User
from orders.models import Order


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')


class CourierFactory(DjangoModelFactory):
    class Meta:
        model = Courier

    user = factory.SubFactory(UserFactory)
    courier_type = 'client'
    status = 'available'
    phone = factory.Sequence(lambda n: f'+7707{n:07d}')


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    status = 'pending'
    total_price = 1000.00
    delivery_address = 'Test Delivery Address'


class DeliveryFactory(DjangoModelFactory):
    class Meta:
        model = Delivery

    order = factory.SubFactory(OrderFactory)
    courier = factory.SubFactory(CourierFactory)
    status = 'pending'
    pickup_location = 'Test Pickup Location'
    delivery_location = 'Test Delivery Location'
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)


class DeliveryStatusHistoryFactory(DjangoModelFactory):
    class Meta:
        model = DeliveryStatusHistory

    delivery = factory.SubFactory(DeliveryFactory)
    status = 'pending'
    created_by = factory.SubFactory(UserFactory)


class DeliveryLogFactory(DjangoModelFactory):
    class Meta:
        model = DeliveryLog

    delivery = factory.SubFactory(DeliveryFactory)
    message = factory.Faker('text')
    created_at = factory.LazyFunction(timezone.now)


class CourierDeliveryHistoryFactory(DjangoModelFactory):
    class Meta:
        model = CourierDeliveryHistory

    courier = factory.SubFactory(CourierFactory)
    order = factory.SubFactory(OrderFactory)
    delivered_at = factory.LazyFunction(timezone.now)
