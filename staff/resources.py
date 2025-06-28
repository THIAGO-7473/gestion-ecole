from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import PersonnelAdministratif, Enseignant

class PersonnelAdministratifResource(resources.ModelResource):
    class Meta:
        model = PersonnelAdministratif
        fields = ('id', 'nom', 'postnom', 'prenom', 'sexe', 'date_naissance', 'adresse', 'telephone', 'email', 'role', 'specialite', 'date_embauche', 'salaire_base', 'devise', 'numero_secu', 'statut')
        export_order = fields

    def get_export_headers(self, *args, **kwargs):
        return {
            'id': 'ID',
            'nom': 'Nom',
            'postnom': 'Postnom',
            'prenom': 'Prénom',
            'sexe': 'Sexe',
            'date_naissance': 'Date de naissance',
            'adresse': 'Adresse',
            'telephone': 'Téléphone',
            'email': 'Email',
            'role': 'Rôle',
            'specialite': 'Spécialité',
            'date_embauche': 'Date d\'embauche',
            'salaire_base': 'Salaire de base',
            'devise': 'Devise',
            'numero_secu': 'Numéro de sécurité sociale',
            'statut': 'Statut'
        }

class EnseignantResource(resources.ModelResource):
    class Meta:
        model = Enseignant
        fields = ('matricule', 'nom', 'postnom', 'prenom', 'sexe', 'date_naissance', 'adresse', 'telephone', 'email', 'diplome', 'date_engagement', 'lieu_affectation', 'statut', 'charge_horaire')
        export_order = fields

    def get_export_headers(self, *args, **kwargs):
        return {
            'matricule': 'Matricule',
            'nom': 'Nom',
            'postnom': 'Postnom',
            'prenom': 'Prénom',
            'sexe': 'Sexe',
            'date_naissance': 'Date de naissance',
            'adresse': 'Adresse',
            'telephone': 'Téléphone',
            'email': 'Email',
            'diplome': 'Diplôme',
            'date_engagement': 'Date d\'engagement',
            'lieu_affectation': 'Lieu d\'affectation',
            'statut': 'Statut',
            'charge_horaire': 'Charge horaire'
        } 