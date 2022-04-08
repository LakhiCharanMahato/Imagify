"""Imagify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from .views import home_view
from django.contrib.auth import views as auth_views
from accounts.views import (
    login_view,
    logout_view,
    register_view,
    activate_user,
    verification_view,
    verification_success_view,
    password_reset_view,
    account_view,
    update_profile_view
)
from ladders.views import (
    upload_view,
    gallery_view,
    detail_view,
    update_view
)

from friends.views import (
    friends_finder_view,
    friend_request_received_view,
    my_friends_all_view
)
urlpatterns = [
    path('',home_view),
    path('gallery/<int:id>/',detail_view),
    path('gallery/<int:id>/edit/',update_view),
    path('admin/', admin.site.urls),
    path('login/',login_view),
    path('logout/',logout_view),
    path('register/',register_view),
    path('upload/',upload_view),
    path('gallery/',gallery_view),

    # path('reset_password/',
    #     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
    #     name="reset_password"),
    path('reset_password/',
        password_reset_view,
        name="reset_password"),
    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
        name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
        name="password_reset_confirm"),
    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_complete"),

    path('activate-user/<uidb64>/<token>/',activate_user,name='activate'),

    path('verification_mail/',verification_view),
    path('verification_success/',verification_success_view),

    path('profile/<user_id>/',account_view,name="profile_view"),
    path('profile/<user_id>/update',update_profile_view,name="profile_view"),

    path('friends/people',friends_finder_view),
    path('friends/requests',friend_request_received_view),
    path('friends/all',my_friends_all_view)

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)