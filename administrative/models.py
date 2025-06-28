# administrative/models.py
from django.core.exceptions import ValidationError
from django.db import models
from staff.models import Enseignant, PersonnelAdministratif
from users.models import Utilisateur


class Etablissement(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    logo = models.ImageField(upload_to='etablissement/logos/', null=True, blank=True)

    def __str__(self):
        return self.nom

class CalendrierScolaire(models.Model):
    annee_scolaire = models.CharField(max_length=20)  # ex: "2024-2025"
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        return self.annee_scolaire

class JourFerie(models.Model):
    calendrier = models.ForeignKey(CalendrierScolaire, on_delete=models.CASCADE, related_name='jours_feries')
    date = models.DateField()
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.date} - {self.description}"

class Evenement(models.Model):
    TYPE_CHOICES = [
        ('culturel', 'Culturel'),
        ('sportif', 'Sportif'),
        ('academique', 'Académique'),
        ('autre', 'Autre'),
    ]

    nom = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    lieu = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    organisateur = models.CharField(max_length=100)
    calendrier = models.ForeignKey(CalendrierScolaire, on_delete=models.CASCADE, related_name='evenements', null=True, blank=True)

    def __str__(self):
        return self.nom

class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    niveau = models.CharField(max_length=50)

    def __str__(self):
        return self.nom

class Salle(models.Model):
    nom = models.CharField(max_length=50)
    capacite = models.IntegerField()
    equipements = models.TextField()  # Stocké en format JSON ou séparé par des virgules

    def __str__(self):
        return self.nom

class Classe(models.Model):
    NIVEAU_CHOICES = [
        ('primaire', 'Primaire'),
        ('secondaire', 'Secondaire'),
    ]

    nom = models.CharField(max_length=50)  # ex: "CM1", "Terminale S"
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOICES)
    filiere = models.CharField(max_length=50, blank=True, null=True)
    effectif = models.IntegerField(default=0)
    enseignant_principal = models.ForeignKey('staff.Enseignant', on_delete=models.SET_NULL, null=True, related_name='classes_dirigees')

    def __str__(self):
        return self.nom

class EmploiDuTemps(models.Model):
    JOUR_CHOICES = [
        ('lundi', 'Lundi'),
        ('mardi', 'Mardi'),
        ('mercredi', 'Mercredi'),
        ('jeudi', 'Jeudi'),
        ('vendredi', 'Vendredi'),
        ('samedi', 'Samedi'),
    ]

    jour = models.CharField(max_length=10, choices=JOUR_CHOICES)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    def __str__(self):
        return f"{self.jour} {self.heure_debut}-{self.heure_fin}"

class Eleve(models.Model):
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    nom = models.CharField(max_length=100)
    postnom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    date_naissance = models.DateField()
    adresse = models.CharField(max_length=255)
    contact_eleve = models.CharField(max_length=20, blank=True, null=True)
    tuteur = models.ForeignKey('staff.Tuteur', on_delete=models.CASCADE, related_name='eleves')
    contact_tuteur = models.CharField(max_length=20)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='eleves')
    ecole_provenance = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.nom} {self.postnom} {self.prenom}"

class Cours(models.Model):
    nom = models.CharField(max_length=100)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    coefficient = models.IntegerField()
    enseignant = models.ForeignKey('staff.Enseignant', on_delete=models.CASCADE, related_name='cours')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='cours')
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    emploi_du_temps = models.ForeignKey(EmploiDuTemps, on_delete=models.CASCADE, related_name='cours')
    description = models.TextField()

    def __str__(self):
        return f"{self.nom} - {self.classe}"

class HoraireCours(models.Model):
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE, related_name='horaires')
    emploi_du_temps = models.ForeignKey(EmploiDuTemps, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cours.nom} - {self.emploi_du_temps.jour} {self.emploi_du_temps.heure_debut}-{self.emploi_du_temps.heure_fin}"

    class Meta:
        unique_together = ('cours', 'emploi_du_temps')
        verbose_name = "Horaire de cours"
        verbose_name_plural = "Horaires des cours"

class Absence(models.Model):
    date = models.DateField()
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name='absences', null=True, blank=True)
    enseignant = models.ForeignKey('staff.Enseignant', on_delete=models.CASCADE, related_name='absences', null=True, blank=True)
    motif = models.CharField(max_length=255)
    justification = models.TextField(blank=True, null=True)
    observation = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.eleve:
            return f"Absence élève: {self.eleve} - {self.date}"
        else:
            return f"Absence enseignant: {self.enseignant} - {self.date}"

