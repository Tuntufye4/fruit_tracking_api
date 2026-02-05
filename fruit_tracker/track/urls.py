from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrackerViewSet

router = DefaultRouter()
router.register(r'track', TrackerViewSet, basename='track')

urlpatterns = [
    path('', include(router.urls)),
]
               