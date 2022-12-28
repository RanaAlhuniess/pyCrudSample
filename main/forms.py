from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    # grade2 = forms.ModelChoiceField(CustomerGrade.objects.all().values_list('id', 'country'),
    #  widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "email","birthday","grade"]