import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

django.setup()

from apps.listings.models import Category

categories = [
    {
        'name': 'Occasions', 'slug': 'second-hand', 'icon': '🔄', 'sort_order': 1,
        'children': [
            {'name': 'Électronique', 'slug': 'electronics', 'icon': '💻'},
            {'name': 'Meubles & Maison', 'slug': 'furniture', 'icon': '🪑'},
            {'name': 'Mode & Accessoires', 'slug': 'clothing', 'icon': '👗'},
            {'name': 'Enfants & Bébé', 'slug': 'baby', 'icon': '🍼'},
            {'name': 'Livres & Papeterie', 'slug': 'books', 'icon': '📚'},
            {'name': 'Autres occasions', 'slug': 'other-secondhand', 'icon': '📦'},
        ]
    },
    {
        'name': 'Immobilier', 'slug': 'housing', 'icon': '🏠', 'sort_order': 2,
        'children': [
            {'name': 'Location entière', 'slug': 'whole-rental', 'icon': '🏡'},
            {'name': 'Colocation', 'slug': 'shared-rental', 'icon': '🛏️'},
            {'name': 'Courte durée', 'slug': 'short-term', 'icon': '🏨'},
            {'name': 'Recherche logement', 'slug': 'looking-for', 'icon': '🔍'},
        ]
    },
    {
        'name': 'Emplois', 'slug': 'jobs', 'icon': '💼', 'sort_order': 3,
        'children': [
            {'name': 'Plein temps', 'slug': 'full-time', 'icon': '👔'},
            {'name': 'Temps partiel', 'slug': 'part-time', 'icon': '⏰'},
            {'name': 'Stage', 'slug': 'internship', 'icon': '📋'},
            {'name': 'Recrutement', 'slug': 'recruiting', 'icon': '📢'},
        ]
    },
    {
        'name': 'Services', 'slug': 'services', 'icon': '🔧', 'sort_order': 4,
        'children': [
            {'name': 'Ménage & Nettoyage', 'slug': 'cleaning', 'icon': '🧹'},
            {'name': 'Déménagement', 'slug': 'moving', 'icon': '🚛'},
            {'name': 'Beauté & Coiffure', 'slug': 'beauty', 'icon': '💇'},
            {'name': 'Restauration', 'slug': 'food', 'icon': '🍜'},
            {'name': 'Autres services', 'slug': 'other-services', 'icon': '📌'},
        ]
    },
    {
        'name': 'Véhicules', 'slug': 'auto', 'icon': '🚗', 'sort_order': 5,
        'children': [
            {'name': 'Voitures d\'occasion', 'slug': 'used-cars', 'icon': '🚙'},
            {'name': 'Pièces auto', 'slug': 'auto-parts', 'icon': '⚙️'},
            {'name': 'Auto-école', 'slug': 'driving-school', 'icon': '📝'},
        ]
    },
    {
        'name': 'Rencontres', 'slug': 'social', 'icon': '🤝', 'sort_order': 6,
        'children': [
            {'name': 'Événements', 'slug': 'events', 'icon': '🎉'},
            {'name': 'Animaux', 'slug': 'pets', 'icon': '🐾'},
            {'name': 'Autres', 'slug': 'other-social', 'icon': '💬'},
        ]
    },
]

for cat_data in categories:
    children = cat_data.pop('children')
    parent = Category.objects.create(**cat_data)
    for child in children:
        Category.objects.create(parent=parent, **child)
    print(f'  ✓ {parent.name} ({len(children)} sous-catégories)')

print(f'\n✓ {Category.objects.count()} catégories créées')
