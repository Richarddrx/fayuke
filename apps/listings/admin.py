from django.contrib import admin
from .models import Category, Listing, ListingImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'sort_order', 'is_active']
    list_editable = ['sort_order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'user', 'price', 'city', 'status', 'is_urgent', 'created_at']
    list_filter = ['status', 'category', 'city', 'is_urgent']
    search_fields = ['title', 'description']
    date_hierarchy = 'created_at'
    actions = ['make_active', 'make_expired']
    fieldsets = [
        ('Informations', {'fields': ['title', 'description', 'price', 'price_negotiable', 'category']}),
        ('Contact', {'fields': ['contact_phone', 'contact_wechat', 'contact_email']}),
        ('Localisation', {'fields': ['city', 'postal_code']}),
        ('Statut', {'fields': ['status', 'is_urgent', 'views_count']}),
    ]

    def make_active(self, request, queryset):
        queryset.update(status='active')
    make_active.short_description = 'Marquer comme active'

    def make_expired(self, request, queryset):
        queryset.update(status='expired')
    make_expired.short_description = 'Marquer comme expirée'

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ['listing', 'sort_order']
