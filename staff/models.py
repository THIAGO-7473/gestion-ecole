# staff/models.py
from django.db import models
from django.core.validators import MinValueValidator
from users.models import Utilisateur
from django.utils import timezone
from django.core.exceptions import ValidationError




class PersonnelAdministratif(models.Model):
    ROLE_CHOICES = [
        ('directeur', 'Directeur'),
        ('prefet', 'Préfet'),
        ('directeur_etudes', 'Directeur des Études'),
        ('disciplinaire', 'Disciplinaire'),
        ('secretaire', 'Secrétaire'),
        ('comptable', 'Comptable'),
        ('administratif', 'Administratif'),
    ]
    
    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('suspendu', 'Suspendu'),
        ('congé', 'Congé'),
        ('inactif', 'Inactif'),
    ]
    
    DEVISE_CHOICES = [
        ('FC', 'Franc Congolais'),
        ('$', 'Dollar Américain'),
        ('Shs', 'Shillings Ougandais'),
    ]
    
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    
    photo = models.ImageField(upload_to='personnel/', null=True, blank=True)
    nom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=10, choices=SEXE_CHOICES)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100, null=True, blank=True)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    specialite = models.CharField(max_length=100, blank=True, null=True)
    date_embauche = models.DateField()
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2)
    devise = models.CharField(max_length=3, choices=DEVISE_CHOICES, default='FC')
    numero_secu = models.CharField(max_length=50, null=True, blank=True, verbose_name="N° DE SÉCURITÉ SOCIALE")
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='actif')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Personnel Administratif"
        verbose_name_plural = "Personnel Administratif"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name()} - {self.get_role_display()}"

    def get_full_name(self):
        return f"{self.nom} {self.postnom} {self.prenom}"

