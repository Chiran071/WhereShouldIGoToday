"""
Image Service - Fetches REAL images from Google Places API
"""
import os
import requests
from functools import lru_cache

# Google Places API - Get key at https://console.cloud.google.com/
GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY', '')


@lru_cache(maxsize=100)
def fetch_google_place_image(place_name: str, city: str) -> str:
    """
    Fetch a REAL photo from Google Places API.
    This returns actual photos of the location taken by visitors.
    """
    if not GOOGLE_PLACES_API_KEY:
        print("Warning: GOOGLE_PLACES_API_KEY not set")
        return ""
    
    try:
        # Step 1: Search for the place to get place_id
        search_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        search_params = {
            "input": f"{place_name} {city} Nepal",
            "inputtype": "textquery",
            "fields": "place_id,name,photos",
            "key": GOOGLE_PLACES_API_KEY
        }
        
        response = requests.get(search_url, params=search_params, timeout=10)
        
        if response.status_code != 200:
            print(f"Google Places search failed: {response.status_code}")
            return ""
        
        data = response.json()
        
        if data.get("status") != "OK" or not data.get("candidates"):
            # Try without city name
            search_params["input"] = f"{place_name} Nepal"
            response = requests.get(search_url, params=search_params, timeout=10)
            data = response.json()
            
            if data.get("status") != "OK" or not data.get("candidates"):
                print(f"No place found for: {place_name}")
                return ""
        
        candidate = data["candidates"][0]
        
        # Check if place has photos
        if "photos" not in candidate or not candidate["photos"]:
            print(f"No photos for: {place_name}")
            return ""
        
        # Step 2: Get the photo using photo_reference
        photo_reference = candidate["photos"][0]["photo_reference"]
        
        # Return the Google Places Photo URL
        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photo_reference={photo_reference}&key={GOOGLE_PLACES_API_KEY}"
        
        return photo_url
        
    except Exception as e:
        print(f"Google Places API error: {e}")
        return ""


def get_place_image(place_name: str, city: str, mood: str) -> str:
    """
    Get the real image for a place from Google Places API.
    """
    # Fetch real photo from Google
    image_url = fetch_google_place_image(place_name, city)
    
    if image_url:
        return image_url
    
    # Try with simplified name (remove parentheses content)
    simple_name = place_name.split('(')[0].strip()
    if simple_name != place_name:
        image_url = fetch_google_place_image(simple_name, city)
        if image_url:
            return image_url
    
    return ""
