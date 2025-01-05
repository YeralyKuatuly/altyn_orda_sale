import factory
from factory.django import DjangoModelFactory
from inventory.models import Category, Product, Warehouse


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'Category {n}')


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f'Product {n}')
    description = factory.Faker('text')
    price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    stock = factory.Faker('random_int', min=1, max=100)
    category = factory.SubFactory(CategoryFactory)


class WarehouseFactory(DjangoModelFactory):
    class Meta:
        model = Warehouse

    name = factory.Sequence(lambda n: f'Warehouse {n}')
    address = factory.Faker('address')
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker('random_int', min=0, max=1000)
