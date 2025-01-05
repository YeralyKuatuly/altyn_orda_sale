from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, RoleViewSet, PermissionViewSet,
    RolePermissionViewSet, UserRoleViewSet, UserAddressViewSet,
    ClientViewSet, test_db_connection, telegram_login
)


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'role-permissions', RolePermissionViewSet)
router.register(r'user-roles', UserRoleViewSet)
router.register(r'addresses', UserAddressViewSet)
router.register(r'clients', ClientViewSet, basename='client')

urlpatterns = [
    path('', include(router.urls)),
    path('test-db/', test_db_connection, name='test-db'),
    path('telegram-login/', telegram_login, name='telegram-login'),
]
