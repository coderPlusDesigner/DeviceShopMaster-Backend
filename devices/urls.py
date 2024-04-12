from django.urls import path
from .views import ProductsView, AllProductsView, CreateProductsView, UpdateProductsView, filterProduct

urlpatterns = [
    path('', ProductsView.as_view()),
    path('all/', AllProductsView.as_view()),
    path('<int:pk>/', UpdateProductsView.as_view()),
    path('create/', CreateProductsView.as_view()),
    path('filter/', filterProduct),
]
