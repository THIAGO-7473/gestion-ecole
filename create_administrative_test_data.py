#!/usr/bin/env python
"""
Script pour créer les données de test des modules administratifs
"""
import os
import sys
import django
from datetime import datetime, timedelta, date
from decimal import Decimal

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from django.contrib.auth import get_user_model
from staff.models import Enseignant, PersonnelAdministratif
from administrative.models import Conge, Contrat, Formation, ParticipationFormation

User = get_user_model()

def create_test_users():
    """Créer des utilisateurs de test"""
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
                'date_naissance': date(1985, 3, 15),
                'adresse': '123 Avenue du Commerce, Kinshasa',
                'telephone': '+243 123 456 789',
                'email': 'jean.kabila@ecole.com',
                'specialite': 'Mathématiques',
                'diplome': 'Licence en Mathématiques',
                'date_embauche': date(2020, 9, 1)
            },
            {
                'nom': 'Mukendi',
                'postnom': 'Tshisekedi',
                'prenom': 'Marie',
                'sexe': 'F',
                'date_naissance': date(1988, 7, 22),
                'adresse': '456 Rue de la Paix, Kinshasa',
                'telephone': '+243 234 567 890',
                'email': 'marie.mukendi@ecole.com',
                'specialite': 'Français',
                'diplome': 'Licence en Lettres Modernes',
                'date_embauche': date(2019, 9, 1)
            },
            {
                'nom': 'Lumumba',
                'postnom': 'Bemba',
                'prenom': 'Antoine',
                'sexe': 'M',
                'date_naissance': date(1982, 11, 10),
                'adresse': '789 Boulevard Lumumba, Kinshasa',
                'telephone': '+243 345 678 901',
                'email': 'antoine.lumumba@ecole.com',
                'specialite': 'Sciences',
                'diplome': 'Licence en Biologie',
                'date_embauche': date(2018, 9, 1)
            },
            {
                'nom': 'Nzuzi',
                'postnom': 'Kabongo',
                'prenom': 'Lucie',
                'sexe': 'F',
                'date_naissance': date(1990, 5, 18),
                'adresse': '321 Avenue de l\'Indépendance, Kinshasa',
                'telephone': '+243 456 789 012',
                'email': 'lucie.nzuzi@ecole.com',
                'specialite': 'Histoire-Géographie',
                'diplome': 'Licence en Histoire',
                'date_embauche': date(2021, 9, 1)
            },
            {
                'nom': 'Banza',
                'postnom': 'Nkosi',
                'prenom': 'Emmanuel',
                'sexe': 'M',
                'date_naissance': date(1987, 12, 3),
                'adresse': '654 Rue de la Révolution, Kinshasa',
                'telephone': '+243 567 890 123',
                'email': 'emmanuel.banza@ecole.com',
                'specialite': 'Anglais',
                'diplome': 'Licence en Langues Étrangères',
                'date_embauche': date(2022, 9, 1)
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
                'date_naissance': date(1975, 8, 12),
                'adresse': '111 Avenue du Commerce, Kinshasa',
                'telephone': '+243 111 222 333',
                'email': 'pierre.mwamba@ecole.com',
                'fonction': 'Directeur Administratif',
                'departement': 'Administration',
                'date_embauche': date(2015, 9, 1)
            },
            {
                'nom': 'Tshisekedi',
                'postnom': 'Mukendi',
                'prenom': 'Sarah',
                'sexe': 'F',
                'date_naissance': date(1980, 4, 25),
                'adresse': '222 Rue de la Paix, Kinshasa',
                'telephone': '+243 222 333 444',
                'email': 'sarah.tshisekedi@ecole.com',
                'fonction': 'Secrétaire Administrative',
                'departement': 'Administration',
                'date_embauche': date(2017, 3, 1)
            },
            {
                'nom': 'Bemba',
                'postnom': 'Lumumba',
                'prenom': 'Claire',
                'sexe': 'F',
                'date_naissance': date(1983, 9, 30),
                'adresse': '333 Boulevard Lumumba, Kinshasa',
                'telephone': '+243 333 444 555',
                'email': 'claire.bemba@ecole.com',
                'fonction': 'Agent de Maintenance',
                'departement': 'Technique',
                'date_embauche': date(2019, 1, 15)
            },
            {
                'nom': 'Kabongo',
                'postnom': 'Banza',
                'prenom': 'Grace',
                'sexe': 'F',
                'date_naissance': date(1986, 6, 14),
                'adresse': '444 Avenue de l\'Indépendance, Kinshasa',
                'telephone': '+243 444 555 666',
                'email': 'grace.kabongo@ecole.com',
                'fonction': 'Stagiaire Administratif',
                'departement': 'Administration',
                'date_embauche': date(2024, 4, 1)
            },
            {
                'nom': 'Nkosi',
                'postnom': 'Mwamba',
                'prenom': 'Paul',
                'sexe': 'M',
                'date_naissance': date(1978, 2, 8),
                'adresse': '555 Rue de la Révolution, Kinshasa',
                'telephone': '+243 555 666 777',
                'email': 'paul.nkosi@ecole.com',
                'fonction': 'Comptable',
                'departement': 'Finances',
                'date_embauche': date(2016, 9, 1)
            }
        ]

        for data in personnel_data:
            PersonnelAdministratif.objects.create(**data)
        print("✓ Personnel administratif de test créé avec succès.")
    else:
        print("✓ Personnel administratif existant trouvé.")

