from django.contrib import admin
from .models import (
    User, Role, Permission, RolePermission,
    UserRole, UserAddress
)

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(RolePermission)
admin.site.register(UserRole)
admin.site.register(UserAddress)
