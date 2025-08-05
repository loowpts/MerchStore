from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .models import Category, Product, Size, ProductSize
from .forms import ProductForm, ProductImageFormSet, AddToCartForm

def index_view(request):
    return render(request, 'shop/index.html', {
        'current_datetime': timezone.now().strftime('%d %B %Y, %H:%M %Z')
    })

def product_list(request):
    query = request.GET.get('q', '')
    size_id = request.GET.get('size')
    products = Product.objects.filter(available=True)
    sizes = Size.objects.filter(productsize__quantity__gt=0).distinct()
    selected_size = None

    if query:
        products = products.filter(Q(name__icontains=query))
    
    if size_id:
        products = products.filter(product_sizes__size_id=size_id)
        selected_size = int(size_id)


    return render(request, 'shop/product_list.html', {
        'query': query,
        'products': products,
        'sizes': sizes,
        'selected_size': selected_size
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    form = AddToCartForm(product=product)
    if request.method == 'POST':
        form = AddToCartForm(request.POST, product=product)
        if form.is_valid():
            size = form.cleaned_data['size']
            quantity = form.cleaned_data['quantity']
            product_size = get_object_or_404(ProductSize, product=product, size=size)
            if product_size.quantity < quantity:
                messages.error(request, f'Недостаточно товара {product.name} ({size.name}) на складе.')
                return redirect('shop:product_detail', slug=slug)
            return redirect('cart:add_to_cart', item_slug=slug, size_id=size.id, quantity=quantity)
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'form': form
    })

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=Product())
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            formset.instance = product
            formset.save()
            messages.success(request, 'Продукт успешно создан.')
            return redirect('shop:product_list')
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = ProductForm()
        formset = ProductImageFormSet(instance=Product())
    return render(request, 'shop/product_form.html', {
        'form': form,
        'formset': formset,
        'title': 'Добавить товар'
    })

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Товар успешно обновлен.')
            return redirect('shop:product_list')
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(instance=product)
    return render(request, 'shop/product_form.html', {
        'product': product,
        'form': form,
        'formset': formset,
        'title': 'Редактировать товар'
    })

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Товар удален.')
        return redirect('shop:product_list')
    return render(request, 'shop/product_confirm_delete.html', {'product': product})
