from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'full_name']

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        confirm_password = self.cleaned_data['password2']
        if password1 and confirm_password and password1 != confirm_password:
            raise ValidationError('password must match')
        return confirm_password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='you cant change password! using <a href="../password/">This form</a>')

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'full_name', 'password', 'last_login']
