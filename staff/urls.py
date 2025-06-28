from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    # URL d'accueil
    path('', views.DashboardView.as_view(), name='dashboard'),

    # URLs pour la gestion du personnel administratif
    path('personnel/', views.PersonnelListView.as_view(), name='personnel_list'),
    path('personnel/ajouter/', views.PersonnelCreateView.as_view(), name='personnel_create'),
    path('personnel/<int:pk>/modifier/', views.PersonnelUpdateView.as_view(), name='personnel_update'),
    path('personnel/<int:pk>/supprimer/', views.PersonnelDeleteView.as_view(), name='personnel_delete'),
    path('personnel/import/', views.import_personnel, name='import_personnel'),
    path('personnel/export/<str:format_type>/', views.export_personnel, name='export_personnel'),

    # URLs pour les enseignants
    path('enseignants/', views.EnseignantListView.as_view(), name='enseignant_list'),
    path('enseignants/ajouter/', views.EnseignantCreateView.as_view(), name='enseignant_create'),
    path('enseignants/<int:pk>/modifier/', views.EnseignantUpdateView.as_view(), name='enseignant_update'),
    path('enseignants/<int:pk>/supprimer/', views.EnseignantDeleteView.as_view(), name='enseignant_delete'),
    path('enseignants/export/<str:format>/', views.export_enseignant, name='export_enseignant'),

    # URLs pour les spécialités
    path('specialites/', views.SpecialiteEnseignantListView.as_view(), name='specialite_list'),
    path('specialites/ajouter/', views.SpecialiteEnseignantCreateView.as_view(), name='specialite_create'),
    path('specialites/<int:pk>/modifier/', views.SpecialiteEnseignantUpdateView.as_view(), name='specialite_update'),
    path('specialites/<int:pk>/supprimer/', views.SpecialiteEnseignantDeleteView.as_view(), name='specialite_delete'),

    # URLs pour les documents
    path('documents/', views.DocumentPersonnelListView.as_view(), name='document_list'),
    path('documents/ajouter/', views.DocumentPersonnelCreateView.as_view(), name='document_create'),
    path('documents/<int:pk>/modifier/', views.DocumentPersonnelUpdateView.as_view(), name='document_update'),
    path('documents/<int:pk>/supprimer/', views.DocumentPersonnelDeleteView.as_view(), name='document_delete'),

    # URLs pour les tuteurs
    path('tuteurs/', views.TuteurListView.as_view(), name='tuteur_list'),
    path('tuteurs/ajouter/', views.TuteurCreateView.as_view(), name='tuteur_create'),
    path('tuteurs/<int:pk>/modifier/', views.TuteurUpdateView.as_view(), name='tuteur_update'),
    path('tuteurs/<int:pk>/supprimer/', views.TuteurDeleteView.as_view(), name='tuteur_delete'),

    # URLs pour les sanctions
    path('sanctions/', views.SanctionListView.as_view(), name='sanction_list'),
    path('sanctions/ajouter/', views.SanctionCreateView.as_view(), name='sanction_create'),
    path('sanctions/<int:pk>/', views.SanctionDetailView.as_view(), name='sanction_detail'),
    path('sanctions/<int:pk>/modifier/', views.SanctionUpdateView.as_view(), name='sanction_update'),
    path('sanctions/<int:pk>/supprimer/', views.SanctionDeleteView.as_view(), name='sanction_delete'),
    path('sanctions/<int:pk>/valider/', views.valider_sanction, name='valider_sanction'),
    path('sanctions/<int:pk>/annuler/', views.annuler_sanction, name='annuler_sanction'),
]
