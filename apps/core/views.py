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
                    {'name': 'Occasions', 'slug': 'second-hand', 'icon': '🔄', 'sort_order': 1, 'children': [
                        {'name': 'Électronique', 'slug': 'electronics', 'icon': '💻'},
                        {'name': 'Meubles & Maison', 'slug': 'furniture', 'icon': '🪑'},
                        {'name': 'Mode & Accessoires', 'slug': 'clothing', 'icon': '👗'},
                        {'name': 'Enfants & Bébé', 'slug': 'baby', 'icon': '🍼'},
                        {'name': 'Livres & Papeterie', 'slug': 'books', 'icon': '📚'},
                        {'name': 'Autres occasions', 'slug': 'other-secondhand', 'icon': '📦'},
                    ]},
                    {'name': 'Immobilier', 'slug': 'housing', 'icon': '🏠', 'sort_order': 2, 'children': [
                        {'name': 'Location entière', 'slug': 'whole-rental', 'icon': '🏡'},
                        {'name': 'Colocation', 'slug': 'shared-rental', 'icon': '🛏️'},
                        {'name': 'Courte durée', 'slug': 'short-term', 'icon': '🏨'},
                        {'name': 'Recherche logement', 'slug': 'looking-for', 'icon': '🔍'},
                    ]},
                    {'name': 'Emplois', 'slug': 'jobs', 'icon': '💼', 'sort_order': 3, 'children': [
                        {'name': 'Plein temps', 'slug': 'full-time', 'icon': '👔'},
                        {'name': 'Temps partiel', 'slug': 'part-time', 'icon': '⏰'},
                        {'name': 'Stage', 'slug': 'internship', 'icon': '📋'},
                        {'name': 'Recrutement', 'slug': 'recruiting', 'icon': '📢'},
                    ]},
                    {'name': 'Services', 'slug': 'services', 'icon': '🔧', 'sort_order': 4, 'children': [
                        {'name': 'Ménage & Nettoyage', 'slug': 'cleaning', 'icon': '🧹'},
                        {'name': 'Déménagement', 'slug': 'moving', 'icon': '🚛'},
                        {'name': 'Beauté & Coiffure', 'slug': 'beauty', 'icon': '💇'},
                        {'name': 'Restauration', 'slug': 'food', 'icon': '🍜'},
                        {'name': 'Autres services', 'slug': 'other-services', 'icon': '📌'},
                    ]},
                    {'name': 'Véhicules', 'slug': 'auto', 'icon': '🚗', 'sort_order': 5, 'children': [
                        {'name': 'Voitures d\'occasion', 'slug': 'used-cars', 'icon': '🚙'},
                        {'name': 'Pièces auto', 'slug': 'auto-parts', 'icon': '⚙️'},
                        {'name': 'Auto-école', 'slug': 'driving-school', 'icon': '📝'},
                    ]},
                    {'name': 'Rencontres', 'slug': 'social', 'icon': '🤝', 'sort_order': 6, 'children': [
                        {'name': 'Événements', 'slug': 'events', 'icon': '🎉'},
                        {'name': 'Animaux', 'slug': 'pets', 'icon': '🐾'},
                        {'name': 'Autres', 'slug': 'other-social', 'icon': '💬'},
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
                    {'title': 'iPhone 15 Pro Max 256G Noir', 'description': 'Acheté en 2025, état neuf (95%), accessoires complets. Remise en main propre à Paris.', 'price': 899, 'cat': 'electronics', 'city': 'Paris', 'urgent': True},
                    {'title': 'Table IKEA + 4 chaises 9/10', 'description': 'Table en bois massif + 4 chaises, utilisé 1 an, déménagement. À venir chercher (Paris 13e).', 'price': 120, 'cat': 'furniture', 'city': 'Paris'},
                    {'title': 'Studio meublé Paris 13e près métro', 'description': '35m², 3e étage ascenseur, cuisine équipée. 850€/mois CC.', 'price': 850, 'cat': 'whole-rental', 'city': 'Paris', 'urgent': True},
                    {'title': 'Grande chambre en coloc près Créteil', 'description': '20m², meublé, charges incluses (wifi/électricité/eau). 500€/mois.', 'price': 500, 'cat': 'shared-rental', 'city': 'Créteil'},
                    {'title': 'Restaurant chinois cherche plongeur/aide-cuisine', 'description': 'Restaurant Paris 13e, bonne rémunération, repas fourni. Titre de séjour requis, pas d\'expérience nécessaire.', 'price': None, 'cat': 'full-time', 'city': 'Paris'},
                    {'title': 'BMW X3 2019 Diesel 60 000 km', 'description': 'Première main, entretien régulier, excellent état. CT juin 2026.', 'price': 18500, 'cat': 'used-cars', 'city': 'Paris', 'urgent': True},
                    {'title': 'Service déménagement équipe pro', 'description': 'Déménagement Paris et banlieue, équipe de 2 + fourgon. Tarif à l\'heure.', 'price': None, 'cat': 'moving', 'city': 'Paris'},
                    {'title': 'Photographe chinois à Paris', 'description': 'Photographe professionnel à Paris, shooting Tour Eiffel, Louvre... À partir de 120€.', 'price': 120, 'cat': 'other-services', 'city': 'Paris'},
                    {'title': 'Bouledogue français à donner', 'description': '2 ans, vaccins à jour, caractère doux. Je rentre en Chine, ne peux pas l\'emmener.', 'price': 200, 'cat': 'pets', 'city': 'Paris'},
                    {'title': 'Covoiturage Paris → Lyon week-end', 'description': 'Départ Paris vendredi après-midi direction Lyon. 25€/personne.', 'price': 25, 'cat': 'other-secondhand', 'city': 'Paris'},
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
            Listing.objects.filter(title__icontains='Creteil').update(title='Grande chambre en coloc près Créteil')
            out.write('Fixed Créteil title\n')

        if action == 'update_fr':
            name_map = {
                '二手闲置': 'Occasions', '电子产品': 'Électronique', '家具家居': 'Meubles & Maison',
                '服装鞋包': 'Mode & Accessoires', '母婴用品': 'Enfants & Bébé', '书籍文具': 'Livres & Papeterie',
                '其他二手': 'Autres occasions', '房屋租贷': 'Immobilier', '整租': 'Location entière',
                '合租': 'Colocation', '短租': 'Courte durée', '求租': 'Recherche logement',
                '求职招聘': 'Emplois', '全职': 'Plein temps', '兼职': 'Temps partiel',
                '实习': 'Stage', '招聘': 'Recrutement', '生活服务': 'Services',
                '家政清洁': 'Ménage & Nettoyage', '搬家货运': 'Déménagement',
                '美容美发': 'Beauté & Coiffure', '餐饮外卖': 'Restauration', '其他服务': 'Autres services',
                '车辆专区': 'Véhicules', '二手车': "Voitures d'occasion", '车辆配件': 'Pièces auto',
                '驾校学车': 'Auto-école', '同城交友': 'Rencontres', '活动组织': 'Événements',
                '宠物': 'Animaux', '其他': 'Autres',
            }
            for old_name, new_name in name_map.items():
                cnt = Category.objects.filter(name=old_name).update(name=new_name)
                if cnt:
                    out.write(f'Renamed "{old_name}" → "{new_name}"\n')
            cnt2 = Listing.objects.filter(city='巴黎').update(city='Paris')
            if cnt2:
                out.write(f'Updated {cnt2} listings: 巴黎 → Paris\n')
            else:
                out.write('No Chinese city names found\n')
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
