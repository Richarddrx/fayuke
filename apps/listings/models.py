from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.timezone import now
from uuid import uuid4
from datetime import timedelta

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nom')
    slug = models.SlugField(max_length=60, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children', verbose_name='Catégorie parente')
    icon = models.CharField(max_length=20, blank=True, verbose_name='Icône')
    sort_order = models.IntegerField(default=0, verbose_name='Ordre')
    is_active = models.BooleanField(default=True, verbose_name='Active')

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'

    def __str__(self):
        return f'{self.parent.name} > {self.name}' if self.parent else self.name

class Listing(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Vendue'),
        ('expired', 'Expirée'),
        ('draft', 'Brouillon'),
        ('rejected', 'Rejetée'),
    ]

    title = models.CharField(max_length=100, verbose_name='Titre')
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Prix (€)')
    price_negotiable = models.BooleanField(default=False, verbose_name='Prix négociable')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings', verbose_name='Catégorie')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings', verbose_name='Utilisateur')
    contact_phone = models.CharField(max_length=25, blank=True, verbose_name='Téléphone')
    contact_wechat = models.CharField(max_length=50, blank=True, verbose_name='WeChat')
    contact_email = models.EmailField(blank=True, verbose_name='Email')
    city = models.CharField(max_length=50, blank=True, default='Paris', verbose_name='Ville')
    postal_code = models.CharField(max_length=10, blank=True, verbose_name='Code postal')
    is_urgent = models.BooleanField(default=False, verbose_name='Urgent')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name='Statut')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Vues')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date de création')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Date de modification')
    expires_at = models.DateTimeField(verbose_name='Date d\'expiration')

    class Meta:
        ordering = ['-is_urgent', '-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['city']),
        ]
        verbose_name = 'Annonce'
        verbose_name_plural = 'Annonces'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.title}-{uuid4().hex[:8]}')
        if not self.expires_at:
            self.expires_at = now() + timedelta(days=45)
        super().save(*args, **kwargs)

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images', verbose_name='Annonce')
    image = models.ImageField(upload_to='listings/%Y/%m/', verbose_name='Image')
    sort_order = models.IntegerField(default=0, verbose_name='Ordre')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order']
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    def __str__(self):
        return f'Image {self.sort_order} - {self.listing.title}'
