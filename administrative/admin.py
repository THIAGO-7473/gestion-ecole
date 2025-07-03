from django.contrib import admin
from .models import (
    Eleve, Classe, JourFerie, Matiere, Salle, EmploiDuTemps, Cours,
    Etablissement, CalendrierScolaire, Evenement, HoraireCours, Absence,
    Inscription, Examen, Note, Bulletin, Contrat, Conge, Formation,
    ParticipationFormation, RapportAdministratif, DocumentContrat,
    AttestationParticipation, DocumentConge, DocumentRapport
)

@admin.register(JourFerie)
class JourFerieAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'calendrier')
    list_filter = ('calendrier', 'date')
    search_fields = ('description',)
    date_hierarchy = 'date'

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'niveau', 'description')
    list_filter = ('niveau',)
    search_fields = ('nom', 'description')

@admin.register(Salle)
class SalleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'capacite', 'equipements')
    list_filter = ('capacite',)
    search_fields = ('nom', 'equipements')

@admin.register(EmploiDuTemps)
class EmploiDuTempsAdmin(admin.ModelAdmin):
    list_display = ('jour', 'heure_debut', 'heure_fin')
    list_filter = ('jour',)
    search_fields = ('jour',)

@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('nom', 'matiere', 'enseignant', 'classe', 'salle', 'emploi_du_temps')
    list_filter = ('matiere', 'enseignant', 'classe', 'salle')
    search_fields = ('nom', 'matiere__nom', 'enseignant__nom', 'classe__nom', 'salle__nom')
    raw_id_fields = ('matiere', 'enseignant', 'classe', 'salle', 'emploi_du_temps')

@admin.register(DocumentRapport)
class DocumentRapportAdmin(admin.ModelAdmin):
    list_display = ['nom', 'rapport', 'date_upload']
    list_filter = ['date_upload', 'rapport__annee_scolaire']
    search_fields = ['nom', 'rapport__annee_scolaire']
    date_hierarchy = 'date_upload'
