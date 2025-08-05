from django.urls import path
from .views import order_create, order_list, order_detail

app_name = 'orders'

urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('', order_list, name='order_list'),
    path('<int:order_id>/', order_detail, name='order_detail'),
]
