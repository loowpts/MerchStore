from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Order, OrderItem
from .forms import OrderForm, OrderStatusForm
from cart.models import Cart

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_create(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        messages.error(request, 'Ваша корзина пуста.')
        return redirect('cart:cart')
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.total_price
            order.save()
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    size=item.size,
                    quantity=item.quantity,
                    price=item.product.price
                )
            cart.items.all().delete()
            messages.success(request, 'Заказ успешно создан.')
            return redirect('orders:order_payment', order_id=order.id)
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = OrderForm()
    return render(request, 'orders/order_create.html', {'form': form, 'cart': cart})

@login_required
def order_update_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user.is_staff or request.user == order.user:
        if request.method == 'POST':
            form = OrderStatusForm(request.POST, instance=order)
            if form.is_valid():
                form.save()
                messages.success(request, 'Статус заказа обновлен.')
                return redirect('orders:order_detail', order_id=order.id)
            else:
                messages.error(request, 'Исправьте ошибки в форме.')
        else:
            form = OrderStatusForm(instance=order)
        return render(request, 'orders/order_status_form.html', {'form': form, 'order': order})
    else:
        messages.error(request, 'У вас нет прав для изменения статуса заказа.')
        return redirect('orders:order_detail', order_id=order.id)

@login_required
def order_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.status = 'paid'
        order.save()
        messages.success(request, 'Оплата успешно завершена (демо).')
        return redirect('orders:order_detail', order_id=order.id)
    return render(request, 'orders/order_payment.html', {'order': order})
