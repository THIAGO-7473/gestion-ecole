from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.FinanceHomeView.as_view(), name='home'),
    # Factures
    path('factures/', views.FactureListView.as_view(), name='facture_list'),
    path('factures/creer/', views.FactureCreateView.as_view(), name='facture_create'),
    path('factures/<int:pk>/', views.FactureDetailView.as_view(), name='facture_detail'),
    path('factures/<int:pk>/modifier/', views.FactureUpdateView.as_view(), name='facture_update'),
    path('factures/<int:pk>/supprimer/', views.FactureDeleteView.as_view(), name='facture_delete'),

    # Paiements
    path('paiements/', views.PaiementListView.as_view(), name='paiement_list'),
    path('paiements/creer/', views.PaiementCreateView.as_view(), name='paiement_create'),
    path('paiements/<int:pk>/', views.PaiementDetailView.as_view(), name='paiement_detail'),
    path('paiements/<int:pk>/modifier/', views.PaiementUpdateView.as_view(), name='paiement_update'),
    path('paiements/<int:pk>/supprimer/', views.PaiementDeleteView.as_view(), name='paiement_delete'),

    # Dépenses
    path('depenses/', views.DepenseListView.as_view(), name='depense_list'),
    path('depenses/creer/', views.DepenseCreateView.as_view(), name='depense_create'),
    path('depenses/<int:pk>/', views.DepenseDetailView.as_view(), name='depense_detail'),
    path('depenses/<int:pk>/modifier/', views.DepenseUpdateView.as_view(), name='depense_update'),
    path('depenses/<int:pk>/supprimer/', views.DepenseDeleteView.as_view(), name='depense_delete'),

    # Revenus
    path('revenus/', views.RevenueListView.as_view(), name='revenue_list'),
    path('revenus/creer/', views.RevenueCreateView.as_view(), name='revenue_create'),
    path('revenus/<int:pk>/', views.RevenueDetailView.as_view(), name='revenue_detail'),
    path('revenus/<int:pk>/modifier/', views.RevenueUpdateView.as_view(), name='revenue_update'),
    path('revenus/<int:pk>/supprimer/', views.RevenueDeleteView.as_view(), name='revenue_delete'),

    # Budgets
    path('budgets/', views.BudgetListView.as_view(), name='budget_list'),
    path('budgets/creer/', views.BudgetCreateView.as_view(), name='budget_create'),
    path('budgets/<int:pk>/', views.BudgetDetailView.as_view(), name='budget_detail'),
    path('budgets/<int:pk>/modifier/', views.BudgetUpdateView.as_view(), name='budget_update'),
    path('budgets/<int:pk>/supprimer/', views.BudgetDeleteView.as_view(), name='budget_delete'),

    # Bourses
    path('bourses/', views.BourseListView.as_view(), name='bourse_list'),
    path('bourses/creer/', views.BourseCreateView.as_view(), name='bourse_create'),
    path('bourses/<int:pk>/', views.BourseDetailView.as_view(), name='bourse_detail'),
    path('bourses/<int:pk>/modifier/', views.BourseUpdateView.as_view(), name='bourse_update'),
    path('bourses/<int:pk>/supprimer/', views.BourseDeleteView.as_view(), name='bourse_delete'),

    # Retenues
    path('retenues/', views.RetenueListView.as_view(), name='retenue_list'),
    path('retenues/creer/', views.RetenueCreateView.as_view(), name='retenue_create'),
    path('retenues/<int:pk>/', views.RetenueDetailView.as_view(), name='retenue_detail'),
    path('retenues/<int:pk>/modifier/', views.RetenueUpdateView.as_view(), name='retenue_update'),
    path('retenues/<int:pk>/supprimer/', views.RetenueDeleteView.as_view(), name='retenue_delete'),

    # Fiches de paiement
    path('fiches-paiement/', views.FichePaiementListView.as_view(), name='fiche_paiement_list'),
    path('fiches-paiement/creer/', views.FichePaiementCreateView.as_view(), name='fiche_paiement_create'),
    path('fiches-paiement/<int:pk>/', views.FichePaiementDetailView.as_view(), name='fiche_paiement_detail'),
    path('fiches-paiement/<int:pk>/modifier/', views.FichePaiementUpdateView.as_view(), name='fiche_paiement_update'),
    path('fiches-paiement/<int:pk>/supprimer/', views.FichePaiementDeleteView.as_view(), name='fiche_paiement_delete'),

    # Emprunts
    path('emprunts/', views.FicheEmpruntListView.as_view(), name='emprunt_list'),
    path('emprunts/creer/', views.FicheEmpruntCreateView.as_view(), name='emprunt_create'),
    path('emprunts/<int:pk>/', views.FicheEmpruntDetailView.as_view(), name='emprunt_detail'),
    path('emprunts/<int:pk>/modifier/', views.FicheEmpruntUpdateView.as_view(), name='emprunt_update'),
    path('emprunts/<int:pk>/supprimer/', views.FicheEmpruntDeleteView.as_view(), name='emprunt_delete'),

    # Rapports financiers
    path('rapports/', views.RapportGeneralFinanceListView.as_view(), name='rapport_list'),
    path('rapports/creer/', views.RapportGeneralFinanceCreateView.as_view(), name='rapport_create'),
    path('rapports/<int:pk>/', views.RapportGeneralFinanceDetailView.as_view(), name='rapport_detail'),
    path('rapports/<int:pk>/modifier/', views.RapportGeneralFinanceUpdateView.as_view(), name='rapport_update'),
    path('rapports/<int:pk>/supprimer/', views.RapportGeneralFinanceDeleteView.as_view(), name='rapport_delete'),
]
