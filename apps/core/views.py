from django.shortcuts import render
from apps.listings.models import Category, Listing

def home(request):
    categories = Category.objects.filter(parent__isnull=True, is_active=True).prefetch_related('children')
    # Add listing count for each category
    for cat in categories:
        cat.listing_count = Listing.objects.filter(category__in=cat.children.all(), status='active').count()
    latest_listings = Listing.objects.filter(status='active').select_related('category').prefetch_related('images')[:12]
    return render(request, 'home.html', {
        'categories': categories,
        'latest_listings': latest_listings,
    })
