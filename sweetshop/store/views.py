from django.shortcuts import render, redirect, get_object_or_404
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

# Delete Sweet
def delete_sweet(request, sweet_id):
    sweet = get_object_or_404(Sweet, id=sweet_id)
    sweet.delete()
    return redirect('sweet_list')