class Enseignant(models.Model):
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    
    STATUT_CHOICES = [
        ('titulaire', 'Titulaire'),
        ('vacataire', 'Vacataire'),
        ('stagiaire', 'Stagiaire'),
        ('contractuel', 'Contractuel'),
    ]

    DEVISE_CHOICES = [
        ('FC', 'Franc Congolais'),
        ('$', 'Dollar Américain'),
        ('Shs', 'Shillings Ougandais'),
    ]

    ANCIENNETE_UNITE_CHOICES = [
        ('semaines', 'Semaines'),
        ('mois', 'Mois'),
        ('annees', 'Années'),
    ]
    
    nom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    matricule = models.CharField(max_length=50, unique=True)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    date_naissance = models.DateField()
    nationalite = models.CharField(max_length=50)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    situation_familiale = models.CharField(max_length=50, blank=True, null=True)
    date_engagement = models.DateField()
    anciennete = models.IntegerField(blank=True, null=True)
    anciennete_unite = models.CharField(max_length=10, choices=ANCIENNETE_UNITE_CHOICES, default='annees')
    anciennete_grade = models.IntegerField(blank=True, null=True)
    anciennete_grade_unite = models.CharField(max_length=10, choices=ANCIENNETE_UNITE_CHOICES, default='annees')
    grade_echeant = models.CharField(max_length=50, blank=True, null=True)
    acte_nom = models.CharField(max_length=100, blank=True, null=True)
    diplome = models.CharField(max_length=100)
    etat_civil = models.CharField(max_length=50, blank=True, null=True)
    cote = models.FloatField(blank=True, null=True)
    lieu_affectation = models.CharField(max_length=100)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)
    salaire_base = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    devise = models.CharField(max_length=3, choices=DEVISE_CHOICES, default='FC')
    charge_horaire = models.IntegerField()
    photo = models.ImageField(upload_to='enseignants/photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        return f"{self.nom} {self.postnom} {self.prenom}"

    def __str__(self):
        return self.get_full_name()

    def calculer_anciennete(self):
        if self.date_engagement:
            delta = timezone.now().date() - self.date_engagement
            if self.anciennete_unite == 'semaines':
                return delta.days // 7
            elif self.anciennete_unite == 'mois':
                return delta.days // 30
            else:  # annees
                return delta.days // 365
        return 0

    def get_anciennete_display(self):
        if self.anciennete is not None:
            if self.anciennete_unite == 'semaines':
                return f"{self.anciennete} Semaine{'s' if self.anciennete > 1 else ''}"
            elif self.anciennete_unite == 'mois':
                return f"{self.anciennete} Mois"
            else:  # annees
                return f"{self.anciennete} An{'s' if self.anciennete > 1 else ''}"
        return ""

    def get_anciennete_grade_display(self):
        if self.anciennete_grade is not None:
            if self.anciennete_grade_unite == 'semaines':
                return f"{self.anciennete_grade} Semaine{'s' if self.anciennete_grade > 1 else ''}"
            elif self.anciennete_grade_unite == 'mois':
                return f"{self.anciennete_grade} Mois"
            else:  # annees
                return f"{self.anciennete_grade} An{'s' if self.anciennete_grade > 1 else ''}"
        return ""

    def get_cote_display(self):
        if self.cote is not None:
            return f"{self.cote} %"
        return ""

    def get_salaire_display(self):
        if self.salaire_base is not None:
            return f"{self.salaire_base} {self.devise}"
        return ""

class SpecialiteEnseignant(models.Model):
    NIVEAU_CHOICES = [
        ('debutant', 'Débutant'),
        ('intermediaire', 'Intermédiaire'),
        ('expert', 'Expert'),
    ]
    
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    matiere = models.ForeignKey('administrative.Matiere', on_delete=models.CASCADE)
    niveau_competence = models.CharField(max_length=20, choices=NIVEAU_CHOICES)
    annees_experience = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('enseignant', 'matiere')

    def __str__(self):
        return f"{self.enseignant} - {self.matiere} ({self.get_niveau_competence_display()})"

class DocumentPersonnel(models.Model):
    TYPE_CHOICES = [
        ('diplome', 'Diplôme'),
        ('attestation', 'Attestation'),
        ('cv', 'CV'),
        ('autre', 'Autre'),
    ]
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
        ('expire', 'Expiré'),
    ]
    
    type_document = models.CharField(max_length=100)
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date_depot = models.DateField()
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, null=True, blank=True)
    personnel = models.ForeignKey(PersonnelAdministratif, on_delete=models.CASCADE, null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.enseignant and not self.personnel:
            raise ValidationError("Un document doit être lié à un enseignant ou à un personnel administratif.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.titre} - {self.get_type_document_display()}"

class FichierDocument(models.Model):
    document = models.ForeignKey(DocumentPersonnel, on_delete=models.CASCADE, related_name='fichiers')
    fichier = models.FileField(upload_to='documents/')
    nom_fichier = models.CharField(max_length=255)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom_fichier
    
class Tuteur(models.Model):
    nom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    contact_tuteur = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.nom} {self.postnom} {self.prenom}"

class Sanction(models.Model):
    TYPE_CHOICES = [
        ('avertissement_oral', 'Avertissement oral'),
        ('avertissement_ecrit', 'Avertissement écrit'),
        ('blame', 'Blâme'),
        ('retenue_salaire', 'Retenue sur salaire'),
        ('suspension', 'Suspension'),
        ('licenciement', 'Licenciement'),
        ('autre', 'Autre'),
    ]
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('appliquee', 'Appliquée'),
        ('annulee', 'Annulée'),
        ('contestee', 'Contestée'),
    ]

    DONNEUR_SANCTION_CHOICES = [
        ('prefet_etudes', 'Préfet des études'),
        ('secretaire', 'Secrétaire'),
        ('promoteur', 'Promoteur'),
        ('directeur_etudes', 'Directeur des études'),
    ]

    DUREE_UNITE_CHOICES = [
        ('jours', 'Jour(s)'),
        ('mois', 'Mois'),
        ('annees', 'Année(s)'),
    ]

    DEVISE_CHOICES = [
        ('FC', 'Franc Congolais'),
        ('$', 'Dollar Américain'),
        ('Shs', 'Shillings Ougandais'),
    ]
    
    enseignant = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, blank=True, null=True)
    personnel = models.ForeignKey(PersonnelAdministratif, on_delete=models.SET_NULL, blank=True, null=True)
    type_sanction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_sanction = models.DateField()
    date_effet = models.DateField()
    motif = models.TextField()
    duree = models.IntegerField(blank=True, null=True)
    duree_unite = models.CharField(max_length=10, choices=DUREE_UNITE_CHOICES, default='jours')
    montant_retenue = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    devise = models.CharField(max_length=3, choices=DEVISE_CHOICES, default='FC')
    reference = models.CharField(max_length=50, unique=True, blank=True)
    donneur_sanction = models.CharField(max_length=20, choices=DONNEUR_SANCTION_CHOICES)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    document_path = models.CharField(max_length=255, blank=True, null=True)
    date_validation = models.DateField(blank=True, null=True)
    validation_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, blank=True, null=True, related_name='sanctions_validees')
    observations = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_reference(self):
        prefix = 'SAN'
        year = timezone.now().strftime('%Y')
        month = timezone.now().strftime('%m')
        
        # Obtenir le dernier numéro de séquence pour ce mois
        last_sanction = Sanction.objects.filter(
            reference__startswith=f'{prefix}{year}{month}'
        ).order_by('-reference').first()
        
        if last_sanction:
            last_seq = int(last_sanction.reference[-4:])
            new_seq = last_seq + 1
        else:
            new_seq = 1
            
        return f'{prefix}{year}{month}{new_seq:04d}'

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self.generate_reference()
        super().save(*args, **kwargs)

    def clean(self):
        if not (self.enseignant or self.personnel):
            raise ValidationError("Une sanction doit être liée soit à un enseignant, soit à un personnel")
        if self.enseignant and self.personnel:
            raise ValidationError("Une sanction ne peut être liée à la fois à un enseignant et un personnel")
        if self.date_sanction > self.date_effet:
            raise ValidationError("La date d'effet doit être postérieure ou égale à la date de sanction")
        
        # Validation spécifique au type de sanction
        if self.type_sanction == 'retenue_salaire' and not self.montant_retenue:
            raise ValidationError("Un montant doit être spécifié pour les retenues sur salaire")
        if self.type_sanction == 'suspension' and not self.duree:
            raise ValidationError("Une durée doit être spécifiée pour les suspensions")

    def get_donneur_sanction_display(self):
        return dict(self.DONNEUR_SANCTION_CHOICES).get(self.donneur_sanction, '')

    def __str__(self):
        return f"Sanction {self.reference} - {self.get_type_sanction_display()}"

class FichierPreuve(models.Model):
    sanction = models.ForeignKey(Sanction, on_delete=models.CASCADE, related_name='fichiers_preuves')
    fichier = models.FileField(upload_to='sanctions/preuves/')
    date_ajout = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Preuve pour {self.sanction} - {self.fichier.name}"

    class Meta:
        verbose_name = "Fichier de preuve"
        verbose_name_plural = "Fichiers de preuves"