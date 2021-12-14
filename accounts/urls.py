from django.urls import path

from accounts.views import ResetPasswordRequestToken, ResetPasswordConfirm, ResetPasswordValidateToken

urlpatterns = [
    path('reset_password/', ResetPasswordRequestToken.as_view(), name='reset_password'),
    path('reset_password/confirm/', ResetPasswordConfirm.as_view(), name='reset_password_confirm'),
    path('reset_password/validate_token/', ResetPasswordValidateToken.as_view(), name='reset_password_validate_token'),
]
