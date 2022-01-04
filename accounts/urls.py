from django.urls import path
from rest_framework_simplejwt import views as token_views

from accounts import views

urlpatterns = [
    path('token/', token_views.TokenObtainPairView.as_view()),
    path('token/refresh/', token_views.TokenRefreshView.as_view()),
    path('token/verify/', token_views.TokenVerifyView.as_view(), name='token_verify'),

    path('reset_password/', views.ResetPasswordRequestToken.as_view(), name='reset_password'),
    path('reset_password/confirm/', views.ResetPasswordConfirm.as_view(), name='reset_password_confirm'),
    path('reset_password/validate_token/', views.ResetPasswordValidateToken.as_view(),
         name='reset_password_validate_token'),

    path('update_password/', views.UpdatePasswordAPIView.as_view(), name='update_password'),
    path('register_candidate/', views.CandidateCreateAPIView.as_view(), name='register_candidate'),
]
