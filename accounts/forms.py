from enum import unique
from django.contrib.auth.forms import UserCreationForm
from django import forms
# from django.contrib.auth.models import User
from .models import User
class CustomUserCreationForm(UserCreationForm):
    email=forms.EmailField(label='Email address',required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # for fieldname in ['username', 'password1', 'password2']:
        #   self.fields[fieldname].help_text = None

        # new_data={
        #     'class':'form-controller'
        # }

        # for field in self.fields:
        #     self.fields[str(field)].widget.attrs.update(new_data)

        # self.fields['email'].widget.attrs.update({'class':"container"})

    def clean_password1(self):
        password1=self.cleaned_data.get("password1")
        # password2=self.cleaned_data.get("password2")
        contains_digit=any(map(str.isdigit,password1))
        if not contains_digit:
            self.add_error("password2","Password must contain digit")
        return password1

    def clean_email(self):
        email=self.cleaned_data.get("email")
        users=User.objects.all()
        if email in users.values_list('email',flat=True):
            self.add_error("email","Email is already taken")
        return email
