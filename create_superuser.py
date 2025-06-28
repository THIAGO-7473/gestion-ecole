import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
django.setup()

from users.models import Utilisateur

# Créer le superutilisateur
if not Utilisateur.objects.filter(username='admin').exists():
    admin = Utilisateur.objects.create_superuser(
        username='admin',
        email='admin@test.com',
        password='admin123',
        first_name='Admin',
        last_name='Test',
        role='admin'
    )
    print(f"Superutilisateur créé : {admin.username}")
else:
    print("Le superutilisateur existe déjà")
