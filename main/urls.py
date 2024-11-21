from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path('categories/', views.CategoryListView.as_view(), name='category'),
    path('products/<int:category_id>/', views.ProductListView.as_view(), name='products'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
