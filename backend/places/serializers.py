from rest_framework import serializers
from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    """Serializer for Place model."""
    
    primary_weather_display = serializers.CharField(source='get_primary_weather_display', read_only=True)
    mood_display = serializers.CharField(source='get_primary_mood_display', read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Place
        fields = [
            'id', 'name', 'description', 'city',
            'latitude', 'longitude',
            'primary_mood', 'secondary_mood', 'tertiary_mood', 'quaternary_mood', 'mood_display',
            'min_budget', 'max_budget',
            'min_time_hours', 'max_time_hours',
            'primary_weather', 'secondary_weather', 'primary_weather_display',
            'image', 'image_url', 'google_maps_url',
            'rating'
        ]
    
    def get_image_url(self, obj):
        """Return the full URL for the image if it exists."""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            # Fallback if no request context - use localhost
            return f"http://localhost:8000{obj.image.url}"
        return None


class RecommendationRequestSerializer(serializers.Serializer):
    """Serializer for recommendation request."""
    
    mood = serializers.ChoiceField(choices=[
        'relax', 'adventure', 'food', 'nature', 'socialize', 'shopping'
    ])
    budget = serializers.IntegerField(min_value=0, max_value=100000)
    time_available = serializers.FloatField(min_value=0.5, max_value=24)
    weather_preference = serializers.ChoiceField(
        choices=['sunny', 'cloudy', 'rainy', 'any'],
        default='any'
    )
    city = serializers.ChoiceField(
        choices=['kathmandu', 'pokhara', 'bhaktapur', 'lalitpur', 'butwal', 'any'],
        default='kathmandu'
    )


class RecommendationResponseSerializer(serializers.Serializer):
    """Serializer for a single recommendation."""
    
    place = PlaceSerializer()
    total_score = serializers.FloatField()
    mood_score = serializers.FloatField()
    budget_score = serializers.FloatField()
    time_score = serializers.FloatField()
    weather_score = serializers.FloatField()
    rating_score = serializers.FloatField()
    explanation = serializers.CharField()
    match_reasons = serializers.ListField(child=serializers.CharField())
    
    # Computed fields for frontend
    budget_range = serializers.SerializerMethodField()
    time_range = serializers.SerializerMethodField()
    weather_suitable = serializers.SerializerMethodField()
    
    def get_budget_range(self, obj):
        place = obj.place
        return f"₹{place.min_budget} - ₹{place.max_budget}"
    
    def get_time_range(self, obj):
        place = obj.place
        if place.min_time_hours == place.max_time_hours:
            return f"{place.min_time_hours}h"
        return f"{place.min_time_hours}-{place.max_time_hours}h"
    
    def get_weather_suitable(self, obj):
        weather = obj.place.primary_weather
        if weather == 'rainy':
            return "🌧️ Great for rainy days"
        elif weather == 'sunny':
            return "☀️ Best on sunny days"
        return "☁️ Good for cloudy days"
