# finance/models.py
import random
import string
from datetime import datetime
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator
from administrative.models import Eleve
from staff.models import Enseignant
from users.models import Utilisateur
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


DEVISE_CHOICES = [
    ('FC', 'Franc Congolais'),
    ('$', 'Dollar Américain'),
    ('Shs', 'Shillings Ougandais'),
]

def generate_facture_reference():
    """Génère une référence de facture unique (format: FACT-AAAAMMJJ-XXXX)"""
    date_part = datetime.now().strftime("%Y%m%d")
    random_part = ''.join(random.choices(string.ascii_uppercase, k=4))
    return f"FACT-{date_part}-{random_part}"

class Facture(models.Model):
    class Statut(models.TextChoices):
        PAYEE = 'payee', 'Payée'
        NON_PAYEE = 'non_payee', 'Non payée'
        PARTIELLE = 'partielle', 'Partiellement payée'
        ANNULEE = 'annulee', 'Annulée'
    
    class TypeFacture(models.TextChoices):
        SCOLARITE = 'frais_scolarite', 'Frais de scolarité'
        INSCRIPTION = 'inscription', 'Frais d\'inscription'
        SALAIRE = 'salaires', 'Salaires enseignants'
        FOURNITURE = 'fournitures', 'Fournitures scolaires'
        AUTRE = 'autre', 'Autre'

    # Champs de base
    reference = models.CharField(
        max_length=20,
        unique=True,
        default=generate_facture_reference,
        validators=[
            RegexValidator(
                regex=r'^FACT-\d{8}-[A-Z]{4}$',
                message="Format de référence invalide (ex: FACT-20240515-ABCD)"
            )
        ],
        editable=False,
        verbose_name="Référence",
        help_text="Numéro unique généré automatiquement"
    )
    
    date_emission = models.DateField(
        auto_now_add=True,
        verbose_name="Date d'émission"
    )
    
    date_echeance = models.DateField(
        verbose_name="Date d'échéance",
        null=True,
        blank=True
    )
    
    montant = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Montant TTC"
    )
    
    devise = models.CharField(
        max_length=3,
        choices=DEVISE_CHOICES,
        default='FC',
        verbose_name="Devise"
    )
    
    fichiers = models.ManyToManyField(
        'FichierFacture',
        related_name='factures',
        blank=True,
        verbose_name="Fichiers joints"
    )
    
    statut = models.CharField(
        max_length=20,
        choices=Statut.choices,
        default=Statut.NON_PAYEE,
        db_index=True
    )
    
    type = models.CharField(
        max_length=20,
        choices=TypeFacture.choices,
        default=TypeFacture.SCOLARITE,
        db_index=True
    )
    
    description = models.TextField(
        max_length=500,
        blank=True,
        help_text="Détails de la facture"
    )
    
    # Relations
    eleve = models.ForeignKey(
        'administrative.Eleve',
        on_delete=models.PROTECT,
        related_name='factures',
        null=True,
        blank=True,
        verbose_name="Élève lié"
    )
    
    enseignant = models.ForeignKey(
        'staff.Enseignant',
        on_delete=models.PROTECT,
        related_name='factures',
        null=True,
        blank=True,
        verbose_name="Enseignant lié"
    )
    
    created_by = models.ForeignKey(
        'users.Utilisateur',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Créée par"
    )

    # Métadonnées
    class Meta:
        ordering = ['-date_emission']
        verbose_name = "Facture"
        verbose_name_plural = "Factures"
        indexes = [
            models.Index(fields=['reference']),
            models.Index(fields=['statut', 'type']),
            models.Index(fields=['date_emission', 'date_echeance']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(montant__gt=0),
                name="montant_positif"
            ),
            models.UniqueConstraint(
                fields=['reference'],
                name='reference_unique'
            )
        ]

    def __str__(self):
        prefix = f"{self.reference} - {self.get_type_display()}"
        if self.eleve:
            return f"{prefix} - {self.eleve.nom_complet}"
        if self.enseignant:
            return f"{prefix} - {self.enseignant.get_full_name()}"
        return prefix

    def montant_with_devise(self):
        if self.devise == 'CDF':
            return f"{self.montant} Fc"
        elif self.devise == 'USD':
            return f"${self.montant}"
        elif self.devise == 'UGX':
            return f"{self.montant} Shs"
        return f"{self.montant} {self.devise}"

    def clean(self):
        """Validation complète de la facture"""
        super().clean()
        
        # Vérifier qu'une facture est liée soit à un élève, soit à un enseignant
        if not self.eleve and not self.enseignant:
            raise ValidationError("La facture doit être liée à un élève ou un enseignant")
        
        if self.eleve and self.enseignant:
            raise ValidationError("Une facture ne peut être liée à la fois à un élève et un enseignant")
        
        # Validation des dates
        if self.date_echeance is not None and self.date_emission is not None:
            if self.date_echeance < self.date_emission:
                    raise ValidationError("La date d'échéance doit être postérieure à la date d'émission")

    def save(self, *args, **kwargs):
        """Surcharge de la sauvegarde avec gestion de référence"""
        if not self.reference:
            self.reference = self._generate_unique_reference()
        
        self.full_clean()  # Validation avant sauvegarde
        super().save(*args, **kwargs)

    @classmethod
    def _generate_unique_reference(cls):
        """Génère une référence unique avec vérification"""
        while True:
            ref = generate_facture_reference()
            if not cls.objects.filter(reference=ref).exists():
                return ref

    # Méthodes métier
    def solde_restant(self):
        """Calcule le montant restant à payer"""
        total_paiements = sum(p.montant for p in self.paiements.all())
        return max(self.montant - total_paiements, 0)

    def update_statut(self):
        """Met à jour automatiquement le statut selon les paiements"""
        solde = self.solde_restant()
        
        if solde <= 0:
            self.statut = self.Statut.PAYEE
        elif solde < self.montant:
            self.statut = self.Statut.PARTIELLE
        else:
            self.statut = self.Statut.NON_PAYEE
        
        self.save(update_fields=['statut'])

    @property
    def est_en_retard(self):
        """Vérifie si la facture est en retard de paiement"""
        if not self.date_echeance or self.statut == self.Statut.PAYEE:
            return False
        return datetime.now().date() > self.date_echeance

    def generer_pdf(self):
        """Génère le PDF de la facture (à implémenter)"""
        # Utiliser une lib comme ReportLab ou WeasyPrint
        pass

