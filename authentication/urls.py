from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import CustomPasswordResetForm
from . import views

urlpatterns = [
    path("login/", views.login_user, name="login_user"),
    path("signup/", views.signup, name="signup"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', views.password_reset_request, name="password-reset"),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password-reset-done.html'), 
            name='password-reset-done'),
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password-reset-confirm.html'), 
            name='password-reset-confirm'),
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password-reset-complete.html'), 
            name='password-reset-complete'),
]