def create_test_conges():
    """Créer des congés de test"""
    if not Conge.objects.exists():
        print("Création de congés de test...")

        admin_user = User.objects.first()
        enseignants = list(Enseignant.objects.all())
        personnel = list(PersonnelAdministratif.objects.all())

        conges_data = [
            {
                'personnel': personnel[0] if personnel else None,
                'enseignant': None,
                'type_conge': 'annuel',
                'date_debut': date(2024, 7, 15),
                'date_fin': date(2024, 8, 15),
                'jours_ouvrables': 22,
                'statut': 'approuve',
                'motif': 'Congé annuel pour repos et récupération',
                'approuve_par': admin_user,
                'date_approbation': date(2024, 6, 20)
            },
            {
                'personnel': None,
                'enseignant': enseignants[0] if enseignants else None,
                'type_conge': 'maladie',
                'date_debut': date(2024, 9, 10),
                'date_fin': date(2024, 9, 20),
                'jours_ouvrables': 8,
                'statut': 'approuve',
                'motif': 'Congé maladie avec certificat médical',
                'approuve_par': admin_user,
                'date_approbation': date(2024, 9, 9)
            },
            {
                'personnel': personnel[1] if len(personnel) > 1 else None,
                'enseignant': None,
                'type_conge': 'maternite',
                'date_debut': date(2024, 10, 1),
                'date_fin': date(2024, 12, 31),
                'jours_ouvrables': 65,
                'statut': 'approuve',
                'motif': 'Congé maternité - accouchement prévu en octobre',
                'approuve_par': admin_user,
                'date_approbation': date(2024, 9, 15)
            },
            {
                'personnel': None,
                'enseignant': enseignants[1] if len(enseignants) > 1 else None,
                'type_conge': 'exceptionnel',
                'date_debut': date(2024, 11, 5),
                'date_fin': date(2024, 11, 7),
                'jours_ouvrables': 3,
                'statut': 'approuve',
                'motif': 'Décès d\'un membre de la famille - funérailles',
                'approuve_par': admin_user,
                'date_approbation': date(2024, 11, 4)
            },
            {
                'personnel': personnel[2] if len(personnel) > 2 else None,
                'enseignant': None,
                'type_conge': 'paternite',
                'date_debut': date(2024, 12, 1),
                'date_fin': date(2024, 12, 15),
                'jours_ouvrables': 11,
                'statut': 'approuve',
                'motif': 'Congé paternité - naissance de jumeaux',
                'approuve_par': admin_user,
                'date_approbation': date(2024, 11, 28)
            }
        ]

        for data in conges_data:
            if data['personnel'] or data['enseignant']:
                Conge.objects.create(**data)

        print("✓ Congés de test créés avec succès.")
    else:
        print("✓ Congés existants trouvés.")

