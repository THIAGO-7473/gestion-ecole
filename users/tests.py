from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Utilisateur
from django.core.files.uploadedfile import SimpleUploadedFile

class UtilisateurTests(TestCase):
    def setUp(self):
        """Configuration initiale pour tous les tests"""
        # Créer un superutilisateur pour les tests
        self.admin = Utilisateur.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123',
            first_name='Admin',
            last_name='Test',
            role='admin'
        )

        # Créer un utilisateur normal pour les tests
        self.user = Utilisateur.objects.create_user(
            username='user',
            email='user@test.com',
            password='user123',
            first_name='User',
            last_name='Test',
            role='enseignant'
        )

        self.client = Client()

    def test_1_login_success(self):
        """Test de connexion réussie"""
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'admin123'
        })
        self.assertEqual(response.status_code, 302)  # Redirection après connexion
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_2_login_failure(self):
        """Test de connexion échouée"""
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Reste sur la page de login
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_3_create_user(self):
        """Test de création d'un nouvel utilisateur"""
        self.client.login(username='admin', password='admin123')
        response = self.client.post(reverse('utilisateur_create'), {
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password1': 'newuser123',
            'password2': 'newuser123',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'enseignant',
            'statut': 'actif'
        })
        self.assertEqual(response.status_code, 302)  # Redirection après création
        self.assertTrue(Utilisateur.objects.filter(username='newuser').exists())

    def test_4_update_user(self):
        """Test de mise à jour d'un utilisateur"""
        self.client.login(username='admin', password='admin123')
        response = self.client.post(
            reverse('utilisateur_update', kwargs={'pk': self.user.pk}),
            {
                'username': 'updateduser',
                'email': 'updated@test.com',
                'first_name': 'Updated',
                'last_name': 'User',
                'role': 'personnel',
                'statut': 'actif'
            }
        )
        self.assertEqual(response.status_code, 302)
        updated_user = Utilisateur.objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.username, 'updateduser')

    def test_5_delete_user(self):
        """Test de suppression d'un utilisateur"""
        self.client.login(username='admin', password='admin123')
        response = self.client.post(
            reverse('utilisateur_delete', kwargs={'pk': self.user.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Utilisateur.objects.filter(pk=self.user.pk).exists())

    def test_6_user_list_view(self):
        """Test de la vue liste des utilisateurs"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('utilisateur_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/utilisateur_list.html')
        self.assertContains(response, 'admin')
        self.assertContains(response, 'user')

    def test_7_export_users_csv(self):
        """Test d'export des utilisateurs en CSV"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('export_users_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertTrue('attachment; filename="utilisateurs.csv"' in response['Content-Disposition'])

    def test_8_user_photo_upload(self):
        """Test de téléchargement de photo de profil"""
        self.client.login(username='admin', password='admin123')
        image = SimpleUploadedFile(
            "test_image.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        response = self.client.post(
            reverse('utilisateur_update', kwargs={'pk': self.user.pk}),
            {
                'username': 'user',
                'email': 'user@test.com',
                'first_name': 'User',
                'last_name': 'Test',
                'role': 'enseignant',
                'statut': 'actif',
                'photo_profil': image
            }
        )
        self.assertEqual(response.status_code, 302)
        updated_user = Utilisateur.objects.get(pk=self.user.pk)
        self.assertTrue(updated_user.photo_profil)

    def test_9_user_search(self):
        """Test de recherche d'utilisateurs"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('utilisateur_list') + '?search=admin')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'admin')
        self.assertNotContains(response, 'user')

    def test_10_user_role_filter(self):
        """Test de filtrage des utilisateurs par rôle"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('utilisateur_list') + '?role=enseignant')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'user')
        self.assertNotContains(response, 'admin')
