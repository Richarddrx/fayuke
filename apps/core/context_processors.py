from apps.listings.models import Category

def category_tree(request):
    return {
        'categories': Category.objects.filter(parent__isnull=True, is_active=True).prefetch_related('children'),
    }
