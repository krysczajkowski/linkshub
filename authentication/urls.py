from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('validate-username',csrf_exempt(views.UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email', csrf_exempt(views.EmailValidationView.as_view()), name='validate-email'),
    path('validate-password', csrf_exempt(views.PasswordValidationView.as_view()), name='validate-password'),
    path('activate/<uidb64>/<token>', views.VerificationView.as_view(), name='activate'),
    path('set-new-password/<uidb64>/<token>', views.CompletePasswordReset.as_view(), name='reset-user-password'),
    path('reset-password/', views.RequestPasswordResetEmail.as_view(), name='request-password'),
    path('confirm-email', views.confirmEmail, name='confirm-email'),
    path('login/resend-activation-email', views.ResendActivationEmail.as_view(), name='resend-activation-email')
]
