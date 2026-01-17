from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Place
from .serializers import (
    PlaceSerializer,
    RecommendationRequestSerializer,
    RecommendationResponseSerializer
)
from .scoring import engine, UserPreferences


class RecommendationsView(APIView):
    """
    POST /api/recommendations/
    
    Get personalized place recommendations based on user preferences.
    Returns top 3 places with scores and explanations.
    """
    
    def post(self, request):
        # Validate input
        serializer = RecommendationRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        # Create user preferences object
        prefs = UserPreferences(
            mood=data['mood'],
            budget=data['budget'],
            time_available=data['time_available'],
            weather_preference=data.get('weather_preference', 'any'),
            city=data.get('city', 'kathmandu')
        )
        
        # Get all places
        places = Place.objects.all()
        
        if not places.exists():
            return Response({
                'message': 'No places in database. Run: python manage.py loaddata places',
                'recommendations': []
            })
        
        # Get recommendations from scoring engine
        recommendations = engine.get_recommendations(places, prefs, top_n=3)
        
        # Serialize response
        response_data = []
        for rec in recommendations:
            rec_dict = {
                'place': PlaceSerializer(rec.place).data,
                'total_score': rec.total_score,
                'mood_score': rec.mood_score,
                'budget_score': rec.budget_score,
                'time_score': rec.time_score,
                'weather_score': rec.weather_score,
                'rating_score': rec.rating_score,
                'explanation': rec.explanation,
                'match_reasons': rec.match_reasons,
                'budget_range': f"₹{rec.place.min_budget} - ₹{rec.place.max_budget}",
                'time_range': f"{rec.place.min_time_hours}-{rec.place.max_time_hours}h",
                'weather_suitable': self._get_weather_text(rec.place.primary_weather)
            }
            response_data.append(rec_dict)
        
        return Response({
            'recommendations': response_data,
            'user_input': data,
            'total_places_considered': places.count()
        })
    
    def _get_weather_text(self, weather):
        if weather == 'rainy':
            return "🌧️ Great for rainy days"
        elif weather == 'sunny':
            return "☀️ Best on sunny days"
        return "☁️ Good for cloudy days"


class PlacesListView(APIView):
    """
    GET /api/places/
    
    List all places in the database.
    """
    
    def get(self, request):
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        return Response({
            'places': serializer.data,
            'count': places.count()
        })


class PlaceDetailView(APIView):
    """
    GET /api/places/<id>/
    
    Get details of a specific place.
    """
    
    def get(self, request, pk):
        try:
            place = Place.objects.get(pk=pk)
        except Place.DoesNotExist:
            return Response(
                {'error': 'Place not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = PlaceSerializer(place)
        return Response(serializer.data)


@api_view(['GET'])
def health_check(request):
    """
    GET /api/health/
    
    Health check endpoint for the API.
    """
    place_count = Place.objects.count()
    return Response({
        'status': 'healthy',
        'service': 'Where To Go Today API',
        'places_count': place_count,
        'message': 'API is running!' if place_count > 0 else 'API running but no places loaded'
    })


@api_view(['GET'])
def get_options(request):
    """
    GET /api/options/
    
    Get available options for the form dropdowns.
    """
    return Response({
        'moods': [
            {'value': 'relax', 'label': '😌 Relax', 'description': 'Unwind and de-stress'},
            {'value': 'adventure', 'label': '🏔️ Adventure', 'description': 'Excitement and thrills'},
            {'value': 'food', 'label': '🍜 Food', 'description': 'Culinary experiences'},
            {'value': 'nature', 'label': '🌿 Nature', 'description': 'Connect with outdoors'},
            {'value': 'socialize', 'label': '👥 Socialize', 'description': 'Meet people, hangout'},
            {'value': 'shopping', 'label': '🛍️ Shopping', 'description': 'Retail therapy'},
        ],
        'weathers': [
            {'value': 'any', 'label': '🌤️ Any Weather', 'description': 'No preference'},
            {'value': 'sunny', 'label': '☀️ Sunny', 'description': 'Clear sunny day'},
            {'value': 'cloudy', 'label': '☁️ Cloudy', 'description': 'Overcast weather'},
            {'value': 'rainy', 'label': '🌧️ Rainy', 'description': 'Rainy day activities'},
        ],
        'cities': [
            {'value': 'kathmandu', 'label': 'Kathmandu'},
            {'value': 'lalitpur', 'label': 'Lalitpur (Patan)'},
            {'value': 'bhaktapur', 'label': 'Bhaktapur'},
            {'value': 'pokhara', 'label': 'Pokhara'},
            {'value': 'butwal', 'label': 'Butwal'},
            {'value': 'any', 'label': 'Any Location'},
        ],
        'budget_presets': [
            {'value': 500, 'label': 'Budget (₹500)'},
            {'value': 1500, 'label': 'Moderate (₹1,500)'},
            {'value': 3000, 'label': 'Comfortable (₹3,000)'},
            {'value': 5000, 'label': 'Premium (₹5,000+)'},
        ],
        'time_presets': [
            {'value': 1, 'label': '1 hour'},
            {'value': 2, 'label': '2 hours'},
            {'value': 3, 'label': 'Half day (3-4h)'},
            {'value': 6, 'label': 'Full day (6h+)'},
        ]
    })
