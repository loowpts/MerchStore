from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('product_list/', views.product_list, name='product_list'),
    path('product/create/', views.product_create, name='product_create'),  # Moved up
    path('product/<int:pk>/edit/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),  # Moved down
]
