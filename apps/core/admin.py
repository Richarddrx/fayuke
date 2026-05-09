from django.contrib import admin
from .models import Inquiry, Favorite

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['listing', 'sender_name', 'is_read', 'created_at']
    list_filter = ['is_read']
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = '标记为已读'

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'listing', 'created_at']
