from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.management import call_command
from io import StringIO
from apps.listings.models import Category, Listing

def run_migrations(request):
    token = request.GET.get('token', '')
    action = request.GET.get('action', 'migrate')
    if token != 'fayuke2026migrate':
        return HttpResponse('Unauthorized', status=401)
    out = StringIO()
    try:
        if action == 'seed':
            from apps.listings.models import Category
            if Category.objects.count() == 0:
                cat_tree = [
                    {'name': '二手闲置', 'slug': 'second-hand', 'icon': '🔄', 'sort_order': 1, 'children': [
                        {'name': '电子产品', 'slug': 'electronics', 'icon': '💻'},
                        {'name': '家具家居', 'slug': 'furniture', 'icon': '🪑'},
                        {'name': '服装鞋包', 'slug': 'clothing', 'icon': '👗'},
                        {'name': '母婴用品', 'slug': 'baby', 'icon': '🍼'},
                        {'name': '书籍文具', 'slug': 'books', 'icon': '📚'},
                        {'name': '其他二手', 'slug': 'other-secondhand', 'icon': '📦'},
                    ]},
                    {'name': '房屋租贷', 'slug': 'housing', 'icon': '🏠', 'sort_order': 2, 'children': [
                        {'name': '整租', 'slug': 'whole-rental', 'icon': '🏡'},
                        {'name': '合租', 'slug': 'shared-rental', 'icon': '🛏️'},
                        {'name': '短租', 'slug': 'short-term', 'icon': '🏨'},
                        {'name': '求租', 'slug': 'looking-for', 'icon': '🔍'},
                    ]},
                    {'name': '求职招聘', 'slug': 'jobs', 'icon': '💼', 'sort_order': 3, 'children': [
                        {'name': '全职', 'slug': 'full-time', 'icon': '👔'},
                        {'name': '兼职', 'slug': 'part-time', 'icon': '⏰'},
                        {'name': '实习', 'slug': 'internship', 'icon': '📋'},
                        {'name': '招聘', 'slug': 'recruiting', 'icon': '📢'},
                    ]},
                    {'name': '生活服务', 'slug': 'services', 'icon': '🔧', 'sort_order': 4, 'children': [
                        {'name': '家政清洁', 'slug': 'cleaning', 'icon': '🧹'},
                        {'name': '搬家货运', 'slug': 'moving', 'icon': '🚛'},
                        {'name': '美容美发', 'slug': 'beauty', 'icon': '💇'},
                        {'name': '餐饮外卖', 'slug': 'food', 'icon': '🍜'},
                        {'name': '其他服务', 'slug': 'other-services', 'icon': '📌'},
                    ]},
                    {'name': '车辆专区', 'slug': 'auto', 'icon': '🚗', 'sort_order': 5, 'children': [
                        {'name': '二手车', 'slug': 'used-cars', 'icon': '🚙'},
                        {'name': '车辆配件', 'slug': 'auto-parts', 'icon': '⚙️'},
                        {'name': '驾校学车', 'slug': 'driving-school', 'icon': '📝'},
                    ]},
                    {'name': '同城交友', 'slug': 'social', 'icon': '🤝', 'sort_order': 6, 'children': [
                        {'name': '活动组织', 'slug': 'events', 'icon': '🎉'},
                        {'name': '宠物', 'slug': 'pets', 'icon': '🐾'},
                        {'name': '其他', 'slug': 'other-social', 'icon': '💬'},
                    ]},
                ]
                for cat_data in cat_tree:
                    children = cat_data.pop('children')
                    parent = Category.objects.create(**cat_data)
                    for child in children:
                        Category.objects.create(parent=parent, **child)
                out.write(f'Created {Category.objects.count()} categories\n')
            else:
                out.write('Categories already exist, skipping\n')

            from django.contrib.auth import get_user_model
            User = get_user_model()
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@europe58.com', 'admin123')
                out.write('Created superuser: admin / admin123\n')
            else:
                out.write('Admin user already exists\n')
        else:
            call_command('migrate', interactive=False, stdout=out)
    except Exception as e:
        return HttpResponse(f'<pre>Error: {e}</pre>', status=500)
    return HttpResponse(f'<pre>{out.getvalue()}</pre>')

def home(request):
    categories = Category.objects.filter(parent__isnull=True, is_active=True).prefetch_related('children')
    # Add listing count for each category
    for cat in categories:
        cat.listing_count = Listing.objects.filter(category__in=cat.children.all(), status='active').count()
    latest_listings = Listing.objects.filter(status='active').select_related('category').prefetch_related('images')[:12]
    return render(request, 'home.html', {
        'categories': categories,
        'latest_listings': latest_listings,
    })
