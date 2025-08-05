from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from shop.models import Product, Size
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
def add_to_cart(request, item_slug, size_id, quantity):
    product = get_object_or_404(Product, slug=item_slug)
    size = get_object_or_404(Size, id=size_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_product, created = CartProduct.objects.get_or_create(
        cart=cart,
        product=product,
        size=size
    )
    if not created:
        cart_product.quantity += quantity
    else:
        cart_product.quantity = quantity
    cart_product.save()
    return redirect('cart:cart')

@login_required
def delete_cart_product(request, item_slug):
    product = get_object_or_404(Product, slug=item_slug)
    size_id = request.GET.get('size_id')
    size = get_object_or_404(Size, id=size_id) if size_id else None
    cart_product = CartProduct.objects.get(
        cart=Cart.objects.get(user=request.user),
        product=product,
        size=size
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
        product_size = get_object_or_404(ProductSize, product=cart_product.product, size=cart_product.size)
        if new_quantity > product_size.quantity:
            return JsonResponse({
                'success': False,
                'error': f'Недостаточно товара {cart_product.product.name} ({cart_product.size.name}) на складе.'
            })
        cart_product.quantity = new_quantity
        cart_product.save()
        return JsonResponse({
            'success': True,
            'cart_product_id': cart_product.id,
            'cart_product_quantity': cart_product.quantity,
            'cart_product_total_price': float(cart_product.total_price()),
            'cart_total_price': float(cart.total_price)
        })
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })
