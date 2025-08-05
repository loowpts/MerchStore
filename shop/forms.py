from django import forms
from django.forms import inlineformset_factory
from .models import Category, Product, ProductImage, Size

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'main_image', 'stock', 'category', 'available']
        labels = {
            'name': 'Название',
            'description': 'Описание',
            'price': 'Цена',
            'main_image': 'Основное изображение',
            'stock': 'Общий запас',
            'category': 'Категория',
            'available': 'Доступен',
        }

ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    fields=['image'],
    extra=3,
    can_delete=True,
    labels={'image': 'Дополнительное изображение'}
)

class AddToCartForm(forms.Form):
    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
        if product:
            self.fields['size'].queryset = Size.objects.filter(productsize__product=product, productsize__quantity__gt=0)

    size = forms.ModelChoiceField(
        queryset=Size.objects.all(),
        label='Размер',
        empty_label='Выберите размер',
        required=True
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label='Количество'
    )