class Paiement(models.Model):
    MODE_PAIEMENT_CHOICES = [
        ('especes', 'Espèces'),
        ('cheque', 'Chèque'),
        ('virement', 'Virement bancaire'),
        ('mobile_money', 'Mobile Money'),
    ]
    
    date = models.DateField()
    montant = models.FloatField()
    devise = models.CharField(
        max_length=3,
        choices=DEVISE_CHOICES,
        default='FC',
        verbose_name="Devise"
    )
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT_CHOICES)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='paiements')
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name='paiements', null=True, blank=True)
    remarques = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Paiement: {self.montant} {self.devise} - {self.date}"

class Depense(models.Model):
    CATEGORIE_CHOICES = [
        ('salaires', 'Salaires'),
        ('maintenance', 'Maintenance'),
        ('achat_materiel', 'Achat de matériel'),
        ('services', 'Services'),
        ('autre', 'Autre'),
    ]
    
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
    ]
    
    MOYEN_PAIEMENT_CHOICES = [
        ('especes', 'Espèces'),
        ('cheque', 'Chèque'),
        ('virement', 'Virement bancaire'),
        ('mobile_money', 'Mobile Money'),
    ]
    
    intitule = models.CharField(max_length=100)
    description = models.TextField()
    montant = models.FloatField(validators=[MinValueValidator(0)])
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    date_depense = models.DateField()
    moyen_paiement = models.CharField(max_length=20, choices=MOYEN_PAIEMENT_CHOICES)
    personne_beneficiaire = models.CharField(max_length=100)
    justificatif = models.FileField(upload_to='justificatifs/depenses/', blank=True, null=True)
    service_concerne = models.CharField(max_length=50)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_validation = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.intitule} - {self.montant} - {self.date_depense}"

class Revenue(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
    ]
    
    MOYEN_PAIEMENT_CHOICES = [
        ('especes', 'Espèces'),
        ('cheque', 'Chèque'),
        ('virement', 'Virement bancaire'),
        ('mobile_money', 'Mobile Money'),
    ]
    
    intitule = models.CharField(max_length=100)
    description = models.TextField()
    montant = models.FloatField(validators=[MinValueValidator(0)])
    date_reception = models.DateField()
    moyen_paiement = models.CharField(max_length=20, choices=MOYEN_PAIEMENT_CHOICES)
    personne_payeur = models.CharField(max_length=100)
    justificatif = models.FileField(upload_to='justificatifs/revenus/', blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    date_validation = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.intitule} - {self.montant} - {self.date_reception}"

class Budget(models.Model):
    annee_scolaire = models.CharField(max_length=20)
    montant_prevu = models.FloatField()
    montant_realise = models.FloatField(default=0)
    remarques = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Budget {self.annee_scolaire}"

class Bourse(models.Model):
    TYPE_BENEFICIAIRE_CHOICES = [
        ('eleve', 'Élève'),
        ('enseignant', 'Enseignant'),
    ]
    
    SOURCE_CHOICES = [
        ('etat', 'État'),
        ('ong', 'ONG'),
        ('etablissement', 'Établissement'),
        ('autre', 'Autre'),
    ]
    
    beneficiaire = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, related_name='bourses')
    type_beneficiaire = models.CharField(max_length=20, choices=TYPE_BENEFICIAIRE_CHOICES)
    montant = models.FloatField()
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    criteres = models.TextField()
    motif = models.TextField()
    date_attribution = models.DateField()
    justificatifs = models.FileField(upload_to='justificatifs/bourses/', blank=True, null=True)
    condition = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    
    def __str__(self):
        return f"Bourse: {self.beneficiaire} - {self.montant}"

