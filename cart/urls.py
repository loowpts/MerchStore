from django.urls import path

from .views import add_to_cart, cart, delete_cart_product, update_cart_product

app_name = 'cart'

urlpatterns = [
    path('', cart, name='cart'),
    path('add/<slug:item_slug>/', add_to_cart, name='add_to_cart'),
    path('delete/<slug:item_slug>/', delete_cart_product, name='delete_cart_product'),
    path('update_cart_item/', update_cart_product, name='update_cart_product'),
]
