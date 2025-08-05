from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<slug:item_slug>/<int:size_id>/<int:quantity>/', views.add_to_cart, name='add_to_cart'),
    path('delete/<slug:item_slug>/', views.delete_cart_product, name='delete_cart_product'),
    path('update/', views.update_cart_product, name='update_cart_product'),
]
