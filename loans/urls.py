from rest_framework.routers import DefaultRouter

from loans.views import LoanViewSet

router = DefaultRouter()
router.register(r'', LoanViewSet, basename='loan')
urlpatterns = router.urls
