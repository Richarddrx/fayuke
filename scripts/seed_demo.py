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
    {'title': 'iPhone 15 Pro Max 256G Noir', 'description': 'Acheté en 2025, état neuf (95%), déverrouillé, accessoires complets. Vendu pour changement de téléphone. Remise en main propre ou envoi à Paris.', 'price': 899, 'category_slug': 'electronics', 'city': 'Paris', 'is_urgent': True},
    {'title': 'Table IKEA + 4 chaises 9/10', 'description': 'Table en bois massif + 4 chaises, utilisé 1 an, déménagement. À venir chercher (Paris 13e). Dimensions 140x80cm.', 'price': 120, 'category_slug': 'furniture', 'city': 'Paris'},
    {'title': 'Chanel classique état impeccable', 'description': 'Acheté en 2024 aux Galeries Lafayette, utilisé 3 fois seulement, boîte et ticket d\'origine. Authenticité garantie.', 'price': 2800, 'category_slug': 'clothing', 'city': 'Paris'},
    {'title': 'Studio meublé Paris 13e près métro', 'description': '35m², 3e étage ascenseur, cuisine équipée, salle de bain indépendante. 850€/mois CC. Disponible immédiatement. Près ligne 7 Tolbiac.', 'price': 850, 'category_slug': 'whole-rental', 'city': 'Paris', 'is_urgent': True},
    {'title': 'Grande chambre en coloc près Créteil', 'description': '20m² meublé, charges incluses (wifi/électricité/eau). Coloc avec étudiants chinois. 500€/mois.', 'price': 500, 'category_slug': 'shared-rental', 'city': 'Créteil'},
    {'title': 'Restaurant chinois cherche plongeur/aide-cuisine', 'description': 'Paris 13e, bonne rémunération, repas fournis. Titre de séjour requis. Lun-sam, 8h/jour.', 'price': None, 'category_slug': 'full-time', 'city': 'Paris'},
    {'title': 'Cours de chinois le week-end cherche prof', 'description': 'Pour deux enfants chinois (8 et 10 ans), soutien en chinois et maths. Samedi après-midi, 25€/h.', 'price': None, 'category_slug': 'part-time', 'city': 'Paris'},
    {'title': 'BMW X3 2019 Diesel 60 000 km', 'description': 'Première main, entretien régulier, excellent état. CT juin 2026. Prix négociable. Visible à Paris.', 'price': 18500, 'category_slug': 'used-cars', 'city': 'Paris', 'is_urgent': True},
    {'title': 'Service déménagement équipe pro', 'description': 'Déménagement Paris et banlieue, équipe de 2 + fourgon. Tarif à l\'heure, transparent. WeChat : demo_wechat.', 'price': None, 'category_slug': 'moving', 'city': 'Paris'},
    {'title': 'Photographe chinois à Paris', 'description': 'Photographe pro à Paris, shooting Tour Eiffel, Louvre... Portraits famille, couple, individuels. À partir de 120€.', 'price': 120, 'category_slug': 'other-services', 'city': 'Paris'},
    {'title': 'Bouledogue français à donner', 'description': '2 ans, mâle, vaccins à jour, caractère doux. Je rentre en Chine, cherche bonne famille. Frais de vaccins à payer.', 'price': 200, 'category_slug': 'pets', 'city': 'Paris'},
    {'title': 'Covoiturage Paris → Lyon week-end', 'description': 'Départ Paris vendredi après-midi direction Lyon, retour dimanche après-midi. 25€/personne, bagages illimités.', 'price': 25, 'category_slug': 'other-secondhand', 'city': 'Paris'},
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

print(f'\n✅ {len(demo_listings)} annonces créées')
