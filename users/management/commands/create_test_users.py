from django.core.management.base import BaseCommand
from users.models import Utilisateur

class Command(BaseCommand):
    help = 'Crée des utilisateurs de test dans la base de données'

    def handle(self, *args, **kwargs):
        # Créer un superutilisateur
        if not Utilisateur.objects.filter(username='admin').exists():
            admin = Utilisateur.objects.create_superuser(
                username='admin',
                email='admin@test.com',
                password='admin123',
                first_name='Admin',
                last_name='Test',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS(f'Superutilisateur créé : {admin.username}'))

        # Créer un utilisateur enseignant
        if not Utilisateur.objects.filter(username='enseignant').exists():
            enseignant = Utilisateur.objects.create_user(
                username='enseignant',
                email='enseignant@test.com',
                password='enseignant123',
                first_name='Jean',
                last_name='Dupont',
                role='enseignant'
            )
            self.stdout.write(self.style.SUCCESS(f'Enseignant créé : {enseignant.username}'))

        # Créer un utilisateur personnel
        if not Utilisateur.objects.filter(username='personnel').exists():
            personnel = Utilisateur.objects.create_user(
                username='personnel',
                email='personnel@test.com',
                password='personnel123',
                first_name='Marie',
                last_name='Martin',
                role='personnel'
            )
            self.stdout.write(self.style.SUCCESS(f'Personnel créé : {personnel.username}'))

        # Créer un utilisateur parent
        if not Utilisateur.objects.filter(username='parent').exists():
            parent = Utilisateur.objects.create_user(
                username='parent',
                email='parent@test.com',
                password='parent123',
                first_name='Pierre',
                last_name='Durand',
                role='parent'
            )
            self.stdout.write(self.style.SUCCESS(f'Parent créé : {parent.username}'))

        # Créer un utilisateur élève
        if not Utilisateur.objects.filter(username='eleve').exists():
            eleve = Utilisateur.objects.create_user(
                username='eleve',
                email='eleve@test.com',
                password='eleve123',
                first_name='Sophie',
                last_name='Leroy',
                role='eleve'
            )
            self.stdout.write(self.style.SUCCESS(f'Élève créé : {eleve.username}'))
