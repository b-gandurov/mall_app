from django import forms
from .models import CustomerCar


class CustomerCarForm(forms.ModelForm):
    code = forms.CharField(max_length=12, label='12-digit Code')
    class Meta:
        model = CustomerCar
        fields = ['license_plate', 'code']


class CarEntryForm(forms.Form):
    license_plate = forms.CharField(label='License Plate', max_length=10)
