# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class UtilisateurManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError(_('Le nom d\'utilisateur doit être défini'))
        email = self.normalize_email(email) if email else None
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('statut', 'actif')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Le superutilisateur doit avoir is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Le superutilisateur doit avoir is_superuser=True.'))

        return self.create_user(username, email, password, **extra_fields)

class Utilisateur(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Administrateur')
        ENSEIGNANT = 'enseignant', _('Enseignant')
        PERSONNEL = 'personnel', _('Personnel administratif')
        PARENT = 'parent', _('Parent/Tuteur')
        ELEVE = 'eleve', _('Élève')

    class Statut(models.TextChoices):
        ACTIF = 'actif', _('Actif')
        SUSPENDU = 'suspendu', _('Suspendu')

    username = models.CharField(
        _('nom d\'utilisateur'),
        max_length=150,
        unique=True,
        help_text=_('150 caractères maximum. Lettres, chiffres et @/./+/-/_ seulement.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("Un utilisateur avec ce nom d'utilisateur existe déjà."),
        },
    )
    email = models.EmailField(_('adresse email'), blank=True, default='')
    postnom = models.CharField(_('postnom'), max_length=100, blank=True, null=True)

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Le numéro de téléphone doit être au format: '+999999999'. Jusqu'à 15 chiffres.")
    )
    telephone = models.CharField(
        _('téléphone'), 
        max_length=20, 
        blank=True, 
        null=True, 
        validators=[phone_regex]
    )
    
    adresse = models.TextField(_('adresse'), blank=True, null=True)
    date_naissance = models.DateField(_('date de naissance'), blank=True, null=True)
    
    role = models.CharField(
        _('rôle'),
        max_length=20,
        choices=Role.choices,
        default=Role.ELEVE,
        db_index=True
    )
    
    statut = models.CharField(
        _('statut'),
        max_length=20,
        choices=Statut.choices,
        default=Statut.ACTIF,
        db_index=True
    )
    
    date_creation = models.DateTimeField(_('date de création'), default=timezone.now)
    dernier_login = models.DateTimeField(_('dernière connexion'), blank=True, null=True)
    photo_profil = models.ImageField(
        _('photo de profil'),
        upload_to='profils/',
        blank=True,
        null=True,
        max_length=255
    )

    objects = UtilisateurManager()

    class Meta:
        verbose_name = _('utilisateur')
        verbose_name_plural = _('utilisateurs')
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['role']),
            models.Index(fields=['statut']),
        ]

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})" if self.get_full_name() else self.username

    def clean(self):
        """Validation supplémentaire"""
        super().clean()
        if self.role == self.Role.ADMIN and not self.is_superuser:
            self.is_staff = True  # Les admins sont automatiquement staff

    def save(self, *args, **kwargs):
        self.clean()
        
        # Formatage cohérent des noms
        if self.first_name:
            self.first_name = self.first_name.strip().title()
        if self.last_name:
            self.last_name = self.last_name.strip().upper()
        if self.postnom:
            self.postnom = self.postnom.strip().upper()
        
        # Synchronisation statut/is_active
        if self.statut == self.Statut.SUSPENDU:
            self.is_active = False
        else:
            self.is_active = True
            
        super().save(*args, **kwargs)

    @property
    def nom_complet(self):
        """Retourne le nom complet formaté"""
        names = filter(None, [self.first_name, self.last_name, self.postnom])
        return ' '.join(names).strip() or self.username

    # Méthodes de vérification de rôle
    def is_admin(self):
        return self.role == self.Role.ADMIN or self.is_superuser
    
    def is_enseignant(self):
        return self.role == self.Role.ENSEIGNANT
    
    def is_personnel(self):
        return self.role == self.Role.PERSONNEL
    
    def is_parent(self):
        return self.role == self.Role.PARENT
    
    def is_eleve(self):
        return self.role == self.Role.ELEVE

    def has_module_perms(self, app_label):
        """Est-ce que l'utilisateur a des permissions pour voir cette app?"""
        if self.is_active and (self.is_staff or self.is_superuser):
            return True
        return super().has_module_perms(app_label)

    def get_role_color(self):
        """Retourne la couleur Bootstrap associée au rôle"""
        colors = {
            self.Role.ADMIN: 'danger',
            self.Role.ENSEIGNANT: 'primary',
            self.Role.PERSONNEL: 'success',
            self.Role.PARENT: 'warning',
            self.Role.ELEVE: 'secondary'
        }
        return colors.get(self.role, 'secondary')
