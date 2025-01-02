from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import (
    User, Role, Permission, RolePermission,
    UserRole, UserAddress
)
from .serializers import (
    UserSerializer,
    RoleSerializer,
    PermissionSerializer,
    RolePermissionSerializer,
    UserRoleSerializer,
    UserAddressSerializer
)
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


@extend_schema(tags=['accounts'])
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'], permission_classes=[])
    def assign_role(self, request, pk=None):
        user = self.get_object()
        role_id = request.data.get('role_id')
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response({"error": "Role not found"}, status=404)

        UserRole.objects.create(user=user, role=role)
        return Response({"message": "Role assigned successfully"})

    @extend_schema(
        tags=["Users"],
        summary="Retrieve a list of all users",
        description=(
            "This endpoint returns all registered users with their details."
        ),
        examples=[
            OpenApiExample(
                "Example Response",
                value=[
                    {
                        "id": 1,
                        "username": "john_doe",
                        "telegram_id": "123456",
                        "phone_number": "+70777777777"
                    },
                    {
                        "id": 2,
                        "username": "jane_doe",
                        "telegram_id": "654321",
                        "phone_number": "+70777777777"
                    }
                ]
            )
        ],
        responses={200: UserSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=['accounts'])
class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class RolePermissionViewSet(ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer


class UserRoleViewSet(ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer


class UserAddressViewSet(ModelViewSet):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer


@api_view(['GET'])
@extend_schema(tags=['system'])
def test_db_connection(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            return Response(
                {'status': 'Database connection successful'},
                content_type='application/json'
            )
    except Exception as e:
        return Response(
            {
                'status': 'Database connection failed',
                'error': str(e)
            },
            status=500,
            content_type='application/json'
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def telegram_login(request):
    telegram_id = request.data.get('telegram_id')
    
    try:
        user = User.objects.get(telegram_id=telegram_id)
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)
