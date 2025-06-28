from django.urls import path
from . import views

app_name = 'administrative'

urlpatterns = [
    path('', views.index, name='index'),
    # URLs pour la gestion des élèves
    path('eleves/', views.eleve_list, name='eleve_list'),
    path('eleves/nouveau/', views.eleve_create, name='eleve_create'),
    path('eleves/<int:pk>/', views.eleve_detail, name='eleve_detail'),
    path('eleves/<int:pk>/modifier/', views.eleve_update, name='eleve_update'),
    path('eleves/<int:pk>/supprimer/', views.eleve_delete, name='eleve_delete'),

    # URLs pour la gestion des classes
    path('classes/', views.classe_list, name='classe_list'),
    path('classes/nouvelle/', views.classe_create, name='classe_create'),
    path('classes/<int:pk>/', views.classe_detail, name='classe_detail'),
    path('classes/<int:pk>/modifier/', views.classe_update, name='classe_update'),
    path('classes/<int:pk>/supprimer/', views.classe_delete, name='classe_delete'),

    # URLs pour la gestion des établissements
    path('etablissements/', views.etablissement_list, name='etablissement_list'),
    path('etablissements/nouveau/', views.etablissement_create, name='etablissement_create'),
    path('etablissements/<int:pk>/modifier/', views.etablissement_update, name='etablissement_update'),
    path('etablissements/<int:pk>/supprimer/', views.etablissement_delete, name='etablissement_delete'),

    # URLs pour la gestion des calendriers scolaires
    path('calendriers/', views.calendrier_list, name='calendrier_list'),
    path('calendriers/nouveau/', views.calendrier_create, name='calendrier_create'),
    path('calendriers/<int:pk>/modifier/', views.calendrier_update, name='calendrier_update'),
    path('calendriers/<int:pk>/supprimer/', views.calendrier_delete, name='calendrier_delete'),

    # URLs pour la gestion des événements
    path('evenements/', views.evenement_list, name='evenement_list'),
    path('evenements/nouveau/', views.evenement_create, name='evenement_create'),
    path('evenements/<int:pk>/modifier/', views.evenement_update, name='evenement_update'),
    path('evenements/<int:pk>/supprimer/', views.evenement_delete, name='evenement_delete'),

    # URLs pour la gestion des horaires de cours
    path('horaires/', views.horaire_list, name='horaire_list'),
    path('horaires/nouveau/', views.horaire_create, name='horaire_create'),
    path('horaires/<int:pk>/modifier/', views.horaire_update, name='horaire_update'),
    path('horaires/<int:pk>/supprimer/', views.horaire_delete, name='horaire_delete'),

    # URLs pour la gestion des absences
    path('absences/', views.absence_list, name='absence_list'),
    path('absences/nouvelle/', views.absence_create, name='absence_create'),
    path('absences/<int:pk>/modifier/', views.absence_update, name='absence_update'),
    path('absences/<int:pk>/supprimer/', views.absence_delete, name='absence_delete'),

    # URLs pour la gestion des inscriptions
    path('inscriptions/', views.inscription_list, name='inscription_list'),
    path('inscriptions/nouvelle/', views.inscription_create, name='inscription_create'),
    path('inscriptions/<int:pk>/modifier/', views.inscription_update, name='inscription_update'),
    path('inscriptions/<int:pk>/supprimer/', views.inscription_delete, name='inscription_delete'),

    # URLs pour la gestion des examens
    path('examens/', views.examen_list, name='examen_list'),
    path('examens/nouveau/', views.examen_create, name='examen_create'),
    path('examens/<int:pk>/modifier/', views.examen_update, name='examen_update'),
    path('examens/<int:pk>/supprimer/', views.examen_delete, name='examen_delete'),

    # URLs pour Note
    path('notes/', views.note_list, name='note_list'),
    path('notes/nouvelle/', views.note_create, name='note_create'),
    path('notes/<int:pk>/modifier/', views.note_update, name='note_update'),
    path('notes/<int:pk>/supprimer/', views.note_delete, name='note_delete'),

    # URLs pour Bulletin
    path('bulletins/', views.bulletin_list, name='bulletin_list'),
    path('bulletins/nouveau/', views.bulletin_create, name='bulletin_create'),
    path('bulletins/<int:pk>/modifier/', views.bulletin_update, name='bulletin_update'),
    path('bulletins/<int:pk>/supprimer/', views.bulletin_delete, name='bulletin_delete'),

    # URLs pour Contrat
    path('contrats/', views.contrat_list, name='contrat_list'),
    path('contrats/nouveau/', views.contrat_create, name='contrat_create'),
    path('contrats/<int:pk>/', views.contrat_detail, name='contrat_detail'),
    path('contrats/<int:pk>/modifier/', views.contrat_update, name='contrat_update'),
    path('contrats/<int:pk>/supprimer/', views.contrat_delete, name='contrat_delete'),
    path('contrats/document/<int:pk>/supprimer/', views.document_contrat_delete, name='document_contrat_delete'),

    # URLs pour Conge
    path('conges/', views.conge_list, name='conge_list'),
    path('conges/nouveau/', views.conge_create, name='conge_create'),
    path('conges/<int:pk>/modifier/', views.conge_update, name='conge_update'),
    path('conges/<int:pk>/supprimer/', views.conge_delete, name='conge_delete'),
    path('conges/<int:pk>/', views.CongeDetailView.as_view(), name='conge_detail'),

    # URLs pour Formation
    path('formations/', views.formation_list, name='formation_list'),
    path('formations/nouvelle/', views.formation_create, name='formation_create'),
    path('formations/<int:pk>/modifier/', views.formation_update, name='formation_update'),
    path('formations/<int:pk>/supprimer/', views.formation_delete, name='formation_delete'),
    path('formations/<int:pk>/', views.formation_detail, name='formation_detail'),

    # URLs pour Participation
    path('participations/', views.participation_list, name='participation_list'),
    path('participations/nouvelle/', views.participation_create, name='participation_create'),
    path('participations/<int:pk>/', views.ParticipationDetailView.as_view(), name='participation_detail'),
    path('participations/<int:pk>/modifier/', views.participation_update, name='participation_update'),
    path('participations/<int:pk>/supprimer/', views.participation_delete, name='participation_delete'),

       # URLs pour RapportAdministratif
    path('rapports/', views.rapport_list, name='rapport_list'),
    path('rapports/nouveau/', views.rapport_create, name='rapport_create'),
    path('rapports/<int:pk>/', views.RapportAdministratifDetailView.as_view(), name='rapport_detail'),
    path('rapports/<int:pk>/modifier/', views.rapport_update, name='rapport_update'),
    path('rapports/<int:pk>/supprimer/', views.rapport_delete, name='rapport_delete'),

    # JourFerie URLs
    path('jours-feries/', views.jour_ferie_list, name='jour_ferie_list'),
    path('jours-feries/nouveau/', views.jour_ferie_create, name='jour_ferie_create'),
    path('jours-feries/<int:pk>/modifier/', views.jour_ferie_update, name='jour_ferie_update'),
    path('jours-feries/<int:pk>/supprimer/', views.jour_ferie_delete, name='jour_ferie_delete'),

    # Matiere URLs
    path('matieres/', views.matiere_list, name='matiere_list'),
    path('matieres/nouvelle/', views.matiere_create, name='matiere_create'),
    path('matieres/<int:pk>/modifier/', views.matiere_update, name='matiere_update'),
    path('matieres/<int:pk>/supprimer/', views.matiere_delete, name='matiere_delete'),

    # Salle URLs
    path('salles/', views.salle_list, name='salle_list'),
    path('salles/nouvelle/', views.salle_create, name='salle_create'),
    path('salles/<int:pk>/modifier/', views.salle_update, name='salle_update'),
    path('salles/<int:pk>/supprimer/', views.salle_delete, name='salle_delete'),

    # EmploiDuTemps URLs
    path('emplois-du-temps/', views.emploi_du_temps_list, name='emploi_du_temps_list'),
    path('emplois-du-temps/nouveau/', views.emploi_du_temps_create, name='emploi_du_temps_create'),
    path('emplois-du-temps/<int:pk>/modifier/', views.emploi_du_temps_update, name='emploi_du_temps_update'),
    path('emplois-du-temps/<int:pk>/supprimer/', views.emploi_du_temps_delete, name='emploi_du_temps_delete'),

    # Cours URLs
    path('cours/', views.cours_list, name='cours_list'),
    path('cours/nouveau/', views.cours_create, name='cours_create'),
    path('cours/<int:pk>/modifier/', views.cours_update, name='cours_update'),
    path('cours/<int:pk>/supprimer/', views.cours_delete, name='cours_delete'),
]
