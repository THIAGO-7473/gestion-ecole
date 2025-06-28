from django import forms
from .models import (
    AttestationParticipation, DocumentConge, Eleve, Classe, JourFerie, Matiere, Salle, EmploiDuTemps, Cours,
    Etablissement, CalendrierScolaire, Evenement, HoraireCours, Absence,
    Inscription, Examen, Note, Bulletin, Contrat, Conge, Formation, ParticipationFormation, RapportAdministratif, DocumentContrat
)
from staff.models import Tuteur, Enseignant, PersonnelAdministratif
from django.utils.safestring import mark_safe

class EleveForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = [
            'nom', 'postnom', 'prenom', 'sexe', 'date_naissance',
            'adresse', 'contact_eleve', 'tuteur', 'contact_tuteur',
            'classe', 'ecole_provenance'
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'postnom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'sexe': forms.Select(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_eleve': forms.TextInput(attrs={'class': 'form-control'}),
            'tuteur': forms.Select(attrs={'class': 'form-control'}),
            'contact_tuteur': forms.TextInput(attrs={'class': 'form-control'}),
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'ecole_provenance': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tuteur'].queryset = Tuteur.objects.all()
        self.fields['classe'].queryset = Classe.objects.all()

        # Si c'est une modification (instance existante)
        if self.instance.pk:
            # Conserver la date de naissance existante
            if self.instance.date_naissance:
                self.initial['date_naissance'] = self.instance.date_naissance.strftime('%Y-%m-%d')

class JourFerieForm(forms.ModelForm):
    class Meta:
        model = JourFerie
        fields = ['calendrier', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'calendrier': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si c'est une modification (instance existante)
        if self.instance.pk:
            # Conserver la date existante
            if self.instance.date:
                self.initial['date'] = self.instance.date.strftime('%Y-%m-%d')

class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = ['nom', 'description', 'niveau']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'niveau': forms.TextInput(attrs={'class': 'form-control'})
        }

class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = ['nom', 'capacite', 'equipements']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'capacite': forms.NumberInput(attrs={'class': 'form-control'}),
            'equipements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = ['nom', 'niveau', 'filiere', 'effectif', 'enseignant_principal']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'niveau': forms.Select(attrs={'class': 'form-control'}),
            'filiere': forms.TextInput(attrs={'class': 'form-control'}),
            'effectif': forms.NumberInput(attrs={'class': 'form-control'}),
            'enseignant_principal': forms.Select(attrs={'class': 'form-control'})
        }

class EmploiDuTempsForm(forms.ModelForm):
    class Meta:
        model = EmploiDuTemps
        fields = ['jour', 'heure_debut', 'heure_fin']
        widgets = {
            'jour': forms.Select(attrs={'class': 'form-control'}),
            'heure_debut': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
        }

