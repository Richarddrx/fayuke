import django, os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from django.contrib.auth import get_user_model
from apps.listings.models import Category, Listing, ListingImage
from io import BytesIO
from django.core.files.base import ContentFile
import random
from datetime import timedelta
from django.utils.timezone import now

User = get_user_model()
admin = User.objects.get(username='admin')

demo_listings = [
    {'title': 'iPhone 15 Pro Max 256G 黑色', 'description': '2025年购入，95成新，全网通无锁，配件齐全。因换新机出售。可巴黎面交或邮寄。', 'price': 899, 'category_slug': 'electronics', 'city': '巴黎', 'is_urgent': True},
    {'title': '宜家餐桌椅套装 9成新', 'description': '实木餐桌+4把椅子，使用一年，搬家出售。自取（巴黎13区）。尺寸140x80cm。', 'price': 120, 'category_slug': 'furniture', 'city': '巴黎'},
    {'title': 'Chanel 经典款 成色极新', 'description': '2024年购于巴黎老佛爷，仅使用过3次，有原盒和票据。可验货。', 'price': 2800, 'category_slug': 'clothing', 'city': '巴黎'},
    {'title': '13区近地铁 温馨一室一厅 整租', 'description': '35平，3楼带电梯，独立厨房卫生间。月租850欧含charge。即日起租。近7号线Tolbiac。', 'price': 850, 'category_slug': 'whole-rental', 'city': '巴黎', 'is_urgent': True},
    {'title': '94省大房间合租 近Creteil', 'description': '20平大房间，家具齐全，网络水电全包。室友都是中国留学生。月租500欧。', 'price': 500, 'category_slug': 'shared-rental', 'city': 'Créteil'},
    {'title': '中餐馆招聘洗碗工/帮厨', 'description': '巴黎13区中餐馆，待遇优，包餐。需有居留，经验不限。周一至周六，每天8小时。', 'price': None, 'category_slug': 'full-time', 'city': '巴黎'},
    {'title': '周末中文家教 招聘老师', 'description': '为两个华人孩子（8岁和10岁）辅导中文和数学。周六下午，每小时25欧。需要中文标准。', 'price': None, 'category_slug': 'part-time', 'city': '巴黎'},
    {'title': '宝马X3 2019 柴油 6万公里', 'description': '一手车主，定期保养，车况很好。CT2026年6月。价格可小刀。巴黎可看车。', 'price': 18500, 'category_slug': 'used-cars', 'city': '巴黎', 'is_urgent': True},
    {'title': '搬家服务 专业团队', 'description': '巴黎及周边搬家服务，2人团队+货车。按小时收费，透明无隐形费用。微信：demo_wechat。', 'price': None, 'category_slug': 'moving', 'city': '巴黎'},
    {'title': '巴黎华人摄影 约拍服务', 'description': '巴黎专业摄影师，铁塔、卢浮宫等景点跟拍。家庭写真、情侣照、个人写真。€120起。', 'price': 120, 'category_slug': 'other-services', 'city': '巴黎'},
    {'title': '小狗求领养 法国斗牛犬', 'description': '2岁法斗，公，疫苗齐全，性格温顺。因回国无法带走，希望找个好人家。需支付疫苗费用。', 'price': 200, 'category_slug': 'pets', 'city': '巴黎'},
    {'title': '巴黎到里昂 周末拼车', 'description': '每周五下午巴黎出发去里昂，周日下午返回。单程25欧/人，行李不限。', 'price': 25, 'category_slug': 'other-secondhand', 'city': '巴黎'},
]

electronics = Category.objects.get(slug='electronics')
furniture = Category.objects.get(slug='furniture')
clothing = Category.objects.get(slug='clothing')
whole_rental = Category.objects.get(slug='whole-rental')
shared_rental = Category.objects.get(slug='shared-rental')
full_time = Category.objects.get(slug='full-time')
part_time = Category.objects.get(slug='part-time')
used_cars = Category.objects.get(slug='used-cars')
moving = Category.objects.get(slug='moving')
other_services = Category.objects.get(slug='other-services')
pets = Category.objects.get(slug='pets')
other_secondhand = Category.objects.get(slug='other-secondhand')

slug_to_cat = {
    'electronics': electronics, 'furniture': furniture, 'clothing': clothing,
    'whole-rental': whole_rental, 'shared-rental': shared_rental,
    'full-time': full_time, 'part-time': part_time, 'used-cars': used_cars,
    'moving': moving, 'other-services': other_services, 'pets': pets,
    'other-secondhand': other_secondhand,
}

for i, item in enumerate(demo_listings):
    days_ago = random.randint(0, 20)
    listing = Listing.objects.create(
        title=item['title'],
        description=item['description'],
        price=item['price'],
        category=slug_to_cat[item['category_slug']],
        user=admin,
        contact_phone='0612345678',
        contact_wechat='demo_wechat',
        city=item['city'],
        is_urgent=item.get('is_urgent', False),
        created_at=now() - timedelta(days=days_ago),
        expires_at=now() + timedelta(days=45),
    )
    print(f'  ✓ {listing.title}')

print(f'\n✅ 共添加 {len(demo_listings)} 条示例信息')
