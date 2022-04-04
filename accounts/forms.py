from enum import unique
from django.contrib.auth.forms import UserCreationForm
from django import forms
# from django.contrib.auth.models import User
from .models import User

####
from .tasks import send_mail
from django.contrib.auth.forms import PasswordResetForm as PasswordResetFormCore
####
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


####################

class PasswordResetForm(PasswordResetFormCore):
    pass
    # email = forms.EmailField(max_length=254, widget=forms.TextInput(
    #     attrs={
    #         # 'class': 'form-control',
    #         'id': 'email',
    #         'placeholder': 'Email'
    #     }
    # ))

    # def send_mail(self, subject_template_name, email_template_name, context, 
    #               from_email, to_email, html_email_template_name=None):
    #     context['user'] = context['user']

    #     send_mail.delay(subject_template_name=subject_template_name, 
    #                     email_template_name=email_template_name,
    #                     context=context, from_email=from_email, to_email=to_email,
    #                     html_email_template_name=html_email_template_name)


class ProfileUserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','hide_email','profile_pic']