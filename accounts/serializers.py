from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import (
    User, Role, Permission, RolePermission,
    UserRole, UserAddress
)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'description']


class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']


class UserRoleSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = UserRole
        fields = ['role']


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['id', 'address', 'last_used_at']


class UserSerializer(serializers.ModelSerializer):
    addresses = UserAddressSerializer(many=True, read_only=True)
    roles = UserRoleSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'telegram_id',
            'phone_number',
            'email',
            'addresses',
            'roles',
            # Temporarily remove until migration is fixed
            # 'is_telegram_user'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_telegram_id(self, value):
        if User.objects.filter(telegram_id=value).exists():
            raise ValidationError("This Telegram ID is already registered.")
        return value
