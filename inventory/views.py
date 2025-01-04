from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.viewsets import ModelViewSet
from .models import Category, Product, Stock
from .serializers import CategorySerializer, ProductSerializer, StockSerializer
from rest_framework.permissions import IsAuthenticated


@extend_schema(tags=["Inventory"])
class CategoryViewSet(ModelViewSet):
    """
    Handles operations related to product categories, including retrieval of 
    categories and their hierarchical relationships (subcategories).
    """
    queryset = Category.objects.prefetch_related('subcategories').all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List all categories and subcategories",
        description=(
            "Retrieve all categories along with their hierarchical "
            "subcategories. The response includes the parent-child "
            "relationship, where each category can have multiple "
            "subcategories. Top-level categories will have `null` "
            "as their parent category."
        ),
        responses={200: CategorySerializer(many=True)},
        examples=[
            OpenApiExample(
                'Category List Response',
                value=[
                    {
                        "id": 1,
                        "name": "Food",
                        "parent_category": None,
                        "subcategories": [
                            {
                                "id": 2,
                                "name": "Fruits",
                                "parent_category": 1
                            },
                            {
                                "id": 3,
                                "name": "Vegetables",
                                "parent_category": 1
                            }
                        ],
                        "created_at": "2025-01-02T12:00:00Z"
                    }
                ]
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieve all categories and their subcategories.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a single category with its subcategories",
        description=(
            "Retrieve detailed information about a single category, "
            "including its subcategories and their hierarchical structure."
        ),
        responses={200: CategorySerializer},
        examples=[
            OpenApiExample(
                'Single Category Response',
                value={
                    "id": 1,
                    "name": "Food",
                    "parent_category": None,
                    "subcategories": [
                        {
                            "id": 2,
                            "name": "Fruits",
                            "parent_category": 1
                        }
                    ],
                    "created_at": "2025-01-02T12:00:00Z"
                }
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific category by ID.
        """
        return super().retrieve(request, *args, **kwargs)


@extend_schema(tags=["Inventory"])
class ProductViewSet(ModelViewSet):
    """
    Handles operations related to products, including listing, retrieval, and
    filtering by category or subcategory.
    """
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List all products",
        description=(
            "Retrieve all products available in the inventory. Optionally, "
            "filter the products by a specific category or subcategory using "
            "the `category_id` query parameter."
        ),
        parameters=[
            OpenApiExample(
                'Filter by Category',
                value={
                    "query_params": {
                        "category_id": 2
                    }
                }
            )
        ],
        responses={200: ProductSerializer(many=True)},
        examples=[
            OpenApiExample(
                'Product List Response',
                value=[
                    {
                        "id": 1,
                        "name": "Apple",
                        "description": "Fresh apples",
                        "price": "120.00",
                        "stock": 100,
                        "category": 2,
                        "created_at": "2025-01-02T12:00:00Z",
                        "updated_at": "2025-01-03T12:00:00Z"
                    },
                    {
                        "id": 2,
                        "name": "Banana",
                        "description": "Ripe bananas",
                        "price": "80.00",
                        "stock": 150,
                        "category": 2,
                        "created_at": "2025-01-02T12:00:00Z",
                        "updated_at": "2025-01-03T12:00:00Z"
                    }
                ]
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieve all products, optionally filtered by category.
        """
        category_id = request.query_params.get('category_id')
        if category_id:
            self.queryset = self.queryset.filter(category_id=category_id)
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a single product",
        description=(
            "Retrieve detailed information about a single product, including "
            "its category and stock information."
        ),
        responses={200: ProductSerializer},
        examples=[
            OpenApiExample(
                'Single Product Response',
                value={
                    "id": 1,
                    "name": "Apple",
                    "description": "Fresh apples",
                    "price": "120.00",
                    "stock": 100,
                    "category": 2,
                    "created_at": "2025-01-02T12:00:00Z",
                    "updated_at": "2025-01-03T12:00:00Z"
                }
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific product by ID.
        """
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
