from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  

class SignUpForm(UserCreationForm):
    """Custom signup form for CustomUser model."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"placeholder": "Your email address", "class": "form-control"}),
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"}),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password", "class": "form-control"}),
        label="Confirm Password"
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data
