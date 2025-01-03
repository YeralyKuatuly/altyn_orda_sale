from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.viewsets import ModelViewSet
from .models import Category, Product, Stock
from .serializers import CategorySerializer, ProductSerializer, StockSerializer
from rest_framework.permissions import IsAuthenticated


@extend_schema(tags=["Inventory"])
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List all categories",
        description="Retrieve a list of all product categories.",
        responses={200: CategorySerializer(many=True)},
        examples=[
            OpenApiExample(
                'Category List Response',
                value=[
                    {
                        "id": 1,
                        "name": "Electronics",
                        "description": "Electronic devices and accessories"
                    }
                ]
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


@extend_schema(tags=["Inventory"])
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List all products",
        description="Retrieve a list of all products.",
        responses={200: ProductSerializer(many=True)},
        examples=[
            OpenApiExample(
                'Product List Response',
                value=[
                    {
                        "id": 1,
                        "name": "Smartphone",
                        "description": "Latest model smartphone",
                        "price": "999.99",
                        "category": 1
                    }
                ]
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a single product",
        description="Get detailed information about a specific product.",
        responses={200: ProductSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@extend_schema(tags=["Inventory"])
class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List all stock items",
        description="Retrieve a list of all stock items.",
        responses={200: StockSerializer(many=True)},
        examples=[
            OpenApiExample(
                'Stock List Response',
                value=[
                    {
                        "id": 1,
                        "product": 1,
                        "quantity": 100,
                        "location": "Warehouse A"
                    }
                ]
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Update stock quantity",
        description="Update the quantity and location of a stock item.",
        request=StockSerializer,
        responses={200: StockSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
