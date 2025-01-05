import factory
from factory.django import DjangoModelFactory
from accounts.models import User, Role, Permission, RolePermission, UserRole, UserAddress, Client
from django.utils import timezone


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    email = factory.Faker('email')
    phone_number = factory.Sequence(lambda n: f'+7707{n:07d}')
    password = 'testpass123'

    # Remove the default username generation
    username = None

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            return

        # Use the default password for telegram users if telegram_id is set
        if self.telegram_id:
            self.set_password(User.DEFAULT_PASSWORD)
        else:
            self.set_password(extracted or 'testpass123')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the creation to ensure proper username assignment"""
        if 'username' not in kwargs:
            # Let the model's save() method handle username assignment
            kwargs['username'] = None
        return super()._create(model_class, *args, **kwargs)


class RoleFactory(DjangoModelFactory):
    class Meta:
        model = Role

    name = factory.Sequence(lambda n: f'role_{n}')
    description = factory.Faker('text', max_nb_chars=200)


class PermissionFactory(DjangoModelFactory):
    class Meta:
        model = Permission

    name = factory.Sequence(lambda n: f'permission_{n}')
    description = factory.Faker('text', max_nb_chars=200)


class RolePermissionFactory(DjangoModelFactory):
    class Meta:
        model = RolePermission

    role = factory.SubFactory(RoleFactory)
    permission = factory.SubFactory(PermissionFactory)


class UserRoleFactory(DjangoModelFactory):
    class Meta:
        model = UserRole

    user = factory.SubFactory(UserFactory)
    role = factory.SubFactory(RoleFactory)


class UserAddressFactory(DjangoModelFactory):
    class Meta:
        model = UserAddress

    user = factory.SubFactory(UserFactory)
    address = factory.Faker('address')


class ClientFactory(DjangoModelFactory):
    class Meta:
        model = Client

    user = factory.SubFactory(UserFactory)
    created_at = factory.LazyFunction(timezone.now)
