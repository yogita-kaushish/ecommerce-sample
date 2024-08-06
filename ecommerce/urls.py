from django.contrib import admin
from django.urls import path
from shop.views import products,product_detail,list_products,add_product,edit_product,delete_product

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',list_products,name='list_products'),
    path('list_products/', list_products, name='list_products'),
    path('add_product/', add_product, name='add_product'),
    path('edit_product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', delete_product, name='delete_product'),
    path('api/v1/products/', products, name='create_product'),
    path('api/v1/products/<int:product_id>/', product_detail, name='product_detail'),

]
