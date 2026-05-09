from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.management import call_command
from io import StringIO
from apps.listings.models import Category, Listing

def run_migrations(request):
    token = request.GET.get('token', '')
    if token != 'fayuke2026migrate':
        return HttpResponse('Unauthorized', status=401)
    out = StringIO()
    try:
        call_command('migrate', interactive=False, stdout=out)
    except Exception as e:
        return HttpResponse(f'<pre>Error: {e}</pre>', status=500)
    return HttpResponse(f'<pre>{out.getvalue()}</pre>')

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
