from django import forms
from .models import Sweet

class SweetForm(forms.ModelForm):
    class Meta:
        model = Sweet
        fields = ['name', 'category', 'price', 'quantity']
