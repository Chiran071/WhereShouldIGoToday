import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wheretogo.settings")
django.setup()

from places.models import Place

total = Place.objects.count()
# We consider a description "updated" if it's not empty and longer than 5 chars (to exclude "..", "...")
updated = Place.objects.exclude(description__in=['..', '...', '']).filter(description__gt='').count()
# Also check for specific long descriptions
long_desc = Place.objects.filter(description__regex=r'^.{20,}$').count()

print(f"Total Places: {total}")
print(f"Updated Descriptions (basic check): {updated}")
print(f"Long Descriptions (>20 chars): {long_desc}")

# List a few that might have failed if any
if total != long_desc:
    print("\nPotentially missing descriptions for:")
    missing = Place.objects.exclude(description__regex=r'^.{20,}$')
    for p in missing:
        print(f"- {p.name}: {p.description}")