def create_test_contrats():
    """Créer des contrats de test"""
    if not Contrat.objects.exists():
        print("Création de contrats de test...")

        enseignants = list(Enseignant.objects.all())
        personnel = list(PersonnelAdministratif.objects.all())

        contrats_data = [
            {
                'personnel': personnel[0] if personnel else None,
                'enseignant': None,
                'type_contrat': 'CDI',
                'date_debut': date(2023, 9, 1),
                'date_fin': None,
                'salaire_brut': Decimal('2500.00'),
                'devise': '$',
                'fonction': 'Directeur Administratif',
                'heures_semaine': 40,
                'statut': 'actif'
            },
            {
                'personnel': None,
                'enseignant': enseignants[0] if enseignants else None,
                'type_contrat': 'CDI',
                'date_debut': date(2023, 9, 1),
                'date_fin': None,
                'salaire_brut': Decimal('2200.00'),
                'devise': '$',
                'fonction': 'Professeur de Mathématiques',
                'heures_semaine': 35,
                'statut': 'actif'
            },
            {
                'personnel': personnel[1] if len(personnel) > 1 else None,
                'enseignant': None,
                'type_contrat': 'CDD',
                'date_debut': date(2024, 1, 15),
                'date_fin': date(2024, 12, 31),
                'salaire_brut': Decimal('1800.00'),
                'devise': '$',
                'fonction': 'Secrétaire Administrative',
                'heures_semaine': 35,
                'statut': 'actif'
            },
            {
                'personnel': None,
                'enseignant': enseignants[1] if len(enseignants) > 1 else None,
                'type_contrat': 'CDD',
                'date_debut': date(2024, 2, 1),
                'date_fin': date(2025, 1, 31),
                'salaire_brut': Decimal('2000.00'),
                'devise': '$',
                'fonction': 'Professeur de Français',
                'heures_semaine': 30,
                'statut': 'actif'
            },
            {
                'personnel': personnel[2] if len(personnel) > 2 else None,
                'enseignant': None,
                'type_contrat': 'CTT',
                'date_debut': date(2024, 3, 1),
                'date_fin': date(2024, 8, 31),
                'salaire_brut': Decimal('1500.00'),
                'devise': '$',
                'fonction': 'Agent de Maintenance',
                'heures_semaine': 40,
                'statut': 'actif'
            }
        ]

        for data in contrats_data:
            if data['personnel'] or data['enseignant']:
                Contrat.objects.create(**data)

        print("✓ Contrats de test créés avec succès.")
    else:
        print("✓ Contrats existants trouvés.")

def create_test_formations():
    """Créer des formations de test"""
    if not Formation.objects.exists():
        print("Création de formations de test...")

        formations_data = [
            {
                'intitule': 'Formation Pédagogique - Méthodes d\'Enseignement Modernes',
                'type_formation': 'pedagogique',
                'description': 'Formation complète sur les nouvelles méthodes d\'enseignement et l\'utilisation des technologies en classe',
                'objectifs': 'Maîtriser les techniques d\'enseignement modernes, intégrer les TIC dans l\'enseignement, améliorer l\'engagement des élèves',
                'date_debut': date(2024, 6, 15),
                'date_fin': date(2024, 6, 20),
                'lieu': 'Centre de Formation Pédagogique de Kinshasa',
                'formateur': 'Dr. Marie Nzuzi',
                'organisateur': 'Ministère de l\'Éducation',
                'cout': Decimal('500.00'),
                'devise': 'USD',
                'statut': 'realise'
            },
            {
                'intitule': 'Formation Technique - Gestion Administrative Scolaire',
                'type_formation': 'technique',
                'description': 'Formation sur les outils de gestion administrative et la planification scolaire',
                'objectifs': 'Maîtriser les logiciels de gestion scolaire, optimiser les processus administratifs, améliorer la communication interne',
                'date_debut': date(2024, 7, 10),
                'date_fin': date(2024, 7, 12),
                'lieu': 'Institut de Formation Administrative',
                'formateur': 'M. Jean-Pierre Mwamba',
                'organisateur': 'Association des Administrateurs Scolaires',
                'cout': Decimal('300.00'),
                'devise': 'USD',
                'statut': 'realise'
            },
            {
                'intitule': 'Formation Administrative - Comptabilité Scolaire',
                'type_formation': 'administrative',
                'description': 'Formation spécialisée en comptabilité et gestion financière pour établissements scolaires',
                'objectifs': 'Maîtriser la comptabilité scolaire, gérer les budgets, préparer les rapports financiers',
                'date_debut': date(2024, 8, 20),
                'date_fin': date(2024, 8, 25),
                'lieu': 'École Supérieure de Commerce',
                'formateur': 'Mme. Claire Bemba',
                'organisateur': 'Ordre des Comptables du Congo',
                'cout': Decimal('400.00'),
                'devise': 'USD',
                'statut': 'en_cours'
            },
            {
                'intitule': 'Formation Pédagogique - Évaluation des Apprentissages',
                'type_formation': 'pedagogique',
                'description': 'Formation sur les méthodes d\'évaluation modernes et l\'élaboration d\'outils d\'évaluation',
                'objectifs': 'Concevoir des évaluations pertinentes, utiliser les grilles d\'évaluation, analyser les résultats',
                'date_debut': date(2024, 9, 15),
                'date_fin': date(2024, 9, 17),
                'lieu': 'Centre de Formation des Enseignants',
                'formateur': 'Prof. Antoine Kabila',
                'organisateur': 'Syndicat des Enseignants',
                'cout': Decimal('250.00'),
                'devise': 'USD',
                'statut': 'planifie'
            },
            {
                'intitule': 'Formation Technique - Maintenance Informatique',
                'type_formation': 'technique',
                'description': 'Formation sur la maintenance des équipements informatiques et la résolution de problèmes techniques',
                'objectifs': 'Diagnostiquer les problèmes informatiques, effectuer la maintenance préventive, gérer le parc informatique',
                'date_debut': date(2024, 10, 5),
                'date_fin': date(2024, 10, 10),
                'lieu': 'Institut Technique de Kinshasa',
                'formateur': 'Ing. Paul Lumumba',
                'organisateur': 'Association des Techniciens Informatiques',
                'cout': Decimal('600.00'),
                'devise': 'USD',
                'statut': 'planifie'
            }
        ]

        for data in formations_data:
            Formation.objects.create(**data)

        print("✓ Formations de test créées avec succès.")
    else:
        print("✓ Formations existantes trouvées.")

