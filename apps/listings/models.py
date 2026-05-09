from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.timezone import now
from uuid import uuid4
from datetime import timedelta

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='分类名称')
    slug = models.SlugField(max_length=60, unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children', verbose_name='上级分类')
    icon = models.CharField(max_length=20, blank=True, verbose_name='图标')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    is_active = models.BooleanField(default=True, verbose_name='启用')

    class Meta:
        ordering = ['sort_order', 'name']
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def __str__(self):
        return f'{self.parent.name} > {self.name}' if self.parent else self.name

class Listing(models.Model):
    STATUS_CHOICES = [
        ('active', '已发布'),
        ('sold', '已成交'),
        ('expired', '已过期'),
        ('draft', '草稿'),
        ('rejected', '未通过'),
    ]

    title = models.CharField(max_length=100, verbose_name='标题')
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(verbose_name='详细描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='价格(€)')
    price_negotiable = models.BooleanField(default=False, verbose_name='价格可议')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings', verbose_name='分类')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings', verbose_name='发布者')
    contact_phone = models.CharField(max_length=25, blank=True, verbose_name='联系电话')
    contact_wechat = models.CharField(max_length=50, blank=True, verbose_name='微信')
    contact_email = models.EmailField(blank=True, verbose_name='联系邮箱')
    city = models.CharField(max_length=50, blank=True, default='巴黎', verbose_name='城市')
    postal_code = models.CharField(max_length=10, blank=True, verbose_name='邮编')
    is_urgent = models.BooleanField(default=False, verbose_name='置顶')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active', verbose_name='状态')
    views_count = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    expires_at = models.DateTimeField(verbose_name='过期时间')

    class Meta:
        ordering = ['-is_urgent', '-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['city']),
        ]
        verbose_name = '信息'
        verbose_name_plural = '信息列表'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.title}-{uuid4().hex[:8]}')
        if not self.expires_at:
            self.expires_at = now() + timedelta(days=45)
        super().save(*args, **kwargs)

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images', verbose_name='关联信息')
    image = models.ImageField(upload_to='listings/%Y/%m/', verbose_name='图片')
    sort_order = models.IntegerField(default=0, verbose_name='排序')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order']
        verbose_name = '图片'
        verbose_name_plural = '图片'

    def __str__(self):
        return f'图片 {self.sort_order} - {self.listing.title}'
