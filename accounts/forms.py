from django import forms
from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User

class UserCacheMixin:
    user_cache = None

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).exists()
        if user:
            raise ValidationError(('You can not use this email address.'))

        return email


class ChangeProfileForm(forms.Form):
    username = forms.CharField(label='User name', max_length=30, required=False, disabled=True)
    email = forms.CharField(label='Email', max_length=30, required=False, disabled=True)
    first_name = forms.CharField(label='First name', max_length=30, required=False)
    last_name = forms.CharField(label= 'Last name', max_length=150, required=False)
    birthday = forms.CharField(label= 'Birthday', required=False, widget= forms.DateInput(attrs={'type':'date'}))

class RestorePasswordForm(UserCacheMixin, forms.Form):
    email = forms.EmailField(label='Email')

    def clean_email(self):
        email = self.cleaned_data['email']

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError('You entered an invalid email address.')

        if not user.is_active:
            raise ValidationError('This account is not active.')

        self.user_cache = user

        return email

class RestorePasswordResetConfirmForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ["password1", "password2"]