from django import forms
from .models import Cargo

class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['cargo_name', 'importer_name', 'arrival_date', 'total_cost', 'amount_paid', 'storage_location', 'notes']
        widgets = {
            'cargo_name': forms.TextInput(attrs={'class': 'form-class', 'placeholder': 'Enter cargo name'}),
            'importer_name': forms.TextInput(attrs={'class': 'form-class', 'placeholder': 'Enter importer name'}),
            'arrival_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-class'}),
            'total_cost': forms.NumberInput(attrs={'class': 'form-class', 'placeholder': 'Enter total cost'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-class', 'placeholder': 'Enter amount paid'}),
            'storage_location': forms.TextInput(attrs={'class': 'form-class', 'placeholder': 'Enter storage location'}),
            'notes': forms.Textarea(attrs={'class': 'form-class', 'rows': 3, 'placeholder': 'Additional notes'}),
        }
