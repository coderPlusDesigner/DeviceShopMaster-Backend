from rest_framework import generics
from .models import Products
from .serializers import ProductsSerializer, CreateProductsSerializer, UpdateProductsSerializer
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import permission_classes
from django.db.models import Q, Subquery, OuterRef
from rest_framework.decorators import api_view
from rest_framework.response import Response


class RowPagination(PageNumberPagination):
    page_size = 10


class ProductsView(generics.ListAPIView):
    queryset = Products.objects.all().order_by('-updated_date')
    serializer_class = ProductsSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = RowPagination


class AllProductsView(generics.ListAPIView):
    queryset = Products.objects.all().order_by('-updated_date')
    serializer_class = ProductsSerializer
    permission_classes = [permissions.AllowAny]


class CreateProductsView(generics.CreateAPIView):
    queryset = Products.objects.all()
    serializer_class = CreateProductsSerializer
    permission_classes = [permissions.IsAdminUser]
    
  
class UpdateProductsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = UpdateProductsSerializer
    permission_classes = [permissions.IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.image.delete()
        instance.thumbnail.delete()
        return super().destroy(request, *args, **kwargs)



@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def filterProduct(request):
    query = request.query_params.get('query', '')
    p_category = request.query_params.get('category', '')
    if query:
        products = Products.objects.filter(Q(device_model__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query))
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)
    elif p_category:
        products = Products.objects.filter(Q(category__icontains=p_category))
        serializer = ProductsSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})