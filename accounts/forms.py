from django.contrib.auth.forms import UserCreationForm
from django import forms
class CustomUserCreationForm(UserCreationForm):
    def clean_password1(self):
        password1=self.cleaned_data.get("password1")
        # password2=self.cleaned_data.get("password2")
        contains_digit=any(map(str.isdigit,password1))
        if not contains_digit:
            raise forms.ValidationError("Password must contain digit")
        return password1
