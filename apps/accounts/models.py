from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=25, blank=True, verbose_name='Téléphone')
    wechat_id = models.CharField(max_length=50, blank=True, verbose_name='WeChat')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='Avatar')
    email_verified = models.BooleanField(default=False, verbose_name='Email vérifié')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Biographie')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return self.email or self.username
