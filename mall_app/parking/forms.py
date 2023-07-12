from django import forms
from .models import CustomerCar


class CustomerCarForm(forms.ModelForm):
    class Meta:
        model = CustomerCar
        fields = ['license_plate', 'car_type']



class CarEntryForm(forms.Form):
    license_plate = forms.CharField(label='License Plate', max_length=10)