class Retenue(models.Model):
    heure_non_prestee = models.IntegerField(default=0)
    impots = models.FloatField(default=0)
    cotisations_sociales = models.FloatField(default=0)
    pret_recu = models.FloatField(default=0)
    total_retenue = models.FloatField()
    
    def __str__(self):
        return f"Retenue: {self.total_retenue}"

class FichePaiementPersonnel(models.Model):
    class Statut(models.TextChoices):
        PAYEE = 'payee', 'Payée'
        NON_PAYEE = 'non_payee', 'Non payée'
        PARTIELLEMENT_PAYEE = 'partiellement_payee', 'Partiellement payée'
        ANNULEE = 'annulee', 'Annulée'

    enseignant = models.ForeignKey('staff.Enseignant', on_delete=models.CASCADE, related_name='fiches_paiement', null=True, blank=True)
    date_emission = models.DateField(default=timezone.now)
    date_echeance = models.DateField(null=True, blank=True)
    montant_base = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    devise = models.CharField(max_length=3, choices=Enseignant.DEVISE_CHOICES, default='FC')
    
    # Primes
    prime_anciennete = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prime_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prime_risque = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prime_transport = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prime_logement = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prime_autre = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Déductions
    deduction_cnss = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deduction_impot = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deduction_autre = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    statut = models.CharField(max_length=20, choices=Statut.choices, default=Statut.NON_PAYEE)
    created_by = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_emission']
        verbose_name = 'Fiche de paiement'
        verbose_name_plural = 'Fiches de paiement'
        indexes = [
            models.Index(fields=['statut']),
            models.Index(fields=['date_emission']),
            models.Index(fields=['date_echeance']),
        ]
    
    def __str__(self):
        return f"Fiche de paiement - {self.enseignant.get_full_name() if self.enseignant else 'Sans enseignant'} - {self.date_emission}"

    def calculer_total_primes(self):
        return sum([
            self.prime_anciennete,
            self.prime_charge,
            self.prime_risque,
            self.prime_transport,
            self.prime_logement,
            self.prime_autre
        ])

    def calculer_total_deductions(self):
        return sum([
            self.deduction_cnss,
            self.deduction_impot,
            self.deduction_autre
        ])

    def calculer_salaire_net(self):
        return self.montant_base + self.calculer_total_primes() - self.calculer_total_deductions()

    def update_statut(self):
        facture = self.facture
        if not facture:
            self.statut = self.Statut.NON_PAYEE
        else:
            montant_paye = facture.montant_paye
            montant_total = self.calculer_salaire_net()
            
            if montant_paye >= montant_total:
                self.statut = self.Statut.PAYEE
            elif montant_paye > 0:
                self.statut = self.Statut.PARTIELLEMENT_PAYEE
            else:
                self.statut = self.Statut.NON_PAYEE
                
        self.save()

    @property
    def facture(self):
        try:
            return self.facture_set.first()
        except:
            return None

class FicheEmprunt(models.Model):
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('rembourse', 'Remboursé'),
        ('en_retard', 'En retard'),
    ]
    
    emprunteur = models.CharField(max_length=100)
    montant_emprunte = models.FloatField()
    taux_interet = models.FloatField()
    date_emprunt = models.DateField()
    date_echeance = models.DateField()
    montant_rembourse = models.FloatField(default=0)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours')
    description = models.TextField()
    
    def __str__(self):
        return f"Emprunt: {self.emprunteur} - {self.montant_emprunte}"

class RapportGeneralFinance(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
    ]
    
    annee_scolaire = models.CharField(max_length=20)
    total_revenus = models.FloatField()
    total_depenses = models.FloatField()
    total_bourses = models.FloatField()
    solde_final = models.FloatField()
    date_generation = models.DateField()
    responsable_validation = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    observation = models.TextField(blank=True, null=True)
    document_pdf = models.FileField(upload_to='rapports/finances/', blank=True, null=True)
    
    def __str__(self):
        return f"Rapport financier - {self.annee_scolaire}"

class FichierFacture(models.Model):
    fichier = models.FileField(
        upload_to='factures/',
        verbose_name="Fichier"
    )
    date_upload = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date d'upload"
    )
    uploaded_by = models.ForeignKey(
        'users.Utilisateur',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Uploadé par"
    )

    def __str__(self):
        return self.fichier.name

    class Meta:
        verbose_name = "Fichier de facture"
        verbose_name_plural = "Fichiers de facture"
        ordering = ['-date_upload']