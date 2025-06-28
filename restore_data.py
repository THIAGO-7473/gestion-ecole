import json
from django.core.management.base import BaseCommand
from staff.models import Enseignant, PersonnelAdministratif
from finance.models import FichePaiementPersonnel

class Command(BaseCommand):
    help = 'Restore data from backup files'

    def handle(self, *args, **options):
        self.restore_enseignants()
        self.restore_personnel()

    def restore_enseignants(self):
        with open('enseignants_backup.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                fields = item['fields']
                enseignant = Enseignant(
                    nom=fields['nom'],
                    postnom=fields['postnom'],
                    prenom=fields['prenom'],
                    matricule=fields['matricule'],
                    sexe=fields['sexe'],
                    date_naissance=fields['date_naissance'],
                    nationalite=fields['nationalite'],
                    adresse=fields['adresse'],
                    telephone=fields['telephone'],
                    email=fields['email'],
                    situation_familiale=fields['situation_familiale'],
                    date_engagement=fields['date_engagement'],
                    anciennete=fields['anciennete'],
                    anciennete_unite=fields['anciennete_unite'],
                    anciennete_grade=fields['anciennete_grade'],
                    anciennete_grade_unite=fields['anciennete_grade_unite'],
                    grade_echeant=fields['grade_echeant'],
                    acte_nom=fields['acte_nom'],
                    diplome=fields['diplome'],
                    etat_civil=fields['etat_civil'],
                    cote=fields['cote'],
                    lieu_affectation=fields['lieu_affectation'],
                    statut=fields['statut'],
                    salaire_base=fields['salaire_base'],
                    devise=fields['devise'],
                    charge_horaire=fields['charge_horaire'],
                    photo=fields['photo']
                )
                enseignant.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully restored enseignant {enseignant.nom}'))

    def restore_personnel(self):
        with open('personnel_backup.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                fields = item['fields']
                personnel = PersonnelAdministratif(
                    nom=fields['nom'],
                    postnom=fields['postnom'],
                    prenom=fields['prenom'],
                    matricule=fields['matricule'],
                    sexe=fields['sexe'],
                    date_naissance=fields['date_naissance'],
                    nationalite=fields['nationalite'],
                    adresse=fields['adresse'],
                    telephone=fields['telephone'],
                    email=fields['email'],
                    situation_familiale=fields['situation_familiale'],
                    date_engagement=fields['date_engagement'],
                    anciennete=fields['anciennete'],
                    anciennete_unite=fields['anciennete_unite'],
                    anciennete_grade=fields['anciennete_grade'],
                    anciennete_grade_unite=fields['anciennete_grade_unite'],
                    grade_echeant=fields['grade_echeant'],
                    acte_nom=fields['acte_nom'],
                    diplome=fields['diplome'],
                    etat_civil=fields['etat_civil'],
                    cote=fields['cote'],
                    lieu_affectation=fields['lieu_affectation'],
                    statut=fields['statut'],
                    salaire_base=fields['salaire_base'],
                    devise=fields['devise'],
                    photo=fields['photo']
                )
                personnel.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully restored personnel {personnel.nom}')) 