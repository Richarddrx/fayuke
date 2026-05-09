from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('listings/', views.MyListingsView.as_view(), name='my_listings'),
    path('inquiries/', views.MyInquiriesView.as_view(), name='my_inquiries'),
    path('favorites/', views.MyFavoritesView.as_view(), name='my_favorites'),
]
