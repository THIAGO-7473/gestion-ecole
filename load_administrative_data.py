#!/usr/bin/env python
"""
Script pour charger les données de test des modules administratifs
"""
import os
import sys
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model
from staff.models import Enseignant, PersonnelAdministratif
from administrative.models import Conge, Contrat, Formation, ParticipationFormation

User = get_user_model()

def create_test_users():
    """Créer des utilisateurs de test si nécessaire"""
    if not User.objects.exists():
        print("Création d'un utilisateur admin...")
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✓ Utilisateur admin créé avec succès.")
    else:
        print("✓ Utilisateurs existants trouvés.")

def create_test_enseignants():
    """Créer des enseignants de test"""
    if not Enseignant.objects.exists():
        print("Création d'enseignants de test...")
        enseignants_data = [
            {
                'nom': 'Kabila',
                'postnom': 'Mwamba',
                'prenom': 'Jean-Pierre',
                'sexe': 'M',
                'date_naissance': '1985-03-15',
                'adresse': '123 Avenue du Commerce, Kinshasa',
                'telephone': '+243 123 456 789',
                'email': 'jean.kabila@ecole.com',
                'specialite': 'Mathématiques',
                'diplome': 'Licence en Mathématiques',
                'date_embauche': '2020-09-01'
            },
            {
                'nom': 'Mukendi',
                'postnom': 'Tshisekedi',
                'prenom': 'Marie',
                'sexe': 'F',
                'date_naissance': '1988-07-22',
                'adresse': '456 Rue de la Paix, Kinshasa',
                'telephone': '+243 234 567 890',
                'email': 'marie.mukendi@ecole.com',
                'specialite': 'Français',
                'diplome': 'Licence en Lettres Modernes',
                'date_embauche': '2019-09-01'
            },
            {
                'nom': 'Lumumba',
                'postnom': 'Bemba',
                'prenom': 'Antoine',
                'sexe': 'M',
                'date_naissance': '1982-11-10',
                'adresse': '789 Boulevard Lumumba, Kinshasa',
                'telephone': '+243 345 678 901',
                'email': 'antoine.lumumba@ecole.com',
                'specialite': 'Sciences',
                'diplome': 'Licence en Biologie',
                'date_embauche': '2018-09-01'
            },
            {
                'nom': 'Nzuzi',
                'postnom': 'Kabongo',
                'prenom': 'Lucie',
                'sexe': 'F',
                'date_naissance': '1990-05-18',
                'adresse': '321 Avenue de l\'Indépendance, Kinshasa',
                'telephone': '+243 456 789 012',
                'email': 'lucie.nzuzi@ecole.com',
                'specialite': 'Histoire-Géographie',
                'diplome': 'Licence en Histoire',
                'date_embauche': '2021-09-01'
            },
            {
                'nom': 'Banza',
                'postnom': 'Nkosi',
                'prenom': 'Emmanuel',
                'sexe': 'M',
                'date_naissance': '1987-12-03',
                'adresse': '654 Rue de la Révolution, Kinshasa',
                'telephone': '+243 567 890 123',
                'email': 'emmanuel.banza@ecole.com',
                'specialite': 'Anglais',
                'diplome': 'Licence en Langues Étrangères',
                'date_embauche': '2022-09-01'
            }
        ]

        for data in enseignants_data:
            Enseignant.objects.create(**data)
        print("✓ Enseignants de test créés avec succès.")
    else:
        print("✓ Enseignants existants trouvés.")

