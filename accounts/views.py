import email
from site import USER_SITE
import threading
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, PasswordResetForm, ProfileUserUpdateForm

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str, force_text, DjangoUnicodeDecodeError
from .utils import generate_token
from .models import User
from django.core.mail import EmailMessage, send_mail
from django.conf import settings

from .tasks import send_verification_emailid

from django.contrib.auth.tokens import default_token_generator

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

def password_reset_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    form=PasswordResetForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            # form.save(from_email=from_email)
            data=form.cleaned_data.get("email")
            user_email=User.objects.filter(email=data)
            if user_email.exists():
                user=user_email[0]
                subject="Password reset request"
                email_template_name='accounts/password_message.html'
                parameters={
                    'email':user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name':'Imagify',
                    'uid':urlsafe_base64_encode((force_bytes(user.pk))),
                    'token':default_token_generator.make_token(user),
                    'protocol':'http',
                    'user':user
                }
                email=render_to_string(email_template_name,parameters)
                try:
                    from_email=settings.EMAIL_HOST_USER
                    empass=settings.EMAIL_HOST_PASSWORD
                    send_verification_emailid.delay(subject,email,from_email,empass,user.email)
                    # send_mail(subject,email,'',[user.email],fail_silently=False)
                except:
                    pass
            # print(user_email,user_email.exists())
            # print(data,type(data))
            return redirect('/reset_password_sent/')
    return render(request,'accounts/password_reset.html',{'form':form})


def account_view(request,*args,**kwargs):
    """
    - Logic here is kind of tricky 
        is_self (boolean)
            is_friend (boolean)
                -1: NO_REQUEST_SENT
                0: THEM_SENT_TO_YOU
                1: YOU_SENT_TO_THEM
    """
    context={}
    user_id=kwargs.get("user_id")
    try:
        account=User.objects.get(pk=user_id)
    except:
        return HttpResponse("That user doesn't exist")

    if account:
        context['account']=account

        is_self=True
        is_friend=False
        user=request.user

        if user.is_authenticated and user!=account:
            is_self=False
        elif not user.is_authenticated:
            is_self=False

        context['is_self']=is_self
        context['is_friend']=is_friend
        # context['BASE_URL']=settings.BASE_URL

        return render(request,"accounts/profile.html",context)


def update_profile_view(request,*args,**kwargs):
    obj=get_object_or_404(User, id=request.user.id)
    form=ProfileUserUpdateForm(request.POST or None,instance=obj)
    context={
        'form':form,
        "object":obj
    }

    print("OKOK",request.FILES)
    if form.is_valid():
        if not request.user.profile_pic:
            instance=form.save(commit=False)
            instance.profile_pic=request.FILES['profile_pic']
            instance.save()
        else:
            if len(request.FILES)>0:
                instance=form.save(commit=False)
                instance.profile_pic=request.FILES['profile_pic']
                instance.save()
            else:
                form.save()
        context['message']='Data saved.'
    return render(request,'accounts/profileupdate.html',context)
