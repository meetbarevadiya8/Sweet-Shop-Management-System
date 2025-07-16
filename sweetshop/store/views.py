from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Sweet
from .forms import SweetForm

# Create your views here.

#Sweet List Show and Search Filters
def sweet_list(request):
    sweets = Sweet.objects.all()
    form = SweetForm()

    #  Search Filters
    name_query = request.GET.get('name', '')
    category_query = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    if name_query:
        sweets = sweets.filter(name__icontains=name_query)
    if category_query:
        sweets = sweets.filter(category__icontains=category_query)
    if min_price:
        sweets = sweets.filter(price__gte=min_price)
    if max_price:
        sweets = sweets.filter(price__lte=max_price)

    return render(request, 'index.html', {
        'sweets': sweets,
        'form': form,
        'filters': {
            'name': name_query,
            'category': category_query,
            'min_price': min_price,
            'max_price': max_price,
        }
    })

# Add Sweet
def add_sweet(request):
    if request.method == 'POST':
        form = SweetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sweet added successfully.")
        else:
            messages.error(request, "Error adding sweet.")
    return redirect('sweet_list')

## Delete Sweet

from django.db import connection, transaction

def delete_sweet(request, sweet_id):
    sweet = get_object_or_404(Sweet, id=sweet_id)
    sweet.delete()

    # If all sweets are deleted, reset auto-increment counter
    if not Sweet.objects.exists():
        with connection.cursor() as cursor:
            db_vendor = connection.vendor
            table_name = 'store_sweet'
            if db_vendor == 'sqlite':
                cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}'")
    return redirect('sweet_list')


# Buy Sweet
@csrf_exempt
def purchase_sweet(request):
    if request.method == 'POST':
        sweet_id = request.POST.get('sweet_id')
        quantity_to_buy = int(request.POST.get('quantity', 0))

        sweet = get_object_or_404(Sweet, id=sweet_id)

        if sweet.quantity >= quantity_to_buy:
            sweet.quantity -= quantity_to_buy
            sweet.save()
            messages.success(request, f"Purchased {quantity_to_buy} units of {sweet.name}.")
        else:
            messages.error(request, f"Only {sweet.quantity} units available of {sweet.name}.")
    return redirect('sweet_list')

# Restock Sweet
@csrf_exempt
def restock_sweet(request):
    if request.method == 'POST':
        sweet_id = request.POST.get('sweet_id')
        quantity_to_add = int(request.POST.get('quantity', 0))
        new_price = float(request.POST.get('price', 0))

        sweet = get_object_or_404(Sweet, id=sweet_id)

        sweet.quantity += quantity_to_add
        sweet.price = new_price
        sweet.save()

        messages.success(request, f"{sweet.name} restocked and price updated.")
    return redirect('sweet_list')
