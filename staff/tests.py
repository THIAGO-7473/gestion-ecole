from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import (
    PersonnelAdministratif, Enseignant, SpecialiteEnseignant,
    DocumentPersonnel, Tuteur, Sanction, FichierPreuve
)
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
import datetime

class StaffManagementTests(TestCase):
    def setUp(self):
        """Configuration initiale pour tous les tests"""
        # Créer un utilisateur admin
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )

        # Créer un client pour les tests
        self.client = Client()
        self.client.login(username='admin', password='admin123')

        # Créer un personnel administratif de test
        self.personnel = PersonnelAdministratif.objects.create(
            nom='Test',
            postnom='Admin',
            prenom='User',
            date_naissance='1990-01-01',
            adresse='123 Test Street',
            telephone='1234567890',
            email='test@test.com',
            role='secretaire',
            statut='actif',
            salaire_base=1000,
            devise='USD'
        )

        # Créer un enseignant de test
        self.enseignant = Enseignant.objects.create(
            matricule='ENS001',
            nom='Test',
            postnom='Teacher',
            prenom='John',
            sexe='M',
            date_naissance='1985-01-01',
            nationalite='Congolaise',
            adresse='456 Teacher Street',
            telephone='0987654321',
            email='teacher@test.com',
            situation_familiale='celibataire',
            date_engagement='2020-01-01',
            anciennete=3,
            anciennete_unite='annees',
            grade_echeant='A',
            acte_nom='Acte 001',
            diplome='Master',
            etat_civil='celibataire',
            cote=80,
            lieu_affectation='Kinshasa',
            statut='actif',
            salaire_base=2000,
            devise='USD',
            charge_horaire=20
        )

        # Créer une spécialité de test
        self.specialite = SpecialiteEnseignant.objects.create(
            enseignant=self.enseignant,
            matiere='Mathématiques',
            niveau_competence='expert',
            annees_experience=5
        )

        # Créer un tuteur de test
        self.tuteur = Tuteur.objects.create(
            nom='Test',
            postnom='Tutor',
            prenom='Mike',
            contact_tuteur='1234567890',
            email='tutor@test.com',
            profession='Ingénieur'
        )

        # Créer un document de test
        self.document = DocumentPersonnel.objects.create(
            titre='Test Document',
            description='Document de test',
            type_document='diplome',
            date_depot=timezone.now().date(),
            enseignant=self.enseignant
        )

        # Créer une sanction de test
        self.sanction = Sanction.objects.create(
            reference='SAN001',
            type_sanction='avertissement_oral',
            motif='Test de sanction',
            date_sanction=timezone.now().date(),
            date_effet=timezone.now().date(),
            statut='en_attente',
            enseignant=self.enseignant,
            donneur_sanction=self.admin
        )

        # Initialiser les compteurs pour le tableau de bord
        self.total_personnel = PersonnelAdministratif.objects.count()
        self.total_enseignants = Enseignant.objects.count()
        self.total_sanctions = Sanction.objects.count()
        self.total_documents = DocumentPersonnel.objects.count()

    def test_1_personnel_creation(self):
        """Test de création d'un personnel administratif"""
        response = self.client.post(reverse('staff:personnel_create'), {
            'nom': 'New',
            'postnom': 'Staff',
            'prenom': 'Member',
            'date_naissance': '1995-01-01',
            'adresse': '789 New Street',
            'telephone': '5555555555',
            'email': 'new@test.com',
            'role': 'comptable',
            'statut': 'actif',
            'salaire_base': 1500,
            'devise': 'USD'
        })
        self.assertEqual(response.status_code, 302)  # Redirection après création
        self.assertTrue(PersonnelAdministratif.objects.filter(nom='New').exists())

    def test_2_personnel_update(self):
        """Test de mise à jour d'un personnel administratif"""
        response = self.client.post(
            reverse('staff:personnel_update', kwargs={'pk': self.personnel.pk}),
            {
                'nom': 'Updated',
                'postnom': 'Staff',
                'prenom': 'Member',
                'date_naissance': '1990-01-01',
                'adresse': '123 Test Street',
                'telephone': '1234567890',
                'email': 'updated@test.com',
                'role': 'secretaire',
                'statut': 'actif',
                'salaire_base': 1200,
                'devise': 'USD'
            }
        )
        self.assertEqual(response.status_code, 302)
        updated_personnel = PersonnelAdministratif.objects.get(pk=self.personnel.pk)
        self.assertEqual(updated_personnel.nom, 'Updated')

    def test_3_enseignant_creation(self):
        """Test de création d'un enseignant"""
        response = self.client.post(reverse('staff:enseignant_create'), {
            'matricule': 'ENS002',
            'nom': 'New',
            'postnom': 'Teacher',
            'prenom': 'Jane',
            'sexe': 'F',
            'date_naissance': '1990-01-01',
            'nationalite': 'Congolaise',
            'adresse': '789 Teacher Street',
            'telephone': '5555555555',
            'email': 'newteacher@test.com',
            'situation_familiale': 'marie',
            'date_engagement': '2023-01-01',
            'anciennete': 1,
            'anciennete_unite': 'annees',
            'grade_echeant': 'B',
            'acte_nom': 'Acte 002',
            'diplome': 'Doctorat',
            'etat_civil': 'marie',
            'cote': 85,
            'lieu_affectation': 'Lubumbashi',
            'statut': 'actif',
            'salaire_base': 2500,
            'devise': 'USD',
            'charge_horaire': 25
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Enseignant.objects.filter(matricule='ENS002').exists())

    def test_4_specialite_creation(self):
        """Test de création d'une spécialité"""
        response = self.client.post(reverse('staff:specialite_create'), {
            'enseignant': self.enseignant.pk,
            'matiere': 'Physique',
            'niveau_competence': 'intermediaire',
            'annees_experience': 3
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(SpecialiteEnseignant.objects.filter(matiere='Physique').exists())

    def test_5_document_creation(self):
        """Test de création d'un document"""
        response = self.client.post(reverse('staff:document_create'), {
            'titre': 'New Document',
            'description': 'New test document',
            'type_document': 'certificat',
            'date_depot': timezone.now().date(),
            'enseignant': self.enseignant.pk
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(DocumentPersonnel.objects.filter(titre='New Document').exists())

    def test_6_tuteur_creation(self):
        """Test de création d'un tuteur"""
        response = self.client.post(reverse('staff:tuteur_create'), {
            'nom': 'New',
            'postnom': 'Tutor',
            'prenom': 'Sarah',
            'contact_tuteur': '5555555555',
            'email': 'newtutor@test.com',
            'profession': 'Médecin'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tuteur.objects.filter(nom='New').exists())

    def test_7_sanction_creation(self):
        """Test de création d'une sanction"""
        response = self.client.post(reverse('staff:sanction_create'), {
            'reference': 'SAN002',
            'type_sanction': 'avertissement_ecrit',
            'motif': 'Nouvelle sanction de test',
            'date_sanction': timezone.now().date(),
            'date_effet': timezone.now().date(),
            'statut': 'en_attente',
            'enseignant': self.enseignant.pk,
            'donneur_sanction': self.admin.pk
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Sanction.objects.filter(reference='SAN002').exists())

    def test_8_sanction_validation(self):
        """Test de validation d'une sanction"""
        response = self.client.post(
            reverse('staff:valider_sanction', kwargs={'pk': self.sanction.pk})
        )
        self.assertEqual(response.status_code, 302)
        updated_sanction = Sanction.objects.get(pk=self.sanction.pk)
        self.assertEqual(updated_sanction.statut, 'appliquee')

    def test_9_sanction_annulation(self):
        """Test d'annulation d'une sanction"""
        response = self.client.post(
            reverse('staff:annuler_sanction', kwargs={'pk': self.sanction.pk})
        )
        self.assertEqual(response.status_code, 302)
        updated_sanction = Sanction.objects.get(pk=self.sanction.pk)
        self.assertEqual(updated_sanction.statut, 'annulee')

    def test_10_list_views(self):
        """Test des vues de liste"""
        # Test de la liste du personnel
        response = self.client.get(reverse('staff:personnel_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/personnel_list.html')

        # Test de la liste des enseignants
        response = self.client.get(reverse('staff:enseignant_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/enseignant_list.html')

        # Test de la liste des spécialités
        response = self.client.get(reverse('staff:specialite_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/specialite_list.html')

        # Test de la liste des documents
        response = self.client.get(reverse('staff:document_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/document_list.html')

        # Test de la liste des tuteurs
        response = self.client.get(reverse('staff:tuteur_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/tuteur_list.html')

        # Test de la liste des sanctions
        response = self.client.get(reverse('staff:sanction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/sanction_list.html')

    def test_11_search_functionality(self):
        """Test de la fonctionnalité de recherche"""
        # Recherche dans la liste du personnel
        response = self.client.get(reverse('staff:personnel_list') + '?search=Test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')

        # Recherche dans la liste des enseignants
        response = self.client.get(reverse('staff:enseignant_list') + '?search=Teacher')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Teacher')

    def test_12_export_functionality(self):
        """Test des fonctionnalités d'export"""
        # Export du personnel en CSV
        response = self.client.get(reverse('staff:export_personnel', kwargs={'format_type': 'csv'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')

        # Export des enseignants en Excel
        response = self.client.get(reverse('staff:export_enseignant', kwargs={'format': 'xlsx'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def test_13_dashboard_view(self):
        """Test de la vue tableau de bord"""
        response = self.client.get(reverse('staff:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'staff/dashboard.html')
        self.assertContains(response, str(self.total_personnel))
        self.assertContains(response, str(self.total_enseignants))
        self.assertContains(response, str(self.total_sanctions))
        self.assertContains(response, str(self.total_documents))