class Inscription(models.Model):
    STATUT_CHOICES = [
        ('enregistre', 'Enregistré'),
        ('en_attente', 'En attente'),
        ('desinscrit', 'Désinscrit'),
    ]

    date_inscription = models.DateField()
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name='inscriptions')
    classe_anterieure = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True, blank=True, related_name='inscriptions_sortantes')
    classe_montante = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='inscriptions_entrantes')
    pourcentage = models.IntegerField(blank=True, null=True)
    dossier = models.TextField()  # JSON ou champs séparés pour les documents
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')

    def __str__(self):
        return f"Inscription: {self.eleve} - {self.date_inscription}"

class Examen(models.Model):
    SEMESTRE_CHOICES = [
        ('premier', 'Premier Semestre'),
        ('second', 'Second Semestre'),
        ('troisieme', 'Troisième Semestre'),
        ('quatrieme', 'Quatrième Semestre'),
    ]

    PERIODE_CHOICES = [
        ('premier', 'Premier Période'),
        ('second', 'Seconde Période'),
        ('troisieme', 'Troisième Période'),
        ('quatrieme', 'Quatrième Période'),
    ]

    nom = models.CharField(max_length=100)
    date = models.DateField()
    semestre = models.CharField(max_length=20, choices=SEMESTRE_CHOICES)
    periode = models.CharField(max_length=20, choices=PERIODE_CHOICES, default='premier')
    coefficient = models.FloatField()
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} - {self.cours} - {self.date}"

class Note(models.Model):
    TYPE_EVALUATION_CHOICES = [
        ('examen', 'Examen'),
        ('devoir', 'Devoir'),
        ('controle', 'Contrôle'),
    ]

    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name='notes')
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    type_evaluation = models.CharField(max_length=20, choices=TYPE_EVALUATION_CHOICES)
    note_obtenue = models.FloatField()
    maximum = models.FloatField(default=20.0)
    date_evaluation = models.DateField()

    def __str__(self):
        return f"{self.eleve} - {self.cours} - {self.note_obtenue}/{self.maximum}"

    def clean(self):
        # Validation de la note
        if self.note_obtenue > self.maximum:
            raise ValidationError("La note obtenue ne peut pas être supérieure au maximum.")

class Bulletin(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE, related_name='bulletins')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, null=True, blank=True)
    annee_scolaire = models.CharField(max_length=20)
    periode = models.CharField(max_length=50)
    moyenne_generale = models.FloatField()
    appreciation_generale = models.TextField()
    decision = models.CharField(max_length=100)
    rang = models.IntegerField()
    date_edition = models.DateField()

    def __str__(self):
        return f"Bulletin de {self.eleve} - {self.periode} {self.annee_scolaire}"

class DocumentContrat(models.Model):
    contrat = models.ForeignKey('Contrat', on_delete=models.CASCADE, related_name='documents')
    fichier = models.FileField(upload_to='contrats/')
    nom = models.CharField(max_length=255)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

class Contrat(models.Model):
    TYPE_CONTRAT_CHOICES = [
        ('CDI', 'Contrat à Durée Indéterminée'),
        ('CDD', 'Contrat à Durée Déterminée'),
        ('CTT', 'Contrat de Travail Temporaire'),
        ('CIR', "Contrat d'Insertion et de Réinsertion"),
    ]

    STATUT_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('suspendu', 'Suspendu'),
        ('resilie', 'Résilié'),
    ]

    DEVISE_CHOICES = [
        ('$', 'Dollar Américain'),
        ('FC', 'Franc Congolais'),
        ('Shs', 'Shillings Ougandais'),
    ]

    personnel = models.ForeignKey(PersonnelAdministratif, on_delete=models.CASCADE, related_name='contrats_personnel', null=True, blank=True)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name='contrats_enseignant', null=True, blank=True)
    type_contrat = models.CharField(max_length=3, choices=TYPE_CONTRAT_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    reference = models.CharField(max_length=20, unique=True, editable=False)
    salaire_brut = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salaire Brut")
    devise = models.CharField(max_length=3, choices=DEVISE_CHOICES, default='$')
    fonction = models.CharField(max_length=100)
    heures_semaine = models.IntegerField()
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='actif')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_salaire_brut_formatted(self):
        return f"${self.salaire_brut:,.2f}"

    def save(self, *args, **kwargs):
        if not self.reference:
            # Générer la référence automatiquement
            prefix = 'CT'
            if self.personnel:
                type_personnel = 'P'
            else:
                type_personnel = 'E'
            date = self.date_debut.strftime('%y%m')
            last_contrat = Contrat.objects.filter(reference__startswith=f'{prefix}{type_personnel}{date}').order_by('-reference').first()
            if last_contrat:
                last_num = int(last_contrat.reference[-4:])
                new_num = last_num + 1
            else:
                new_num = 1
            self.reference = f'{prefix}{type_personnel}{date}{new_num:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference} - {self.get_type_contrat_display()} ({self.date_debut})"

