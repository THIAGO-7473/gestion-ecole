from django import forms
from .models import (
    Facture, Paiement, Depense, Revenue, Budget, Bourse,
    Retenue, FichePaiementPersonnel, FicheEmprunt, RapportGeneralFinance, FichierFacture
)
from django.utils import timezone
from users.models import Utilisateur
from administrative.models import Eleve  # Import ici pour éviter les problèmes de dépendance circulaire

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        default_attrs = {'multiple': 'multiple'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)

    def value_from_datadict(self, data, files, name):
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return files.get(name)

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields = ['type', 'montant', 'devise', 'date_echeance', 'statut', 'description', 'eleve', 'enseignant', 'created_by']
        widgets = {
            'date_echeance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'devise': forms.Select(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            'eleve': forms.Select(attrs={'class': 'form-control'}),
            'enseignant': forms.Select(attrs={'class': 'form-control'}),
            'created_by': forms.Select(attrs={'class': 'form-control'}),
        }

    fichiers = MultipleFileField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Si c'est une modification (instance existante)
        if self.instance.pk:
            # Gestion de la date d'échéance
            if self.instance.date_echeance:
                self.initial['date_echeance'] = self.instance.date_echeance.strftime('%Y-%m-%d')
        
        # Limiter les choix pour created_by aux utilisateurs avec les rôles appropriés
        self.fields['created_by'].queryset = Utilisateur.objects.filter(role__in=['admin', 'personnel'])
        if self.user:
            self.fields['created_by'].initial = self.user

    def clean(self):
        cleaned_data = super().clean()
        date_echeance = cleaned_data.get('date_echeance')
        
        # Ne valider la date d'échéance que pour les nouvelles factures
        if not self.instance.pk and date_echeance and date_echeance < timezone.now().date():
            raise forms.ValidationError("La date d'échéance ne peut pas être dans le passé")
            
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Sauvegarder d'abord l'instance pour avoir un ID
        if commit:
            instance.save()
            
            # Gestion des fichiers
            if 'fichiers' in self.cleaned_data:
                fichiers = self.cleaned_data['fichiers']
                if fichiers:
                    # Supprimer les anciens fichiers si c'est une modification
                    if instance.pk:
                        instance.fichiers.all().delete()
                    
                    # Créer les nouveaux fichiers et les associer à la facture
                    for fichier in fichiers:
                        fichier_facture = FichierFacture.objects.create(
                            fichier=fichier,
                            uploaded_by=self.user
                        )
                        instance.fichiers.add(fichier_facture)
        
        return instance

class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = [
            'date', 'montant', 'devise', 'mode_paiement', 'facture',
            'eleve', 'remarques'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'devise': forms.Select(attrs={'class': 'form-control'}),
            'mode_paiement': forms.Select(attrs={'class': 'form-control'}),
            'facture': forms.Select(attrs={'class': 'form-control'}),
            'eleve': forms.Select(attrs={'class': 'form-control'}),
            'remarques': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limiter les choix de facture aux factures non payées
        self.fields['facture'].queryset = Facture.objects.filter(statut__in=['non_payee', 'partielle'])
        # Récupérer tous les élèves
        self.fields['eleve'].queryset = Eleve.objects.all()
        
        # Si c'est une modification (instance existante)
        if self.instance.pk:
            # Conserver la date existante
            if self.instance.date:
                self.initial['date'] = self.instance.date.strftime('%Y-%m-%d')

class DepenseForm(forms.ModelForm):
    class Meta:
        model = Depense
        fields = [
            'intitule', 'description', 'montant', 'categorie',
            'date_depense', 'moyen_paiement', 'personne_beneficiaire',
            'justificatif', 'service_concerne', 'statut', 'date_validation'
        ]
        widgets = {
            'date_depense': forms.DateInput(attrs={'type': 'date'}),
            'date_validation': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class RevenueForm(forms.ModelForm):
    class Meta:
        model = Revenue
        fields = [
            'intitule', 'description', 'montant', 'date_reception',
            'moyen_paiement', 'personne_payeur', 'justificatif',
            'statut', 'date_validation'
        ]
        widgets = {
            'date_reception': forms.DateInput(attrs={'type': 'date'}),
            'date_validation': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = [
            'annee_scolaire', 'montant_prevu', 'montant_realise',
            'remarques'
        ]
        widgets = {
            'remarques': forms.Textarea(attrs={'rows': 3}),
        }

class BourseForm(forms.ModelForm):
    class Meta:
        model = Bourse
        fields = [
            'beneficiaire', 'type_beneficiaire', 'montant', 'source',
            'criteres', 'motif', 'date_attribution', 'justificatifs',
            'condition', 'date_debut', 'date_fin'
        ]
        widgets = {
            'date_attribution': forms.DateInput(attrs={'type': 'date'}),
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'criteres': forms.Textarea(attrs={'rows': 3}),
            'motif': forms.Textarea(attrs={'rows': 3}),
            'condition': forms.Textarea(attrs={'rows': 3}),
        }

class RetenueForm(forms.ModelForm):
    class Meta:
        model = Retenue
        fields = [
            'heure_non_prestee', 'impots', 'cotisations_sociales',
            'pret_recu', 'total_retenue'
        ]

class FichePaiementForm(forms.ModelForm):
    class Meta:
        model = FichePaiementPersonnel
        fields = [
            'enseignant', 'date_emission', 'date_echeance',
            'montant_base', 'devise', 'prime_anciennete',
            'prime_charge', 'prime_risque', 'prime_transport',
            'prime_logement', 'prime_autre', 'deduction_cnss',
            'deduction_impot', 'deduction_autre', 'statut',
            'created_by'
        ]
        widgets = {
            'date_emission': forms.DateInput(attrs={'type': 'date'}),
            'date_echeance': forms.DateInput(attrs={'type': 'date'}),
        }

class FicheEmpruntForm(forms.ModelForm):
    class Meta:
        model = FicheEmprunt
        fields = [
            'emprunteur', 'montant_emprunte', 'taux_interet',
            'date_emprunt', 'date_echeance', 'montant_rembourse',
            'statut', 'description'
        ]
        widgets = {
            'date_emprunt': forms.DateInput(attrs={'type': 'date'}),
            'date_echeance': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class RapportGeneralFinanceForm(forms.ModelForm):
    class Meta:
        model = RapportGeneralFinance
        fields = [
            'annee_scolaire', 'total_revenus', 'total_depenses',
            'total_bourses', 'solde_final', 'date_generation',
            'responsable_validation', 'statut', 'observation',
            'document_pdf'
        ]
        widgets = {
            'date_generation': forms.DateInput(attrs={'type': 'date'}),
            'observation': forms.Textarea(attrs={'rows': 3}),
        }
