from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .models import Category, Product
from .forms import ProductForm, ProductImageFormSet

def index_view(request):
    return render(request, 'shop/index.html', {
        'current_datetime': timezone.now().strftime('%d %B %Y, %H:%M %Z')
    })


def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()
    if query:
        products = products.filter(
            Q(name__icontains=query)
        )
    return render(request, 'shop/product_list.html', {
        'query': query,
        'products': products
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})


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
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно обновлен.')
            return redirect('shop:product_list')
        else:
            messages.error(request, 'Исправьте ошибки в форме')
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_form.html', {
        'product': product,
        'form': form,
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

