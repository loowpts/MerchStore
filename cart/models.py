from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Product

User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Покупатель'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    @property
    def total_price(self):
        total = sum(product.total_price() for product in self.items.all())
        return total if total else 0.0 
    
    def __str__(self) -> str:
        return f'Корзина {self.id} для {self.user.username}'
    
    def clear(self):
        self.items.all().delete()

class CartProduct(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def total_price(self):
        total_price = self.quantity * self.product.price
        return total_price if total_price else 0.0 
    
    def __str__(self) -> str:
        return f'{self.quantity} x {self.product.name}'
