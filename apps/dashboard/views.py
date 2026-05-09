from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from apps.listings.models import Listing
from apps.core.models import Inquiry, Favorite

@login_required
def home(request):
    listings_count = Listing.objects.filter(user=request.user).count()
    active_count = Listing.objects.filter(user=request.user, status='active').count()
    inquiries_count = Inquiry.objects.filter(listing__user=request.user, is_read=False).count()
    return render(request, 'dashboard/home.html', {
        'listings_count': listings_count,
        'active_count': active_count,
        'inquiries_count': inquiries_count,
    })

class MyListingsView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/my_listings.html'
    paginate_by = 20

    def get_queryset(self):
        return Listing.objects.filter(user=self.request.user).select_related('category')

class MyInquiriesView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/my_inquiries.html'
    paginate_by = 20

    def get_queryset(self):
        return Inquiry.objects.filter(listing__user=self.request.user).select_related('listing')

class MyFavoritesView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/my_favorites.html'
    paginate_by = 20

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('listing', 'listing__category')
