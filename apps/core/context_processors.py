from apps.listings.models import Category

CATEGORY_IMAGES = {
    'second-hand': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400&h=300&fit=crop',
    'electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400&h=300&fit=crop',
    'furniture': 'https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=300&fit=crop',
    'clothing': 'https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=400&h=300&fit=crop',
    'baby': 'https://images.unsplash.com/photo-1555252333-9f8e92e65df9?w=400&h=300&fit=crop',
    'books': 'https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=400&h=300&fit=crop',
    'other-secondhand': 'https://images.unsplash.com/photo-1688126753535-0ca32e3b5cbb?w=400&h=300&fit=crop',
    'housing': 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400&h=300&fit=crop',
    'whole-rental': 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=400&h=300&fit=crop',
    'shared-rental': 'https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=400&h=300&fit=crop',
    'short-term': 'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400&h=300&fit=crop',
    'looking-for': 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=400&h=300&fit=crop',
    'jobs': 'https://images.unsplash.com/photo-1556761175-4b46a572b786?w=400&h=300&fit=crop',
    'full-time': 'https://images.unsplash.com/photo-1556761175-4b46a572b786?w=400&h=300&fit=crop',
    'part-time': 'https://images.unsplash.com/photo-1564435408878-c4a4f2a3d0ed?w=400&h=300&fit=crop',
    'internship': 'https://images.unsplash.com/photo-1523240795612-9a054b0db644?w=400&h=300&fit=crop',
    'recruiting': 'https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=400&h=300&fit=crop',
    'services': 'https://images.unsplash.com/photo-1581783898377-1c85bf937427?w=400&h=300&fit=crop',
    'cleaning': 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=400&h=300&fit=crop',
    'moving': 'https://images.unsplash.com/photo-1600725935160-f67ee4f6084a?w=400&h=300&fit=crop',
    'beauty': 'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=400&h=300&fit=crop',
    'food': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&h=300&fit=crop',
    'other-services': 'https://images.unsplash.com/photo-1562259929-b4e1fd3aef09?w=400&h=300&fit=crop',
    'auto': 'https://images.unsplash.com/photo-1530130481716-16eac77cb82a?w=400&h=300&fit=crop',
    'used-cars': 'https://images.unsplash.com/photo-1530130481716-16eac77cb82a?w=400&h=300&fit=crop',
    'auto-parts': 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=400&h=300&fit=crop',
    'driving-school': 'https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=400&h=300&fit=crop',
    'social': 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=400&h=300&fit=crop',
    'events': 'https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=400&h=300&fit=crop',
    'pets': 'https://images.unsplash.com/photo-1623387641168-d9803ddd3f35?w=400&h=300&fit=crop',
    'other-social': 'https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=400&h=300&fit=crop',
}


def category_tree(request):
    return {
        'categories': Category.objects.filter(parent__isnull=True, is_active=True).prefetch_related('children'),
        'category_images': CATEGORY_IMAGES,
    }