def create_test_participations():
    """Créer des participations de test"""
    if not ParticipationFormation.objects.exists():
        print("Création de participations de test...")

        formations = list(Formation.objects.all())
        enseignants = list(Enseignant.objects.all())
        personnel = list(PersonnelAdministratif.objects.all())

        participations_data = [
            {
                'formation': formations[0] if formations else None,
                'enseignant': enseignants[0] if enseignants else None,
                'personnel': None,
                'statut_participation': 'present',
                'evaluation_formateur': 'Excellente formatrice, très compétente et pédagogue. Méthodes d\'enseignement claires et pratiques.',
                'evaluation_formation': 'Formation très enrichissante. J\'ai appris de nouvelles techniques que j\'applique déjà en classe. Recommandée à tous les enseignants.'
            },
            {
                'formation': formations[0] if formations else None,
                'enseignant': enseignants[1] if len(enseignants) > 1 else None,
                'personnel': None,
                'statut_participation': 'present',
                'evaluation_formateur': 'Formateur compétent avec une bonne maîtrise du sujet. Explications claires et exemples concrets.',
                'evaluation_formation': 'Formation utile mais pourrait être plus approfondie sur certains aspects techniques.'
            },
            {
                'formation': formations[1] if len(formations) > 1 else None,
                'enseignant': None,
                'personnel': personnel[0] if personnel else None,
                'statut_participation': 'present',
                'evaluation_formateur': 'Formateur très professionnel avec une grande expérience dans le domaine administratif.',
                'evaluation_formation': 'Formation excellente qui m\'a permis d\'améliorer significativement mes compétences administratives.'
            },
            {
                'formation': formations[1] if len(formations) > 1 else None,
                'enseignant': None,
                'personnel': personnel[1] if len(personnel) > 1 else None,
                'statut_participation': 'absent',
                'evaluation_formateur': '',
                'evaluation_formation': ''
            },
            {
                'formation': formations[2] if len(formations) > 2 else None,
                'enseignant': None,
                'personnel': personnel[2] if len(personnel) > 2 else None,
                'statut_participation': 'present',
                'evaluation_formateur': 'Formatrice très compétente en comptabilité. Exemples pratiques très utiles.',
                'evaluation_formation': 'Formation de qualité qui répond parfaitement aux besoins du secteur éducatif.'
            }
        ]

        for data in participations_data:
            if data['formation'] and (data['enseignant'] or data['personnel']):
                ParticipationFormation.objects.create(**data)

        print("✓ Participations de test créées avec succès.")
    else:
        print("✓ Participations existantes trouvées.")

def main():
    """Fonction principale"""
    print("=== Création des données de test administratives ===")

    # Créer les données de base nécessaires
    create_test_users()
    create_test_enseignants()
    create_test_personnel()

    # Créer les données spécifiques aux modules administratifs
    create_test_conges()
    create_test_contrats()
    create_test_formations()
    create_test_participations()

    print("\n=== Création terminée! ===")
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
