"""
Django Realtime Chat & Notifications
"""
## @package users.urls
#
# Urls de la aplicación participacion
# @version 1.0
from django.urls import path, reverse_lazy
from .views import *
from .forms import PasswordResetForm
from users import views
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
	)

app_name = 'users'
urlpatterns = [
    path('login', LoginView.as_view(), name = "login"),
    path('logout', LogoutView.as_view(), name = "logout"),
    path('register', RegisterView.as_view(), name = "register"),
    path('account/password/reset/', PasswordResetView.as_view(
    								template_name='user.reset.html',
    								success_url=reverse_lazy('users:reset_done'),
    								form_class=PasswordResetForm),
    	name='forgot'),
    path('accounts/password/done/', PasswordResetDoneView.as_view(
    							   template_name='user.passwordreset.done.html'),
        name='reset_done'),
    path('account/change-pass/', ChangePasswordView.as_view(), name="change_pass"),
]
