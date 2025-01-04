from rest_framework import permissions
from .models import Order, OrderItem


class IsOrderOwnerOrStaff(permissions.BasePermission):
    """
    Custom permission to only allow owners of an order or staff members to access it.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        # For OrderItem objects, navigate through the order to the user
        if isinstance(obj, OrderItem):
            return obj.order.user == request.user
        # For Order objects, check directly
        return obj.user == request.user


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow staff members to edit objects.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
