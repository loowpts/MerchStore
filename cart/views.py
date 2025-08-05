from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from shop.models import Product
from .models import Cart, CartProduct

@login_required
def cart(request):
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        cart = Cart.objects.create(user=request.user)

    cart_items = CartProduct.objects.filter(cart=cart)
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'cart_items': cart_items
    })

@login_required
def add_to_cart(request, item_slug):
    product = get_object_or_404(Product, slug=item_slug)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_product, created = CartProduct.objects.get_or_create(
        cart=cart,
        product=product
    )
    if not created:
        cart_product.quantity += 1
        cart_product.save()
    return redirect('cart:cart')

@login_required
def delete_cart_product(request, item_slug):
    cart_product = CartProduct.objects.get(
        cart=Cart.objects.get(user=request.user),
        product=get_object_or_404(Product, slug=item_slug)
    )
    cart_product.delete()
    return redirect('cart:cart')

@login_required
def update_cart_product(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_product_id = request.POST.get('cart_product_id')
        new_quantity = int(request.POST.get('new_quantity'))
        cart_id = int(request.POST.get('cart_id'))

        cart = Cart.objects.get(pk=cart_id)
        cart_product = get_object_or_404(CartProduct, id=cart_product_id, cart=cart)
        cart_product.quantity = new_quantity
        cart_product.save()
        return JsonResponse({
            'success': True,
            'cart_product_id': cart_product.id,
            'cart_product_quantity': cart_product.quantity,
            'cart_product_total_price': float(cart_product.total_price()),
            'cart_total_price': float(cart.total_price)
        })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Invalid request method'
        })
