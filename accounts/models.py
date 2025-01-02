from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True, db_index=True)
    telegram_id = models.CharField(max_length=50, unique=True, null=True, blank=True, db_index=True)

    # Make password optional
    password = models.CharField(max_length=128, null=True, blank=True)

    # Optional fields for Telegram users
    email = models.EmailField(null=True, blank=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True, db_index=True)

    # Add default value for existing records
    is_telegram_user = models.BooleanField(default=False, db_index=True)

    DEFAULT_PASSWORD = "telegram_user_default_password"

    def save(self, *args, **kwargs):
        if self.telegram_id:
            self.is_telegram_user = True
            if not self.password:
                self.password = make_password(self.DEFAULT_PASSWORD)

        if not self.username:
            self.username = self.telegram_id or self.phone_number or f"user_{self.id}"

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'users'


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Permission(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permissions")
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="roles")

    class Meta:
        unique_together = ("role", "permission")

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="users")

    class Meta:
        unique_together = ("user", "role")

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    address = models.TextField()
    last_used_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.address}"
