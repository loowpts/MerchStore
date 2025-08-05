from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from cart.models import Cart, CartProduct
from users.models import UserProfile
from .models import Order, OrderItem
from .forms import OrderCreateForm


@login_required
def order_create(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        messages.error(request, 'Ваша корзина пуста.')
        return redirect('cart:cart')

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.shipping_address = form.cleaned_data['shipping_address'] or profile.address
            order.phone_number = form.cleaned_data['phone_number'] or profile.phone_number
            order.save()

            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    size=cart_item.size,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            cart.clear()
            messages.success(request, f'Заказ #{order.id} успешно создан!')
            return redirect('orders:order_detail', order_id=order.id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
    else:
        form = OrderCreateForm(initial={
            'shipping_address': profile.address,
            'phone_number': profile.phone_number
        })

    return render(request, 'orders/order_create.html', {'form': form, 'cart': cart})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
