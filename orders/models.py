from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Product, Size
from users.models import UserProfile

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает обработки'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Покупатель'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    shipping_address = models.CharField(max_length=255, blank=True, verbose_name='Адрес доставки')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='Номер телефона')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Общая сумма')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ {self.id} от {self.user.username} ({self.get_status_display()})'

    def calculate_total_price(self):
        total = sum(item.total_price() for item in self.items.all())
        self.total_price = total
        self.save()
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        verbose_name='Размер',
        null=True
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
        unique_together = ('order', 'product', 'size')

    def __str__(self):
        size_name = self.size.name if self.size else 'Размер не указан'
        return f'{self.quantity} x {self.product.name} ({size_name})'


    def total_price(self):
        return self.quantity * self.price
