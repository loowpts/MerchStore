from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'phone_number']
        labels = {
            'shipping_address': 'Адрес доставки',
            'phone_number': 'Номер телефона',
        }
