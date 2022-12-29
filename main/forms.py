from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ["first_name", "last_name", "email",
                  "birthday", "nationality", "grade"]
        widgets = {'birthday': forms.DateInput(attrs={'type':'date'})}
        
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['nationality'].required = False