def create_test_personnel():
    """Créer du personnel administratif de test"""
    if not PersonnelAdministratif.objects.exists():
        print("Création de personnel administratif de test...")
        personnel_data = [
            {
                'nom': 'Mwamba',
                'postnom': 'Nzuzi',
                'prenom': 'Pierre',
                'sexe': 'M',
                'date_naissance': '1975-08-12',
                'adresse': '111 Avenue du Commerce, Kinshasa',
                'telephone': '+243 111 222 333',
                'email': 'pierre.mwamba@ecole.com',
                'fonction': 'Directeur Administratif',
                'departement': 'Administration',
                'date_embauche': '2015-09-01'
            },
            {
                'nom': 'Tshisekedi',
                'postnom': 'Mukendi',
                'prenom': 'Sarah',
                'sexe': 'F',
                'date_naissance': '1980-04-25',
                'adresse': '222 Rue de la Paix, Kinshasa',
                'telephone': '+243 222 333 444',
                'email': 'sarah.tshisekedi@ecole.com',
                'fonction': 'Secrétaire Administrative',
                'departement': 'Administration',
                'date_embauche': '2017-03-01'
            },
            {
                'nom': 'Bemba',
                'postnom': 'Lumumba',
                'prenom': 'Claire',
                'sexe': 'F',
                'date_naissance': '1983-09-30',
                'adresse': '333 Boulevard Lumumba, Kinshasa',
                'telephone': '+243 333 444 555',
                'email': 'claire.bemba@ecole.com',
                'fonction': 'Agent de Maintenance',
                'departement': 'Technique',
                'date_embauche': '2019-01-15'
            },
            {
                'nom': 'Kabongo',
                'postnom': 'Banza',
                'prenom': 'Grace',
                'sexe': 'F',
                'date_naissance': '1986-06-14',
                'adresse': '444 Avenue de l\'Indépendance, Kinshasa',
                'telephone': '+243 444 555 666',
                'email': 'grace.kabongo@ecole.com',
                'fonction': 'Stagiaire Administratif',
                'departement': 'Administration',
                'date_embauche': '2024-04-01'
            },
            {
                'nom': 'Nkosi',
                'postnom': 'Mwamba',
                'prenom': 'Paul',
                'sexe': 'M',
                'date_naissance': '1978-02-08',
                'adresse': '555 Rue de la Révolution, Kinshasa',
                'telephone': '+243 555 666 777',
                'email': 'paul.nkosi@ecole.com',
                'fonction': 'Comptable',
                'departement': 'Finances',
                'date_embauche': '2016-09-01'
            }
        ]

        for data in personnel_data:
            PersonnelAdministratif.objects.create(**data)
        print("✓ Personnel administratif de test créé avec succès.")
    else:
        print("✓ Personnel administratif existant trouvé.")

def load_fixtures():
    """Charger les fixtures de données de test"""
    fixtures_dir = os.path.join('administrative', 'fixtures')

    fixtures_to_load = [
        'conges_test_data.json',
        'contrats_test_data.json',
        'formations_test_data.json',
        'participations_test_data.json'
    ]

    for fixture in fixtures_to_load:
        fixture_path = os.path.join(fixtures_dir, fixture)
        if os.path.exists(fixture_path):
            try:
                call_command('loaddata', fixture_path, verbosity=0)
                print(f"✓ Données chargées avec succès: {fixture}")
            except Exception as e:
                print(f"✗ Erreur lors du chargement de {fixture}: {str(e)}")
        else:
            print(f"⚠ Fichier non trouvé: {fixture}")

def main():
    """Fonction principale"""
    print("=== Chargement des données de test administratives ===")

    # Créer les données de base nécessaires
    create_test_users()
    create_test_enseignants()
    create_test_personnel()

    # Charger les fixtures
    print("\nChargement des fixtures...")
    load_fixtures()

    print("\n=== Chargement terminé! ===")
    print("\nDonnées créées:")
    print(f"- Utilisateurs: {User.objects.count()}")
    print(f"- Enseignants: {Enseignant.objects.count()}")
    print(f"- Personnel administratif: {PersonnelAdministratif.objects.count()}")
    print(f"- Congés: {Conge.objects.count()}")
    print(f"- Contrats: {Contrat.objects.count()}")
    print(f"- Formations: {Formation.objects.count()}")
    print(f"- Participations: {ParticipationFormation.objects.count()}")

if __name__ == '__main__':
    main()
