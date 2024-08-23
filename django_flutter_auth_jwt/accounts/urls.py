from django.urls import path
from .views import *

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register-page"),
    path("verify-email/", UserVerifyEmailView.as_view(), name="verify-email-page"),
    path("verify-email-code/", verify_email_code, name="verify-email-code-page"),
    path("login/", UserLoginView.as_view(), name="login-page"),
    path("profile/", TestAuthenticationView.as_view(), name="granted-page"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset-page"),
    # path("pssword-reset-request/", password_reset_request, name="pssword-reset-request"),
    path("pssword-reset-request/<str:email>/", password_reset_request, name="password-reset-request-page"), 
    path("password-reset-confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password-reset-confirm-page"),
    path("set-new-password/", SetNewPasswordView.as_view(), name="set-new-password-page"),
    path("logout/", LogoutUserView.as_view(), name="logout-page"),
   
]
