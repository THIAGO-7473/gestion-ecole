from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserDashboardView.as_view(), name='user_dashboard'),
    path('list/', views.UtilisateurListView.as_view(), name='utilisateur_list'),
    path('create/', views.UtilisateurCreateView.as_view(), name='utilisateur_create'),
    path('<int:pk>/update/', views.UtilisateurUpdateView.as_view(), name='utilisateur_update'),
    path('<int:pk>/delete/', views.UtilisateurDeleteView.as_view(), name='utilisateur_delete'),
    path('import/', views.ImportUsersView.as_view(), name='import_users'),
    path('export/csv/', views.export_users_csv, name='export_users_csv'),
    path('export/excel/', views.export_users_excel, name='export_users_excel'),
    path('export/pdf/', views.export_users_pdf, name='export_users_pdf'),
    path('export/word/', views.export_users_word, name='export_users_word'),
    path('login/', views.LoginView.as_view(template_name='users/login.html'), name='login'),
]
