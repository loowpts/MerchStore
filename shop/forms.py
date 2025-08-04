from django import forms
from django.forms import inlineformset_factory
from .models import Category, Product, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'main_image', 'stock', 'category']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'price': 'Цена',
            'main_image': 'Фото товара',
            'stock': 'Количество на складе',
            'category': 'Категория',
        }

ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    fields=['image'],
    extra=3,
    can_delete=True,
    labels={'image': 'Дополнительное фото'}
)
