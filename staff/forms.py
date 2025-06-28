from django import forms
from .models import (
    FichierDocument, PersonnelAdministratif, Enseignant, SpecialiteEnseignant,
    DocumentPersonnel, Tuteur, Sanction, FichierPreuve
)
from django.core.validators import MinValueValidator
from django.utils import timezone

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return files.get(name)

    def value_omitted_from_data(self, data, files, name):
        if name not in files:
            return True
        return False

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if data is None:
            return None
        if isinstance(data, (list, tuple)):
            return [super().clean(d, initial) for d in data]
        return super().clean(data, initial)

class PersonnelForm(forms.ModelForm):
    class Meta:
        model = PersonnelAdministratif
        fields = ['photo', 'nom', 'postnom', 'prenom', 'sexe', 'date_naissance', 
                 'lieu_naissance', 'adresse', 'telephone', 'email', 'role', 
                 'specialite', 'date_embauche', 'salaire_base', 'devise', 
                 'numero_secu', 'statut']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'date_embauche': forms.DateInput(attrs={'type': 'date'}),
            'sexe': forms.Select(choices=PersonnelAdministratif.SEXE_CHOICES),
            'role': forms.Select(choices=PersonnelAdministratif.ROLE_CHOICES),
            'statut': forms.Select(choices=PersonnelAdministratif.STATUT_CHOICES),
            'devise': forms.Select(choices=PersonnelAdministratif.DEVISE_CHOICES),
        }

class EnseignantForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = ['photo', 'nom', 'postnom', 'prenom', 'matricule', 'sexe', 'date_naissance',
                 'nationalite', 'adresse', 'telephone', 'email', 'situation_familiale',
                 'date_engagement', 'anciennete', 'anciennete_unite', 'anciennete_grade',
                 'anciennete_grade_unite', 'grade_echeant', 'acte_nom', 'diplome',
                 'etat_civil', 'cote', 'lieu_affectation', 'statut', 'salaire_base',
                 'devise', 'charge_horaire']
        widgets = {
            'date_naissance': forms.DateInput(attrs={'type': 'date'}),
            'date_engagement': forms.DateInput(attrs={'type': 'date'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class SpecialiteEnseignantForm(forms.ModelForm):
    class Meta:
        model = SpecialiteEnseignant
        fields = ['enseignant', 'matiere', 'niveau_competence', 'annees_experience']
        widgets = {
            'niveau_competence': forms.Select(choices=SpecialiteEnseignant.NIVEAU_CHOICES),
        }

class DocumentPersonnelForm(forms.ModelForm):
    fichiers = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = DocumentPersonnel
        fields = ['type_document', 'titre', 'description', 'date_depot', 'enseignant', 'personnel', 'statut']
        widgets = {
            'date_depot': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'type_document': forms.Select(choices=DocumentPersonnel.TYPE_CHOICES, attrs={'class': 'form-select'}),
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'enseignant': forms.Select(attrs={'class': 'form-select'}),
            'personnel': forms.Select(attrs={'class': 'form-select'}),
            'statut': forms.Select(choices=DocumentPersonnel.STATUT_CHOICES, attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enseignant'].required = False
        self.fields['personnel'].required = False
        self.fields['enseignant'].empty_label = "Sélectionner un enseignant"
        self.fields['personnel'].empty_label = "Sélectionner un personnel"
        self.fields['statut'].initial = 'en_attente'
        self.fields['type_document'].choices = DocumentPersonnel.TYPE_CHOICES
        self.fields['statut'].choices = DocumentPersonnel.STATUT_CHOICES

        if self.instance and self.instance.pk:
            self.fields['fichiers'].required = False
            if self.instance.date_depot:
                self.fields['date_depot'].initial = self.instance.date_depot
                self.initial['date_depot'] = self.instance.date_depot

    def clean(self):
        cleaned_data = super().clean()
        enseignant = cleaned_data.get('enseignant')
        personnel = cleaned_data.get('personnel')
        date_depot = cleaned_data.get('date_depot')
        
        if not enseignant and not personnel:
            raise forms.ValidationError("Un document doit être lié à un enseignant ou à un personnel administratif.")

        if not date_depot and self.instance and self.instance.pk:
            cleaned_data['date_depot'] = self.instance.date_depot
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.instance and self.instance.pk and not instance.date_depot:
            instance.date_depot = self.instance.date_depot
            
        if commit:
            instance.save()
            if self.files.getlist('fichiers'):
                for f in self.files.getlist('fichiers'):
                    FichierDocument.objects.create(
                        document=instance,
                        fichier=f,
                        nom_fichier=f.name
                    )
        return instance

class TuteurForm(forms.ModelForm):
    class Meta:
        model = Tuteur
        fields = ['nom', 'postnom', 'prenom', 'contact_tuteur', 'email', 'profession']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'postnom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_tuteur': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'profession': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nom': 'Nom',
            'postnom': 'Postnom',
            'prenom': 'Prénom',
            'contact_tuteur': 'Contact',
            'email': 'Email',
            'profession': 'Profession',
        }

class SanctionForm(forms.ModelForm):
    fichiers_preuves = MultipleFileField(
        required=False,
        label="Fichiers de preuves"
    )
    descriptions_preuves = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        required=False,
        label="Descriptions des preuves (une par ligne)"
    )

    class Meta:
        model = Sanction
        fields = [
            'enseignant', 'personnel', 'type_sanction',
            'date_sanction', 'date_effet', 'duree', 'duree_unite',
            'montant_retenue', 'devise', 'motif', 'observations',
            'donneur_sanction', 'statut', 'date_validation',
            'fichiers_preuves', 'descriptions_preuves'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['enseignant'].required = False
        self.fields['personnel'].required = False
        self.fields['enseignant'].empty_label = "Sélectionner un enseignant"
        self.fields['personnel'].empty_label = "Sélectionner un personnel"
        self.fields['statut'].initial = 'en_attente'
        self.fields['type_sanction'].choices = Sanction.TYPE_CHOICES
        self.fields['statut'].choices = Sanction.STATUT_CHOICES
        self.fields['duree_unite'].choices = Sanction.DUREE_UNITE_CHOICES
        self.fields['devise'].choices = Sanction.DEVISE_CHOICES
        self.fields['donneur_sanction'].choices = Sanction.DONNEUR_SANCTION_CHOICES
        self.fields['donneur_sanction'].required = True
        self.fields['donneur_sanction'].empty_label = None

    def clean(self):
        cleaned_data = super().clean()
        enseignant = cleaned_data.get('enseignant')
        personnel = cleaned_data.get('personnel')
        donneur_sanction = cleaned_data.get('donneur_sanction')
        
        if not enseignant and not personnel:
            raise forms.ValidationError("Une sanction doit être liée soit à un enseignant, soit à un personnel administratif.")
        
        if enseignant and personnel:
            raise forms.ValidationError("Une sanction ne peut être liée à la fois à un enseignant et un personnel")

        if not donneur_sanction:
            raise forms.ValidationError("Le donneur de sanction est obligatoire")
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            
            # Gérer les fichiers de preuves
            fichiers = self.cleaned_data.get('fichiers_preuves')
            descriptions = self.cleaned_data.get('descriptions_preuves', '').split('\n')
            
            if fichiers:
                for i, fichier in enumerate(fichiers):
                    description = descriptions[i].strip() if i < len(descriptions) else ''
                    FichierPreuve.objects.create(
                        sanction=instance,
                        fichier=fichier,
                        description=description
                    )
            
        return instance
