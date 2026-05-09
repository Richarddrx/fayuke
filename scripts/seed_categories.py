import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

django.setup()

from apps.listings.models import Category

categories = [
    {
        'name': '二手闲置', 'slug': 'second-hand', 'icon': '🔄', 'sort_order': 1,
        'children': [
            {'name': '电子产品', 'slug': 'electronics', 'icon': '💻'},
            {'name': '家具家居', 'slug': 'furniture', 'icon': '🪑'},
            {'name': '服装鞋包', 'slug': 'clothing', 'icon': '👗'},
            {'name': '母婴用品', 'slug': 'baby', 'icon': '🍼'},
            {'name': '书籍文具', 'slug': 'books', 'icon': '📚'},
            {'name': '其他二手', 'slug': 'other-secondhand', 'icon': '📦'},
        ]
    },
    {
        'name': '房屋租贷', 'slug': 'housing', 'icon': '🏠', 'sort_order': 2,
        'children': [
            {'name': '整租', 'slug': 'whole-rental', 'icon': '🏡'},
            {'name': '合租', 'slug': 'shared-rental', 'icon': '🛏️'},
            {'name': '短租', 'slug': 'short-term', 'icon': '🏨'},
            {'name': '求租', 'slug': 'looking-for', 'icon': '🔍'},
        ]
    },
    {
        'name': '求职招聘', 'slug': 'jobs', 'icon': '💼', 'sort_order': 3,
        'children': [
            {'name': '全职', 'slug': 'full-time', 'icon': '👔'},
            {'name': '兼职', 'slug': 'part-time', 'icon': '⏰'},
            {'name': '实习', 'slug': 'internship', 'icon': '📋'},
            {'name': '招聘', 'slug': 'recruiting', 'icon': '📢'},
        ]
    },
    {
        'name': '生活服务', 'slug': 'services', 'icon': '🔧', 'sort_order': 4,
        'children': [
            {'name': '家政清洁', 'slug': 'cleaning', 'icon': '🧹'},
            {'name': '搬家货运', 'slug': 'moving', 'icon': '🚛'},
            {'name': '美容美发', 'slug': 'beauty', 'icon': '💇'},
            {'name': '餐饮外卖', 'slug': 'food', 'icon': '🍜'},
            {'name': '其他服务', 'slug': 'other-services', 'icon': '📌'},
        ]
    },
    {
        'name': '车辆专区', 'slug': 'auto', 'icon': '🚗', 'sort_order': 5,
        'children': [
            {'name': '二手车', 'slug': 'used-cars', 'icon': '🚙'},
            {'name': '车辆配件', 'slug': 'auto-parts', 'icon': '⚙️'},
            {'name': '驾校学车', 'slug': 'driving-school', 'icon': '📝'},
        ]
    },
    {
        'name': '同城交友', 'slug': 'social', 'icon': '🤝', 'sort_order': 6,
        'children': [
            {'name': '活动组织', 'slug': 'events', 'icon': '🎉'},
            {'name': '宠物', 'slug': 'pets', 'icon': '🐾'},
            {'name': '其他', 'slug': 'other-social', 'icon': '💬'},
        ]
    },
]

for cat_data in categories:
    children = cat_data.pop('children')
    parent = Category.objects.create(**cat_data)
    for child in children:
        Category.objects.create(parent=parent, **child)
    print(f'  ✓ {parent.name} ({len(children)} 子分类)')

print(f'\n共创建 {Category.objects.count()} 个分类')
