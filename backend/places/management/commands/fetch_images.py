"""
Management command to fetch REAL images from Google Places API 
and update all places in the database.
"""
from django.core.management.base import BaseCommand
from places.models import Place
from places.image_service import fetch_google_place_image
import os


class Command(BaseCommand):
    help = 'Fetch real images from Google Places API for all places'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update even if image_url already exists',
        )

    def handle(self, *args, **options):
        api_key = os.environ.get('GOOGLE_PLACES_API_KEY', '')
        if not api_key:
            self.stdout.write(self.style.ERROR(
                "GOOGLE_PLACES_API_KEY not set!\n"
                "Get your key at: https://console.cloud.google.com/\n"
                "1. Create/select project\n"
                "2. Enable 'Places API'\n"
                "3. Create API Key\n"
                "4. Add to backend/.env file"
            ))
            return
            
        force = options['force']
        places = Place.objects.all()
        updated = 0
        failed = 0

        self.stdout.write(f"Processing {places.count()} places with Google Places API...")
        self.stdout.write("This fetches REAL photos of actual locations!\n")

        for place in places:
            # Skip if already has image and not forcing
            if place.image_url and not force:
                self.stdout.write(f"  Skipping {place.name} (already has image)")
                continue

            self.stdout.write(f"  Fetching real photo for: {place.name}...")
            
            image_url = fetch_google_place_image(place.name, place.city)
            
            if image_url:
                place.image_url = image_url
                place.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f"    ✓ Got real photo: {place.name}"))
            else:
                failed += 1
                self.stdout.write(self.style.WARNING(f"    ✗ No photo found: {place.name}"))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Updated {updated} places with real photos"))
        if failed:
            self.stdout.write(self.style.WARNING(f"No photos found for {failed} places"))
