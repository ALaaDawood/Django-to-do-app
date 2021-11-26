from django import forms
from django.contrib.auth import get_user_model
from django.db.models.base import Model
from django.forms import fields
from user.models import User

User = get_user_model()


class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email", "password"]

    def clean_email(self):
        """
        Verify email is available.
        """
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email=email)
        if qs.exists():
            self.add_error("email", "email is taken")
        return email

    def clean(self):
        """
        Verify both passwords match.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and password != confirm_password:
            self.add_error("confirm_password", "Your passwords must match")
        return cleaned_data


class LoginForm(forms.Form):
    class Meta:
        model = User
        fields = ["email", "password"]

    email = forms.CharField(max_length=63, widget=forms.EmailInput)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)
