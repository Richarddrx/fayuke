import django, os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
django.setup()

from apps.listings.models import Category

name_map = {
    '二手闲置': 'Occasions', '电子产品': 'Électronique', '家具家居': 'Meubles & Maison',
    '服装鞋包': 'Mode & Accessoires', '母婴用品': 'Enfants & Bébé', '书籍文具': 'Livres & Papeterie',
    '其他二手': 'Autres occasions',
    '房屋租贷': 'Immobilier', '整租': 'Location entière', '合租': 'Colocation',
    '短租': 'Courte durée', '求租': 'Recherche logement',
    '求职招聘': 'Emplois', '全职': 'Plein temps', '兼职': 'Temps partiel',
    '实习': 'Stage', '招聘': 'Recrutement',
    '生活服务': 'Services', '家政清洁': 'Ménage & Nettoyage', '搬家货运': 'Déménagement',
    '美容美发': 'Beauté & Coiffure', '餐饮外卖': 'Restauration', '其他服务': 'Autres services',
    '车辆专区': 'Véhicules', '二手车': 'Voitures d\'occasion', '车辆配件': 'Pièces auto',
    '驾校学车': 'Auto-école',
    '同城交友': 'Rencontres', '活动组织': 'Événements', '宠物': 'Animaux', '其他': 'Autres',
}

for old_name, new_name in name_map.items():
    updated = Category.objects.filter(name=old_name).update(name=new_name)
    if updated:
        print(f'  ✓ {old_name} → {new_name}')

# Also update city from 巴黎 to Paris
from apps.listings.models import Listing
updated_city = Listing.objects.filter(city='巴黎').update(city='Paris')
if updated_city:
    print(f'  ✓ {updated_city} annonces: 巴黎 → Paris')

print(f'\n✅ Mise à jour terminée')
