from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Sweet
from .forms import SweetForm

# Create your views here.


def sweet_list(request):
    sweets = Sweet.objects.all()
    form = SweetForm()  # ← ADD THIS
    return render(request, 'index.html', {
        'sweets': sweets,
        'form': form  
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