class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = ['nom', 'matiere', 'coefficient', 'enseignant', 'classe', 'salle', 'emploi_du_temps', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'matiere': forms.Select(attrs={'class': 'form-control'}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control'}),
            'enseignant': forms.Select(attrs={'class': 'form-control'}),
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'salle': forms.Select(attrs={'class': 'form-control'}),
            'emploi_du_temps': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

class EtablissementForm(forms.ModelForm):
    class Meta:
        model = Etablissement
        fields = ['nom', 'adresse', 'telephone', 'email', 'logo']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CalendrierScolaireForm(forms.ModelForm):
    class Meta:
        model = CalendrierScolaire
        fields = ['annee_scolaire', 'date_debut', 'date_fin']
        widgets = {
            'annee_scolaire': forms.TextInput(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si c'est une modification (instance existante)
        if self.instance.pk:
            # Conserver les dates existantes
            if self.instance.date_debut:
                self.initial['date_debut'] = self.instance.date_debut.strftime('%Y-%m-%d')
            if self.instance.date_fin:
                self.initial['date_fin'] = self.instance.date_fin.strftime('%Y-%m-%d')

class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = ['nom', 'description', 'date', 'lieu', 'type', 'organisateur', 'calendrier']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'lieu': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'organisateur': forms.TextInput(attrs={'class': 'form-control'}),
            'calendrier': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si c'est une modification (instance existante)
        if self.instance.pk:
            # Conserver la date existante
            if self.instance.date:
                self.initial['date'] = self.instance.date.strftime('%Y-%m-%d')

class HoraireCoursForm(forms.ModelForm):
    class Meta:
        model = HoraireCours
        fields = ['cours', 'emploi_du_temps']
        widgets = {
            'cours': forms.Select(attrs={'class': 'form-control'}),
            'emploi_du_temps': forms.Select(attrs={'class': 'form-control'}),
        }

class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = ['date', 'eleve', 'enseignant', 'motif', 'justification', 'observation']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'eleve': forms.Select(attrs={'class': 'form-control'}),
            'enseignant': forms.Select(attrs={'class': 'form-control'}),
            'motif': forms.TextInput(attrs={'class': 'form-control'}),
            'justification': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'observation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = ['date_inscription', 'eleve', 'classe_anterieure', 'classe_montante',
                 'pourcentage', 'dossier', 'statut']
        widgets = {
            'date_inscription': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'eleve': forms.Select(attrs={'class': 'form-control'}),
            'classe_anterieure': forms.Select(attrs={'class': 'form-control'}),
            'classe_montante': forms.Select(attrs={'class': 'form-control'}),
            'pourcentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'dossier': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }

class ExamenForm(forms.ModelForm):
    class Meta:
        model = Examen
        fields = ['nom', 'date', 'semestre', 'periode', 'coefficient', 'cours', 'classe']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'semestre': forms.Select(attrs={'class': 'form-control'}),
            'periode': forms.Select(attrs={'class': 'form-control'}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control'}),
            'cours': forms.Select(attrs={'class': 'form-control'}),
            'classe': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si c'est une modification (instance existante)
        if self.instance.pk:
            # Conserver la date existante
            if self.instance.date:
                self.initial['date'] = self.instance.date.strftime('%Y-%m-%d')

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['eleve', 'cours', 'type_evaluation', 'note_obtenue', 'maximum', 'date_evaluation']
        widgets = {
            'eleve': forms.Select(attrs={'class': 'form-control'}),
            'cours': forms.Select(attrs={'class': 'form-control'}),
            'type_evaluation': forms.Select(attrs={'class': 'form-control'}),
            'note_obtenue': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'maximum': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'date_evaluation': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si c'est une modification (instance existante)
        if self.instance.pk:
            # Conserver la date d'évaluation existante
            if self.instance.date_evaluation:
                self.initial['date_evaluation'] = self.instance.date_evaluation.strftime('%Y-%m-%d')

class BulletinForm(forms.ModelForm):
    PERIODE_CHOICES = [
        ('premier', 'Première Période'),
        ('second', 'Seconde Période'),
        ('troisieme', 'Troisième Période'),
        ('quatrieme', 'Quatrième Période'),
    ]

    periode = forms.ChoiceField(choices=PERIODE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Bulletin
        fields = ['eleve', 'classe', 'annee_scolaire', 'periode', 'moyenne_generale', 'appreciation_generale', 'decision', 'rang', 'date_edition']
        widgets = {
            'eleve': forms.Select(attrs={'class': 'form-control'}),
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'annee_scolaire': forms.TextInput(attrs={'class': 'form-control'}),
            'moyenne_generale': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'appreciation_generale': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'decision': forms.TextInput(attrs={'class': 'form-control'}),
            'rang': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_edition': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si c'est une modification (instance existante)
        if self.instance.pk:
            # Conserver la date d'édition existante
            if self.instance.date_edition:
                self.initial['date_edition'] = self.instance.date_edition.strftime('%Y-%m-%d')

class DocumentContratForm(forms.ModelForm):
    class Meta:
        model = DocumentContrat
        fields = ['fichier', 'nom']
        widgets = {
            'fichier': forms.FileInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        default_attrs = {'multiple': 'multiple'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def value_from_datadict(self, data, files, name):
        print(f"=== MultipleFileInput.value_from_datadict ===")  # Debug
        print(f"Name: {name}")  # Debug
        print(f"Files: {files}")  # Debug
        print(f"Files.getlist({name}): {files.getlist(name) if files else 'No files'}")  # Debug

        if hasattr(files, 'getlist'):
            result = files.getlist(name)
            print(f"Result: {result}")  # Debug
            return result
        return files.get(name)

class ContratForm(forms.ModelForm):
    documents = forms.FileField(
        widget=MultipleFileInput(attrs={'class': 'form-control'}),
        required=False,
        label="Documents du Contrat"
    )

    class Meta:
        model = Contrat
        fields = ['personnel', 'enseignant', 'type_contrat', 'date_debut', 'date_fin', 'salaire_brut', 'fonction', 'heures_semaine', 'statut']
        widgets = {
            'personnel': forms.Select(attrs={'class': 'form-control'}),
            'enseignant': forms.Select(attrs={'class': 'form-control'}),
            'type_contrat': forms.Select(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'salaire_brut': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '$'}),
            'fonction': forms.TextInput(attrs={'class': 'form-control'}),
            'heures_semaine': forms.NumberInput(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si c'est une modification (instance existante)
        if self.instance.pk:
            # Conserver les dates existantes
            if self.instance.date_debut:
                self.initial['date_debut'] = self.instance.date_debut.strftime('%Y-%m-%d')
            if self.instance.date_fin:
                self.initial['date_fin'] = self.instance.date_fin.strftime('%Y-%m-%d')
            # Formater le salaire brut avec le symbole $
            if self.instance.salaire_brut:
                self.initial['salaire_brut'] = self.instance.salaire_brut

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if commit:
            # Gérer les fichiers uploadés
            files = self.cleaned_data.get('documents')
            if files:
                if isinstance(files, list):
                    for file in files:
                        DocumentContrat.objects.create(
                            contrat=instance,
                            fichier=file,
                            nom=file.name
                        )
                else:
                    DocumentContrat.objects.create(
                        contrat=instance,
                        fichier=files,
                        nom=files.name
                    )
        return instance

class CongeForm(forms.ModelForm):
    class Meta:
        model = Conge
        fields = ['personnel', 'enseignant', 'type_conge', 'date_debut', 'date_fin', 'jours_ouvrables', 'statut', 'motif', 'approuve_par', 'date_approbation']
        widgets = {
            'personnel': forms.Select(attrs={'class': 'form-control', 'id': 'id_personnel'}),
            'enseignant': forms.Select(attrs={'class': 'form-control', 'id': 'id_enseignant'}),
            'type_conge': forms.Select(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'format': '%Y-%m-%d'}),
            'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'format': '%Y-%m-%d'}),
            'jours_ouvrables': forms.NumberInput(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'motif': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'approuve_par': forms.Select(attrs={'class': 'form-control'}),
            'date_approbation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'format': '%Y-%m-%d'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Si c'est une modification
            if self.instance.date_debut:
                self.initial['date_debut'] = self.instance.date_debut.strftime('%Y-%m-%d')
            if self.instance.date_fin:
                self.initial['date_fin'] = self.instance.date_fin.strftime('%Y-%m-%d')
            if self.instance.date_approbation:
                self.initial['date_approbation'] = self.instance.date_approbation.strftime('%Y-%m-%d')

    def clean(self):
        print("=== DÉBUT clean CongeForm ===")  # Debug
        cleaned_data = super().clean()
        print(f"Cleaned data: {cleaned_data}")  # Debug

        personnel = cleaned_data.get('personnel')
        enseignant = cleaned_data.get('enseignant')
        print(f"Personnel: {personnel}")  # Debug
        print(f"Enseignant: {enseignant}")  # Debug

        # Validation : un seul type de personnel doit être sélectionné
        if personnel and enseignant:
            print("ERREUR: Personnel et enseignant sélectionnés")  # Debug
            raise forms.ValidationError("Vous ne pouvez sélectionner qu'un seul type de personnel (soit un personnel administratif, soit un enseignant).")

        if not personnel and not enseignant:
            print("ERREUR: Aucun personnel sélectionné")  # Debug
            raise forms.ValidationError("Vous devez sélectionner soit un personnel administratif, soit un enseignant.")

        # Validation des dates
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')
        print(f"Date début: {date_debut}")  # Debug
        print(f"Date fin: {date_fin}")  # Debug

        if date_debut and date_fin and date_debut > date_fin:
            print("ERREUR: Date de fin antérieure à la date de début")  # Debug
            raise forms.ValidationError("La date de fin doit être postérieure à la date de début.")

        print("=== FIN clean CongeForm ===")  # Debug
        return cleaned_data

    def save(self, commit=True):
        print("=== DÉBUT save CongeForm ===")  # Debug
        print(f"Commit: {commit}")  # Debug
        print(f"Self.files: {hasattr(self, 'files')}")  # Debug
        if hasattr(self, 'files'):
            print(f"Self.files content: {self.files}")  # Debug

        instance = super().save(commit=commit)
        print(f"Instance créée: {instance}")  # Debug
        print(f"Instance ID: {instance.id if instance.id else 'Pas encore sauvegardé'}")  # Debug
        print("=== FIN save CongeForm ===")  # Debug
        return instance

class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = ['intitule', 'type_formation', 'description', 'objectifs', 'date_debut', 'date_fin', 'lieu', 'formateur', 'organisateur', 'cout', 'devise', 'statut']
        widgets = {
            'intitule': forms.TextInput(attrs={'class': 'form-control'}),
            'type_formation': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'objectifs': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'lieu': forms.TextInput(attrs={'class': 'form-control'}),
            'formateur': forms.TextInput(attrs={'class': 'form-control'}),
            'organisateur': forms.TextInput(attrs={'class': 'form-control'}),
            'cout': forms.NumberInput(attrs={'class': 'form-control'}),
            'devise': forms.Select(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si c'est une modification (instance existante)
        if self.instance.pk:
            # Conserver les dates existantes
            if self.instance.date_debut:
                self.initial['date_debut'] = self.instance.date_debut.strftime('%Y-%m-%d')
            if self.instance.date_fin:
                self.initial['date_fin'] = self.instance.date_fin.strftime('%Y-%m-%d')

    def clean(self):
        cleaned_data = super().clean()
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')

        if date_debut and date_fin and date_debut > date_fin:
            raise forms.ValidationError("La date de fin doit être postérieure à la date de début.")

        return cleaned_data

class ParticipationForm(forms.ModelForm):
    attestation_files = forms.FileField(
        widget=MultipleFileInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='Vous pouvez sélectionner plusieurs fichiers'
    )

    class Meta:
        model = ParticipationFormation
        fields = ['formation', 'enseignant', 'personnel', 'statut_participation',
                 'evaluation_formateur', 'evaluation_formation']
        widgets = {
            'formation': forms.Select(attrs={'class': 'form-select'}),
            'enseignant': forms.Select(attrs={'class': 'form-select', 'id': 'id_enseignant_participation'}),
            'personnel': forms.Select(attrs={'class': 'form-select', 'id': 'id_personnel_participation'}),
            'statut_participation': forms.Select(attrs={'class': 'form-select'}),
            'evaluation_formateur': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'evaluation_formation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enseignant'].queryset = Enseignant.objects.all()
        self.fields['personnel'].queryset = PersonnelAdministratif.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        enseignant = cleaned_data.get('enseignant')
        personnel = cleaned_data.get('personnel')

        # Validation : un seul type de personnel doit être sélectionné
        if enseignant and personnel:
            raise forms.ValidationError("Vous ne pouvez sélectionner qu'un seul type de personnel (soit un enseignant, soit un personnel administratif).")

        if not enseignant and not personnel:
            raise forms.ValidationError("Vous devez sélectionner soit un enseignant, soit un personnel administratif.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            # Gérer les fichiers uploadés seulement s'ils existent
            if hasattr(self, 'files') and self.files:
                fichiers = self.files.getlist('attestation_files')
                for fichier in fichiers:
                    AttestationParticipation.objects.create(
                        participation=instance,
                        fichier=fichier,
                        nom=fichier.name
                    )
        return instance

class RapportAdministratifForm(forms.ModelForm):
    class Meta:
        model = RapportAdministratif
        fields = [
            'annee_scolaire', 'nombre_eleves_total', 'nombre_eleves_nouveaux',
            'nombre_eleves_exclus', 'nombre_enseignants', 'nombre_personnel_administratif',
            'evenements_importants', 'nombre_recompenses', 'date_generation',
            'responsable_validation', 'statut', 'observation', 'document_pdf'
        ]
        widgets = {
            'annee_scolaire': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_eleves_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre_eleves_nouveaux': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre_eleves_exclus': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre_enseignants': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre_personnel_administratif': forms.NumberInput(attrs={'class': 'form-control'}),
            'evenements_importants': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nombre_recompenses': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_generation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'document_pdf': forms.FileInput(attrs={'class': 'form-control'}),
            'responsable_validation': forms.Select(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'observation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
