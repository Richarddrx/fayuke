from django.db import models
from django.conf import settings

class Inquiry(models.Model):
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='inquiries', verbose_name='Annonce')
    sender_name = models.CharField(max_length=50, verbose_name='Nom')
    sender_email = models.EmailField(verbose_name='Email')
    sender_phone = models.CharField(max_length=25, blank=True, verbose_name='Téléphone')
    message = models.TextField(verbose_name='Message')
    is_read = models.BooleanField(default=False, verbose_name='Lu')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return f'{self.sender_name} → {self.listing.title[:30]}'

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')
        verbose_name = 'Favori'
        verbose_name_plural = 'Favoris'

    def __str__(self):
        return f'{self.user} → {self.listing.title[:30]}'
