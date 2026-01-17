import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wheretogo.settings")
django.setup()

from places.models import Place

# Find places with short descriptions (likely ".." or "...")
missing = Place.objects.filter(description__regex=r'^.{0,10}$')
print(f"Missing count: {missing.count()}")

with open("missing_places.txt", "w", encoding="utf-8") as f:
    for p in missing:
        print(p.name)
        f.write(p.name + "\n")
