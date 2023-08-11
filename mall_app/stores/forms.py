from django import forms
from .models import StoreCategory

class StoreSearchForm(forms.Form):
    search_term = forms.CharField(required=False)
    category = forms.ModelChoiceField(queryset=StoreCategory.objects.all(), required=False)
