from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from staff.models import (
    PersonnelAdministratif, Enseignant, SpecialiteEnseignant,
    DocumentPersonnel, Tuteur, Sanction, FichierPreuve
)
from administrative.models import Matiere
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help = 'Génère des données de test pour la gestion du staff'

    def handle(self, *args, **kwargs):
        # Créer un utilisateur admin pour les sanctions
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )

        # Créer des matières pour les spécialités
        matieres = [
            Matiere.objects.create(nom='Mathématiques', code='MATH'),
            Matiere.objects.create(nom='Français', code='FRAN'),
            Matiere.objects.create(nom='Anglais', code='ANGL'),
            Matiere.objects.create(nom='Histoire', code='HIST'),
            Matiere.objects.create(nom='Géographie', code='GEOG'),
        ]

        # Données de test pour le personnel administratif
        personnel_data = [
            {
                'nom': 'Mukeba',
                'postnom': 'Kazadi',
                'prenom': 'Jean',
                'sexe': 'M',
                'date_naissance': '1980-05-15',
                'adresse': 'Avenue Victoire 123, Kinshasa',
                'telephone': '+243 812345678',
                'email': 'jean.mukeba@ecole.com',
                'role': 'directeur',
                'date_embauche': '2015-01-01',
                'salaire_base': 5000,
                'devise': 'FC',
                'statut': 'actif'
            },
            {
                'nom': 'Lubala',
                'postnom': 'Mpoyi',
                'prenom': 'Marie',
                'sexe': 'F',
                'date_naissance': '1985-08-20',
                'adresse': 'Quartier Matonge 45, Kinshasa',
                'telephone': '+243 823456789',
                'email': 'marie.lubala@ecole.com',
                'role': 'secretaire',
                'date_embauche': '2018-03-15',
                'salaire_base': 3000,
                'devise': 'FC',
                'statut': 'actif'
            },
            {
                'nom': 'Tshibanda',
                'postnom': 'Mukeba',
                'prenom': 'Pierre',
                'sexe': 'M',
                'date_naissance': '1975-12-10',
                'adresse': 'Avenue Kasa-Vubu 78, Kinshasa',
                'telephone': '+243 834567890',
                'email': 'pierre.tshibanda@ecole.com',
                'role': 'comptable',
                'date_embauche': '2016-06-01',
                'salaire_base': 4000,
                'devise': 'FC',
                'statut': 'actif'
            }
        ]

        # Créer le personnel administratif
        personnel_list = []
        for data in personnel_data:
            personnel = PersonnelAdministratif.objects.create(**data)
            personnel_list.append(personnel)

        # Données de test pour les enseignants
        enseignants_data = [
            {
                'nom': 'Kazadi',
                'postnom': 'Mukeba',
                'prenom': 'Paul',
                'matricule': 'ENS001',
                'sexe': 'M',
                'date_naissance': '1982-03-25',
                'nationalite': 'Congolaise',
                'adresse': 'Avenue Lumumba 90, Kinshasa',
                'telephone': '+243 845678901',
                'email': 'paul.kazadi@ecole.com',
                'date_engagement': '2017-09-01',
                'diplome': 'Master en Mathématiques',
                'lieu_affectation': 'Kinshasa',
                'statut': 'titulaire',
                'salaire_base': 3500,
                'devise': 'FC',
                'charge_horaire': 20
            },
            {
                'nom': 'Mpoyi',
                'postnom': 'Lubala',
                'prenom': 'Sophie',
                'matricule': 'ENS002',
                'sexe': 'F',
                'date_naissance': '1988-07-15',
                'nationalite': 'Congolaise',
                'adresse': 'Quartier Limete 34, Kinshasa',
                'telephone': '+243 856789012',
                'email': 'sophie.mpoyi@ecole.com',
                'date_engagement': '2019-01-15',
                'diplome': 'Licence en Français',
                'lieu_affectation': 'Kinshasa',
                'statut': 'titulaire',
                'salaire_base': 3200,
                'devise': 'FC',
                'charge_horaire': 18
            },
            {
                'nom': 'Mukeba',
                'postnom': 'Tshibanda',
                'prenom': 'David',
                'matricule': 'ENS003',
                'sexe': 'M',
                'date_naissance': '1990-11-30',
                'nationalite': 'Congolaise',
                'adresse': 'Avenue Victoire 56, Kinshasa',
                'telephone': '+243 867890123',
                'email': 'david.mukeba@ecole.com',
                'date_engagement': '2020-03-01',
                'diplome': 'Master en Anglais',
                'lieu_affectation': 'Kinshasa',
                'statut': 'vacataire',
                'salaire_base': 2800,
                'devise': 'FC',
                'charge_horaire': 15
            }
        ]

        # Créer les enseignants
        enseignants_list = []
        for data in enseignants_data:
            enseignant = Enseignant.objects.create(**data)
            enseignants_list.append(enseignant)

        # Créer des spécialités pour les enseignants
        specialites_data = [
            {'enseignant': enseignants_list[0], 'matiere': matieres[0], 'niveau_competence': 'expert', 'annees_experience': 10},
            {'enseignant': enseignants_list[1], 'matiere': matieres[1], 'niveau_competence': 'expert', 'annees_experience': 8},
            {'enseignant': enseignants_list[2], 'matiere': matieres[2], 'niveau_competence': 'intermediaire', 'annees_experience': 5},
        ]

        for data in specialites_data:
            SpecialiteEnseignant.objects.create(**data)

        # Créer des documents
        documents_data = [
            {
                'type_document': 'diplome',
                'titre': 'Diplôme Master Mathématiques',
                'description': 'Diplôme de Master en Mathématiques',
                'date_depot': timezone.now().date(),
                'enseignant': enseignants_list[0],
                'statut': 'valide'
            },
            {
                'type_document': 'diplome',
                'titre': 'Diplôme Licence Français',
                'description': 'Diplôme de Licence en Français',
                'date_depot': timezone.now().date(),
                'enseignant': enseignants_list[1],
                'statut': 'valide'
            }
        ]

        for data in documents_data:
            DocumentPersonnel.objects.create(**data)

        # Créer des tuteurs
        tuteurs_data = [
            {
                'nom': 'Mukeba',
                'postnom': 'Kazadi',
                'prenom': 'Joseph',
                'contact_tuteur': '+243 878901234',
                'email': 'joseph.mukeba@example.com',
                'profession': 'Ingénieur'
            },
            {
                'nom': 'Lubala',
                'postnom': 'Mpoyi',
                'prenom': 'Catherine',
                'contact_tuteur': '+243 889012345',
                'email': 'catherine.lubala@example.com',
                'profession': 'Médecin'
            }
        ]

        for data in tuteurs_data:
            Tuteur.objects.create(**data)

        # Créer des sanctions
        sanctions_data = [
            {
                'enseignant': enseignants_list[0],
                'type_sanction': 'avertissement_oral',
                'date_sanction': timezone.now().date(),
                'date_effet': timezone.now().date(),
                'motif': 'Retard répété aux cours',
                'donneur_sanction': 'prefet_etudes',
                'statut': 'appliquee',
                'validation_par': admin_user
            },
            {
                'enseignant': enseignants_list[1],
                'type_sanction': 'avertissement_ecrit',
                'date_sanction': timezone.now().date(),
                'date_effet': timezone.now().date(),
                'motif': 'Absence non justifiée',
                'donneur_sanction': 'directeur_etudes',
                'statut': 'en_attente'
            }
        ]

        for data in sanctions_data:
            Sanction.objects.create(**data)

        self.stdout.write(self.style.SUCCESS('Données de test créées avec succès!'))
