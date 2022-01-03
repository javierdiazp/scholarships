from django.urls import path

from accounts import views

urlpatterns = [
    path('reset_password/', views.ResetPasswordRequestToken.as_view(), name='reset_password'),
    path('reset_password/confirm/', views.ResetPasswordConfirm.as_view(), name='reset_password_confirm'),
    path('reset_password/validate_token/', views.ResetPasswordValidateToken.as_view(),
         name='reset_password_validate_token'),
    path('update_password/', views.UpdatePasswordAPIView.as_view(), name='update_password'),
    path('register_candidate/', views.CandidateCreateAPIView.as_view(), name='register_candidate'),
]
