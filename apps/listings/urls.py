from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.ListingListView.as_view(), name='list'),
    path('category/<slug:slug>/', views.ListingByCategoryView.as_view(), name='category'),
    path('<slug:slug>/', views.ListingDetailView.as_view(), name='detail'),
    path('create/', views.ListingCreateView.as_view(), name='create'),
    path('<slug:slug>/edit/', views.ListingUpdateView.as_view(), name='edit'),
    path('<slug:slug>/delete/', views.ListingDeleteView.as_view(), name='delete'),
    path('search/', views.SearchView.as_view(), name='search'),
]
