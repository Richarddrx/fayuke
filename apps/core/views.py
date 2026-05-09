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

            # Seed demo listings
            from apps.listings.models import Listing
            from datetime import timedelta
            from django.utils.timezone import now
            import random
            if Listing.objects.count() == 0:
                slug_to_cat = {c.slug: c for c in Category.objects.all()}
                demo = [
                    {'title': 'iPhone 15 Pro Max 256G 黑色', 'description': '2025年购入，95成新，配件齐全。可巴黎面交。', 'price': 899, 'cat': 'electronics', 'city': '巴黎', 'urgent': True},
                    {'title': '宜家餐桌椅套装 9成新', 'description': '实木餐桌+4把椅子，使用一年，搬家出售。自取（巴黎13区）。', 'price': 120, 'cat': 'furniture', 'city': '巴黎'},
                    {'title': '13区近地铁 温馨一室一厅 整租', 'description': '35平，3楼带电梯，独立厨房卫生间。月租850欧。', 'price': 850, 'cat': 'whole-rental', 'city': '巴黎', 'urgent': True},
                    {'title': '94省大房间合租 近Créteil', 'description': '20平大房间，家具齐全，网络水电全包。月租500欧。', 'price': 500, 'cat': 'shared-rental', 'city': 'Créteil'},
                    {'title': '中餐馆招聘洗碗工/帮厨', 'description': '巴黎13区中餐馆，待遇优，包餐。需有居留，经验不限。', 'price': None, 'cat': 'full-time', 'city': '巴黎'},
                    {'title': '宝马X3 2019 柴油 6万公里', 'description': '一手车主，定期保养，车况很好。CT2026年6月。', 'price': 18500, 'cat': 'used-cars', 'city': '巴黎', 'urgent': True},
                    {'title': '搬家服务 专业团队', 'description': '巴黎及周边搬家服务，2人团队+货车。按小时收费。', 'price': None, 'cat': 'moving', 'city': '巴黎'},
                    {'title': '巴黎华人摄影 约拍服务', 'description': '巴黎专业摄影师，铁塔、卢浮宫等景点跟拍。€120起。', 'price': 120, 'cat': 'other-services', 'city': '巴黎'},
                    {'title': '小狗求领养 法国斗牛犬', 'description': '2岁法斗，疫苗齐全，性格温顺。因回国无法带走。', 'price': 200, 'cat': 'pets', 'city': '巴黎'},
                    {'title': '巴黎到里昂 周末拼车', 'description': '每周五下午巴黎出发去里昂，单程25欧/人。', 'price': 25, 'cat': 'other-secondhand', 'city': '巴黎'},
                ]
                admin = User.objects.get(username='admin')
                for item in demo:
                    days_ago = random.randint(0, 10)
                    Listing.objects.create(
                        title=item['title'], description=item['description'],
                        price=item['price'], category=slug_to_cat[item['cat']],
                        user=admin, contact_phone='0612345678', city=item['city'],
                        is_urgent=item.get('urgent', False),
                        created_at=now() - timedelta(days=days_ago),
                        expires_at=now() + timedelta(days=45),
                    )
                out.write(f'Created {len(demo)} demo listings\n')
            else:
                out.write('Demo listings already exist, skipping\n')
            # Fix data
            Listing.objects.filter(title__icontains='Creteil').update(title='94省大房间合租 近Créteil')
            out.write('Fixed Créteil title\n')
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
