from rest_framework.routers import DefaultRouter
from .views import TrackerViewSet

router = DefaultRouter()

# IMPORTANT: empty prefix because 'track' is already in project urls
router.register(r'', TrackerViewSet, basename='track')

urlpatterns = router.urls
                    