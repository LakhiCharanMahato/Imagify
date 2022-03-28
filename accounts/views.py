import threading
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from .models import User
from django.core.mail import EmailMessage
from django.conf import settings

from .tasks import send_verification_emailid

# Create your views here.
# class EmailThread(threading.Thread):
#     def __init__(self,email):
#         self.email=email
#         threading.Thread.__init__(self)

#     def run(self):
#         self.email.send()




def send_verification_email(user,request):
    current_site=get_current_site(request)
    email_subject='Activate your account'
    email_body= render_to_string("accounts/activate.html",{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':generate_token.make_token(user)
    })

    # email=EmailMessage(subject=email_subject,body=email_body,
    #         from_email=settings.EMAIL_HOST_USER,
    #         to=[user.email]
    #         )
    # email.send()
    # print(settings.EMAIL_HOST_USER,type(settings.EMAIL_HOST_USER))
    # print(EMAIL_HOST_USER,type(EMAIL_HOST_USER))    
    from_email=settings.EMAIL_HOST_USER
    empass=settings.EMAIL_HOST_PASSWORD

    send_verification_emailid.delay(email_subject,email_body,
        from_email,empass,to=user.email)

    # return email

#     EmailThread(email).start()
    # email.send()

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()

            ###########
            if not user.is_email_verified:
                return render(request,"accounts/login.html",{"form":form,"erroremail":"Email is not verified, please check your email inbox."})


            ###########
            login(request,user)
            return redirect('/')
    else:
        form=AuthenticationForm(request)
    context={
        "form":form
    }
    return render(request,"accounts/login.html",context)

def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    if request.method=="POST":
        logout(request)
        return redirect("/login/")
    return render(request,"accounts/logout.html",{})

def register_view(request):
    if request.user.is_authenticated:
        return redirect("/")
    form=CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj=form.save()

        #############
        # print("Lakhi")
        # print(user_obj)
        # senddata={
        #     'user':user_obj.username,
        #     'pk':user_obj.pk,
        #     'email':user_obj.email,
        # }
        send_verification_email(user_obj,request)

        # send_verification_emailid.delay(email,request)


        ################

        return redirect('/verification_mail')

    context={
        "form":form
    }
    return render(request,"accounts/register.html",context)



def activate_user(request,uidb64,token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except Exception as e:
        user=None
    if user and generate_token.check_token(user,token):
        user.is_email_verified=True
        user.save()

        # return redirect('/login')
        return redirect('/verification_success')

    return render(request,'accounts/activate-failed.html',{"user":user})

def verification_view(request):
    return render(request,'accounts/verification_mail.html',{})

def verification_success_view(request):
    return render(request,'accounts/verification_success.html',{})