class Conge(models.Model):
    TYPE_CHOICES = [
        ('annuel', 'Congé annuel'),
        ('maladie', 'Congé maladie'),
        ('maternite', 'Congé maternité'),
        ('paternite', 'Congé paternité'),
        ('exceptionnel', 'Congé exceptionnel'),
    ]

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('approuve', 'Approuvé'),
        ('rejete', 'Rejeté'),
        ('annule', 'Annulé'),
    ]

    personnel = models.ForeignKey(PersonnelAdministratif, on_delete=models.SET_NULL, blank=True, null=True)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.SET_NULL, blank=True, null=True)
    type_conge = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField()
    jours_ouvrables = models.IntegerField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    motif = models.TextField(blank=True, null=True)
    justificatif = models.FileField(upload_to='conges/justificatifs/', blank=True, null=True)
    approuve_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, blank=True, null=True)
    date_approbation = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if not (self.personnel or self.enseignant):
            raise ValidationError("Un congé doit être lié soit à un personnel, soit à un enseignant")
        if self.personnel and self.enseignant:
            raise ValidationError("Un congé ne peut être lié à la fois à un personnel et un enseignant")
        if self.date_debut > self.date_fin:
            raise ValidationError("La date de fin doit être postérieure à la date de début")

    def __str__(self):
        return f"Conge {self.get_type_conge_display()} - {self.date_debut} au {self.date_fin}"

class Formation(models.Model):
    TYPE_CHOICES = [
        ('pedagogique', 'Pédagogique'),
        ('technique', 'Technique'),
        ('administrative', 'Administrative'),
        ('autre', 'Autre'),
    ]

    STATUT_CHOICES = [
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('realise', 'Réalisé'),
        ('annule', 'Annulé'),
    ]

    DEVISE_CHOICES = [
        ('FC', 'Franc Congolais'),
        ('SHS', 'Shillings Ougandais'),
        ('EUR', 'Euro'),
        ('USD', 'Dollar Américain'),
    ]

    intitule = models.CharField(max_length=200)
    type_formation = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(null=True, blank=True)
    objectifs = models.TextField(null=True, blank=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    lieu = models.CharField(max_length=200)
    formateur = models.CharField(max_length=200, null=True, blank=True)
    organisateur = models.CharField(max_length=200, null=True, blank=True)
    cout = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    devise = models.CharField(max_length=3, choices=DEVISE_CHOICES, default='FC')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='planifie')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.intitule

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"

class ParticipationFormation(models.Model):
    STATUT_CHOICES = [
        ('inscrit', 'Inscrit'),
        ('present', 'Présent'),
        ('absent', 'Absent'),
        ('abandon', 'Abandon'),
    ]

    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, blank=True, null=True)
    personnel = models.ForeignKey(PersonnelAdministratif, on_delete=models.CASCADE, blank=True, null=True)
    statut_participation = models.CharField(max_length=20, choices=STATUT_CHOICES, default='inscrit')
    evaluation_formateur = models.TextField(blank=True, null=True)
    evaluation_formation = models.TextField(blank=True, null=True)
    attestation = models.FileField(upload_to='formations/attestations/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('formation', 'enseignant', 'personnel')

    def clean(self):
        from django.core.exceptions import ValidationError
        if not (self.enseignant or self.personnel):
            raise ValidationError("Une participation doit être liée soit à un enseignant, soit à un personnel")
        if self.enseignant and self.personnel:
            raise ValidationError("Une participation ne peut être liée à la fois à un enseignant et un personnel")

    def __str__(self):
        participant = self.enseignant if self.enseignant else self.personnel
        return f"{participant} - {self.formation}"

class AttestationParticipation(models.Model):
    participation = models.ForeignKey(ParticipationFormation, on_delete=models.CASCADE, related_name='attestations')
    fichier = models.FileField(upload_to='formations/attestations/')
    nom = models.CharField(max_length=255)
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.participation}"

class RapportAdministratif(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
    ]

    annee_scolaire = models.CharField(max_length=9)
    nombre_eleves_total = models.IntegerField()
    nombre_eleves_nouveaux = models.IntegerField()
    nombre_eleves_exclus = models.IntegerField()
    nombre_enseignants = models.IntegerField()
    nombre_personnel_administratif = models.IntegerField()
    evenements_importants = models.TextField()
    nombre_recompenses = models.IntegerField()
    date_generation = models.DateField()
    responsable_validation = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    observation = models.TextField(blank=True)
    document_pdf = models.FileField(upload_to='rapports_administratifs/', null=True, blank=True)

    def __str__(self):
        return f"Rapport {self.annee_scolaire}"

    class Meta:
        verbose_name = "Rapport Administratif"
        verbose_name_plural = "Rapports Administratifs"

class DocumentConge(models.Model):
    conge = models.ForeignKey(Conge, on_delete=models.CASCADE, related_name='documents')
    fichier = models.FileField(upload_to='conges/justificatifs/')
    nom = models.CharField(max_length=255)
    date_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} - {self.conge}"
