import factory
from factory.django import DjangoModelFactory
from payments.models import PaymentProvider, Payment, PaymentLog, Receipt
from orders.tests.factories import OrderFactory


class PaymentProviderFactory(DjangoModelFactory):
    class Meta:
        model = PaymentProvider

    name = factory.Sequence(lambda n: f'provider_{n}')
    description = factory.Faker('text')


class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = Payment

    order = factory.SubFactory(OrderFactory)
    provider = factory.SubFactory(PaymentProviderFactory)
    amount = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    payment_method = 'card'
    status = 'pending'


class PaymentLogFactory(DjangoModelFactory):
    class Meta:
        model = PaymentLog

    payment = factory.SubFactory(PaymentFactory)
    provider = factory.SubFactory(PaymentProviderFactory)
    status_code = 200


class ReceiptFactory(DjangoModelFactory):
    class Meta:
        model = Receipt

    order = factory.SubFactory(OrderFactory)
    payment = factory.SubFactory(PaymentFactory)
    total_amount = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
