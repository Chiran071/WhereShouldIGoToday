from django.db import models


class Place(models.Model):
    """
    Model representing a place/destination in Nepal.
    Static dataset for hackathon demo.
    """
    MOOD_CHOICES = [
        ('relax', 'Relax'),
        ('adventure', 'Adventure'),
        ('food', 'Food'),
        ('nature', 'Nature'),
        ('socialize', 'Socialize'),
        ('shopping', 'Shopping'),
    ]
    
    WEATHER_CHOICES = [
        ('sunny', 'Sunny'),
        ('cloudy', 'Cloudy'),
        ('rainy', 'Rainy'),
    ]
    
    CITY_CHOICES = [
        ('kathmandu', 'Kathmandu'),
        ('pokhara', 'Pokhara'),
        ('bhaktapur', 'Bhaktapur'),
        ('lalitpur', 'Lalitpur'),
        ('butwal', 'Butwal'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    city = models.CharField(max_length=50, choices=CITY_CHOICES, default='kathmandu')
    
    # Location for map display (static coordinates)
    latitude = models.FloatField(blank=True,null=True)
    longitude = models.FloatField(blank=True,null=True)
    
    # Scoring factors - Moods (4 levels)
    primary_mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    secondary_mood = models.CharField(max_length=20, choices=MOOD_CHOICES, blank=True, null=True)
    tertiary_mood = models.CharField(max_length=20, choices=MOOD_CHOICES, blank=True, null=True)
    quaternary_mood = models.CharField(max_length=20, choices=MOOD_CHOICES, blank=True, null=True)
    
    min_budget = models.IntegerField(help_text="Minimum budget in NPR")
    max_budget = models.IntegerField(help_text="Maximum budget in NPR")
    
    min_time_hours = models.FloatField(help_text="Minimum time needed in hours")
    max_time_hours = models.FloatField(help_text="Maximum time for a visit in hours")
    
    # Weather suitability (primary and secondary)
    primary_weather = models.CharField(max_length=10, choices=WEATHER_CHOICES, default='sunny')
    secondary_weather = models.CharField(max_length=10, choices=WEATHER_CHOICES, blank=True, null=True)
    
    # Display info
    image = models.ImageField(upload_to='places/', blank=True, null=True)
    google_maps_url = models.URLField(blank=True, null=True)
    
    # For scoring weight (popularity/quality factor 1-10)
    rating = models.FloatField(default=5.0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.city})"

    class Meta:
        ordering = ['name']
