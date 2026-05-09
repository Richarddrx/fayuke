from django.db import models
from django.conf import settings

class Inquiry(models.Model):
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='inquiries', verbose_name='关联信息')
    sender_name = models.CharField(max_length=50, verbose_name='咨询人')
    sender_email = models.EmailField(verbose_name='咨询人邮箱')
    sender_phone = models.CharField(max_length=25, blank=True, verbose_name='咨询人电话')
    message = models.TextField(verbose_name='咨询内容')
    is_read = models.BooleanField(default=False, verbose_name='已读')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='咨询时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '咨询'
        verbose_name_plural = '咨询记录'

    def __str__(self):
        return f'{self.sender_name} → {self.listing.title[:30]}'

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')
        verbose_name = '收藏'
        verbose_name_plural = '收藏'

    def __str__(self):
        return f'{self.user} → {self.listing.title[:30]}'
