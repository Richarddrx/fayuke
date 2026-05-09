from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=25, blank=True, verbose_name='手机号')
    wechat_id = models.CharField(max_length=50, blank=True, verbose_name='微信号')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='头像')
    email_verified = models.BooleanField(default=False, verbose_name='邮箱已验证')
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简介')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.email or self.username
