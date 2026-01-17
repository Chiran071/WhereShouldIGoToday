from django.urls import path
from .views import (
    RecommendationsView,
    PlacesListView,
    PlaceDetailView,
    health_check,
    get_options
)

urlpatterns = [
    # Main recommendation endpoint
    path('recommendations/', RecommendationsView.as_view(), name='recommendations'),
    
    # Places CRUD
    path('places/', PlacesListView.as_view(), name='places-list'),
    path('places/<int:pk>/', PlaceDetailView.as_view(), name='place-detail'),
    
    # Utility endpoints
    path('health/', health_check, name='health-check'),
    path('options/', get_options, name='options'),
]
