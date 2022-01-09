from django.urls import include, path
from rest_framework.routers import DefaultRouter

from rooms import views

router = DefaultRouter()
router.register(r'', views.DocumentViewSet, basename='document')

urlpatterns = [
    path('', views.RoomListAPIView.as_view()),
    path('<uuid:room_id>/documents/', include(router.urls)),
]
