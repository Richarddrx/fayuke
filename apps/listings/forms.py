from django import forms
from .models import Listing, Category

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'price_negotiable', 'category', 'contact_phone', 'contact_wechat', 'city', 'postal_code', 'is_urgent']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(parent__isnull=False)
        if self.instance.user_id and not self.instance.pk:
            user = self.instance.user
            self.fields['contact_phone'].initial = user.phone
            self.fields['contact_wechat'].initial = user.wechat_id
            self.fields['contact_email'].initial = user.email
