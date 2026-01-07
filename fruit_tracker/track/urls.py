from django.urls import path
from .views import (
     add_tracker_event,
     get_batch_history,
    list_all_tracking
)

urlpatterns = [
    path("track/", add_tracker_event),
    path("track/<str:batch_id>/", get_batch_history),    
    path("track/all/", list_all_tracking),        
]                       