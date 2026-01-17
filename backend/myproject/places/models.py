from django.db import models

# Create your models here.
class Place(models.Model):
    #CHOICES FOR MOOD FIELD
    MOOD_CHOICES=[
        ('relax','Relax'),
        ('adventure','Adventure'),
        ('food','Food'),
        ('nature','Nature'),
        ('socialize','Socialize'),
        ('shopping','Shopping'),
    ]
    #CHOICES FOR WEATHER FIELD
    WEATHER_CHOICES=[
        ('sunny','Sunny'),
        ('cloudy','Cloudy'),
        ('rainy','Rainy'),
    ]
    #CHOICES FOR CITY FIELD
    CITY_CHOICES=[
        ('butwal','Butwal'),
        ('pokhara','Pokhara'),
        ('kathmandu','Kathmandu'),
        ('bhaktapur','Bhaktapur'),
        ('lalitpur','Lalitpur'),
    ]
    
    # Place info
    name=models.CharField(max_length=200)
    description=models.TextField()
    city=models.CharField(max_length=50,choices=CITY_CHOICES,default='kathmandu')
    
    # LOCATION INFO
    latitude=models.FloatField(null=True,blank=True)
    longitude=models.FloatField(null=True,blank=True)
    
    # Moods Category
    primaryMood=models.CharField(max_length=50,choices=MOOD_CHOICES,default='relax')
    secondaryMood=models.CharField(max_length=50,choices=MOOD_CHOICES,default='nature',blank=True)
    tertiaryMood=models.CharField(max_length=50,choices=MOOD_CHOICES,default='food',blank=True)
    quaternaryMood=models.CharField(max_length=50,choices=MOOD_CHOICES,default='adventure',blank=True)
    
    # suitable weather
    primaryWeather=models.CharField(max_length=50,choices=WEATHER_CHOICES,default='sunny')
    secondaryWeather=models.CharField(max_length=50,choices=WEATHER_CHOICES,default='cloudy',blank=True)
    
    # place Rating
    rating=models.FloatField(default=0.0)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name