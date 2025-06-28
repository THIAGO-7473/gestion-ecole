from django import forms
from .models import Utilisateur
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UtilisateurForm(UserCreationForm):
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text="Au moins 8 caractères, pas uniquement des chiffres.",
        required=False
    )
    password2 = forms.CharField(
        label="Confirmation",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Utilisateur
        fields = [
            'username', 'email', 'first_name', 'last_name', 'postnom',
            'telephone', 'adresse', 'date_naissance', 'role', 'statut',
            'photo_profil', 'password1', 'password2'
        ]
        widgets = {
            'date_naissance': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'format': '%Y-%m-%d'
            }),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'photo_profil': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Si c'est une modification d'utilisateur existant
        if self.instance.pk:
            # Si le username n'a pas changé, on le valide
            if username == self.instance.username:
                return username
        # Vérifie si le username existe déjà pour un autre utilisateur
        if Utilisateur.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ajout des classes Bootstrap par défaut
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                if isinstance(field.widget, forms.Select):
                    field.widget.attrs['class'] = 'form-select'
                elif isinstance(field.widget, forms.FileInput):
                    field.widget.attrs['class'] = 'form-control'
                else:
                    field.widget.attrs['class'] = 'form-control'

            # Ajout de placeholders
            if field_name in ['username', 'email', 'first_name', 'last_name', 'postnom']:
                field.widget.attrs['placeholder'] = f"Entrez {field.label.lower()}"

        # Si c'est une modification, rendre les champs de mot de passe optionnels
        if self.instance.pk:
            self.fields['password1'].required = False
            self.fields['password2'].required = False
            self.fields['password1'].help_text = "Laissez vide pour garder le mot de passe actuel."
            self.fields['password2'].help_text = "Laissez vide pour garder le mot de passe actuel."

            # Préserver la date de naissance existante
            if self.instance.date_naissance:
                self.initial['date_naissance'] = self.instance.date_naissance.strftime('%Y-%m-%d')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Si c'est une création, les mots de passe sont obligatoires
        if not self.instance.pk and (not password1 or not password2):
            raise ValidationError("Les mots de passe sont obligatoires pour la création d'un utilisateur.")

        # Si les mots de passe sont fournis, ils doivent correspondre
        if password1 and password2 and password1 != password2:
            raise ValidationError("Les deux mots de passe ne correspondent pas.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Ne mettre à jour le mot de passe que s'il a été fourni
        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
