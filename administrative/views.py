from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import (
    Eleve, Classe, JourFerie, Matiere, Salle, EmploiDuTemps, Cours,
    Etablissement, CalendrierScolaire, Evenement, HoraireCours, Absence,
    Inscription, Examen, Note, Bulletin, Contrat, Conge, Formation, ParticipationFormation, RapportAdministratif, DocumentContrat, AttestationParticipation, DocumentConge
)
from .forms import (
    EleveForm, ClasseForm, JourFerieForm, MatiereForm, SalleForm,
    EmploiDuTempsForm, CoursForm, EtablissementForm, CalendrierScolaireForm,
    EvenementForm, HoraireCoursForm, AbsenceForm, InscriptionForm, ExamenForm,
    NoteForm, BulletinForm, ContratForm, CongeForm, FormationForm, ParticipationForm, RapportAdministratifForm
)
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def index(request):
    """Vue d'index pour l'application administrative"""
    context = {
        'eleves_count': Eleve.objects.count(),
        'classes_count': Classe.objects.count(),
        'matieres_count': Matiere.objects.count(),
        'salles_count': Salle.objects.count(),
        'cours_count': Cours.objects.count(),
        'etablissements_count': Etablissement.objects.count(),
        'calendriers_count': CalendrierScolaire.objects.count(),
        'evenements_count': Evenement.objects.count(),
        'horaires_count': EmploiDuTemps.objects.count(),
        'emplois_du_temps_count': EmploiDuTemps.objects.count(),
        'absences_count': Absence.objects.count(),
        'inscriptions_count': Inscription.objects.count(),
        'examens_count': Examen.objects.count(),
        'notes_count': Note.objects.count(),
        'bulletins_count': Bulletin.objects.count(),
        'contrats_count': Contrat.objects.count(),
        'conges_count': Conge.objects.count(),
        'formations_count': Formation.objects.count(),
        'participations_count': ParticipationFormation.objects.count(),
        'rapports_count': RapportAdministratif.objects.count(),
        'jours_feries_count': JourFerie.objects.count(),
    }
    return render(request, 'administrative/index.html', context)

@login_required
def eleve_list(request):
    query = request.GET.get('q', '')
    classe_filter = request.GET.get('classe', '')
    sexe_filter = request.GET.get('sexe', '')
    ecole_filter = request.GET.get('ecole', '')

    eleves = Eleve.objects.all()
    classes = Classe.objects.all()

    if query:
        eleves = eleves.filter(
            Q(nom__icontains=query) |
            Q(postnom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(contact_eleve__icontains=query)
        )

    if classe_filter:
        eleves = eleves.filter(classe_id=int(classe_filter))

    if sexe_filter:
        eleves = eleves.filter(sexe=sexe_filter)

    if ecole_filter:
        eleves = eleves.filter(ecole_provenance__icontains=ecole_filter)

    context = {
        'eleves': eleves,
        'classes': classes,
        'query': query,
        'classe_filter': classe_filter,
        'sexe_filter': sexe_filter,
        'ecole_filter': ecole_filter,
    }
    return render(request, 'administrative/eleve_list.html', context)

@login_required
def eleve_create(request):
    if request.method == 'POST':
        form = EleveForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Élève créé avec succès.')
            return redirect('administrative:eleve_list')
    else:
        form = EleveForm()

    context = {'form': form}
    return render(request, 'administrative/eleve_form.html', context)

@login_required
def eleve_update(request, pk):
    eleve = get_object_or_404(Eleve, pk=pk)

    if request.method == 'POST':
        form = EleveForm(request.POST, instance=eleve)
        if form.is_valid():
            form.save()
            messages.success(request, 'Élève mis à jour avec succès.')
            return redirect('administrative:eleve_list')
    else:
        form = EleveForm(instance=eleve)

    context = {'form': form, 'eleve': eleve}
    return render(request, 'administrative/eleve_form.html', context)

@login_required
def eleve_delete(request, pk):
    eleve = get_object_or_404(Eleve, pk=pk)

    if request.method == 'POST':
        eleve.delete()
        messages.success(request, 'Élève supprimé avec succès.')
        return redirect('administrative:eleve_list')

    context = {'eleve': eleve}
    return render(request, 'administrative/eleve_confirm_delete.html', context)

@login_required
def eleve_detail(request, pk):
    eleve = get_object_or_404(Eleve, pk=pk)
    context = {'eleve': eleve}
    return render(request, 'administrative/eleve_detail.html', context)

@login_required
def classe_list(request):
    query = request.GET.get('q', '')
    niveau_filter = request.GET.get('niveau', '')
    filiere_filter = request.GET.get('filiere', '')

    classes = Classe.objects.all()

    if query:
        classes = classes.filter(
            Q(nom__icontains=query) |
            Q(filiere__icontains=query)
        )

    if niveau_filter:
        classes = classes.filter(niveau=niveau_filter)

    if filiere_filter:
        classes = classes.filter(filiere__icontains=filiere_filter)

    # Récupérer les valeurs distinctes pour les filtres
    niveaux = Classe.objects.values_list('niveau', flat=True).distinct()
    filieres = Classe.objects.values_list('filiere', flat=True).distinct()

    context = {
        'classes': classes,
        'query': query,
        'niveau_filter': niveau_filter,
        'filiere_filter': filiere_filter,
        'niveaux': niveaux,
        'filieres': filieres,
    }
    return render(request, 'administrative/classe_list.html', context)

@login_required
def classe_create(request):
    if request.method == 'POST':
        form = ClasseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Classe créée avec succès.')
            return redirect('administrative:classe_list')
    else:
        form = ClasseForm()

    context = {'form': form}
    return render(request, 'administrative/classe_form.html', context)

@login_required
def classe_update(request, pk):
    classe = get_object_or_404(Classe, pk=pk)

    if request.method == 'POST':
        form = ClasseForm(request.POST, instance=classe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Classe mise à jour avec succès.')
            return redirect('administrative:classe_list')
    else:
        form = ClasseForm(instance=classe)

    context = {'form': form, 'classe': classe}
    return render(request, 'administrative/classe_form.html', context)

@login_required
def classe_delete(request, pk):
    classe = get_object_or_404(Classe, pk=pk)

    if request.method == 'POST':
        classe.delete()
        messages.success(request, 'Classe supprimée avec succès.')
        return redirect('administrative:classe_list')

    context = {'classe': classe}
    return render(request, 'administrative/classe_confirm_delete.html', context)

@login_required
def classe_detail(request, pk):
    classe = get_object_or_404(Classe, pk=pk)
    eleves = classe.eleves.all()
    context = {
        'classe': classe,
        'eleves': eleves
    }
    return render(request, 'administrative/classe_detail.html', context)

@login_required
def jour_ferie_list(request):
    jours_feries = JourFerie.objects.all()
    return render(request, 'administrative/jour_ferie_list.html', {'jours_feries': jours_feries})

@login_required
def jour_ferie_create(request):
    if request.method == 'POST':
        form = JourFerieForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jour férié créé avec succès.')
            return redirect('administrative:jour_ferie_list')
    else:
        form = JourFerieForm()
    return render(request, 'administrative/jour_ferie_form.html', {'form': form})

@login_required
def jour_ferie_update(request, pk):
    jour_ferie = get_object_or_404(JourFerie, pk=pk)
    if request.method == 'POST':
        form = JourFerieForm(request.POST, instance=jour_ferie)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jour férié mis à jour avec succès.')
            return redirect('administrative:jour_ferie_list')
    else:
        form = JourFerieForm(instance=jour_ferie)
    return render(request, 'administrative/jour_ferie_form.html', {'form': form})

@login_required
def jour_ferie_delete(request, pk):
    jour_ferie = get_object_or_404(JourFerie, pk=pk)
    if request.method == 'POST':
        jour_ferie.delete()
        messages.success(request, 'Jour férié supprimé avec succès.')
        return redirect('administrative:jour_ferie_list')
    return render(request, 'administrative/jour_ferie_confirm_delete.html', {'jour_ferie': jour_ferie})

@login_required
def matiere_list(request):
    matieres = Matiere.objects.all()
    return render(request, 'administrative/matiere_list.html', {'matieres': matieres})

@login_required
def matiere_create(request):
    if request.method == 'POST':
        form = MatiereForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matière créée avec succès.')
            return redirect('administrative:matiere_list')
    else:
        form = MatiereForm()
    return render(request, 'administrative/matiere_form.html', {'form': form})

@login_required
def matiere_update(request, pk):
    matiere = get_object_or_404(Matiere, pk=pk)
    if request.method == 'POST':
        form = MatiereForm(request.POST, instance=matiere)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matière mise à jour avec succès.')
            return redirect('administrative:matiere_list')
    else:
        form = MatiereForm(instance=matiere)
    return render(request, 'administrative/matiere_form.html', {'form': form})

@login_required
def matiere_delete(request, pk):
    matiere = get_object_or_404(Matiere, pk=pk)
    if request.method == 'POST':
        matiere.delete()
        messages.success(request, 'Matière supprimée avec succès.')
        return redirect('administrative:matiere_list')
    return render(request, 'administrative/matiere_confirm_delete.html', {'matiere': matiere})

@login_required
def salle_list(request):
    salles = Salle.objects.all()
    return render(request, 'administrative/salle_list.html', {'salles': salles})

@login_required
def salle_create(request):
    if request.method == 'POST':
        form = SalleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Salle créée avec succès.')
            return redirect('administrative:salle_list')
    else:
        form = SalleForm()
    return render(request, 'administrative/salle_form.html', {'form': form})

@login_required
def salle_update(request, pk):
    salle = get_object_or_404(Salle, pk=pk)
    if request.method == 'POST':
        form = SalleForm(request.POST, instance=salle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Salle mise à jour avec succès.')
            return redirect('administrative:salle_list')
    else:
        form = SalleForm(instance=salle)
    return render(request, 'administrative/salle_form.html', {'form': form})

@login_required
def salle_delete(request, pk):
    salle = get_object_or_404(Salle, pk=pk)
    if request.method == 'POST':
        salle.delete()
        messages.success(request, 'Salle supprimée avec succès.')
        return redirect('administrative:salle_list')
    return render(request, 'administrative/salle_confirm_delete.html', {'salle': salle})

@login_required
def emploi_du_temps_list(request):
    emplois = EmploiDuTemps.objects.all()
    return render(request, 'administrative/emploi_du_temps_list.html', {'emplois': emplois})

@login_required
def emploi_du_temps_create(request):
    if request.method == 'POST':
        form = EmploiDuTempsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Emploi du temps créé avec succès.')
            return redirect('administrative:emploi_du_temps_list')
    else:
        form = EmploiDuTempsForm()
    return render(request, 'administrative/emploi_du_temps_form.html', {'form': form})

@login_required
def emploi_du_temps_update(request, pk):
    emploi = get_object_or_404(EmploiDuTemps, pk=pk)
    if request.method == 'POST':
        form = EmploiDuTempsForm(request.POST, instance=emploi)
        if form.is_valid():
            form.save()
            messages.success(request, 'Emploi du temps mis à jour avec succès.')
            return redirect('administrative:emploi_du_temps_list')
    else:
        form = EmploiDuTempsForm(instance=emploi)
    return render(request, 'administrative/emploi_du_temps_form.html', {'form': form})

@login_required
def emploi_du_temps_delete(request, pk):
    emploi = get_object_or_404(EmploiDuTemps, pk=pk)
    if request.method == 'POST':
        emploi.delete()
        messages.success(request, 'Emploi du temps supprimé avec succès.')
        return redirect('administrative:emploi_du_temps_list')
    return render(request, 'administrative/emploi_du_temps_confirm_delete.html', {'emploi': emploi})

@login_required
def cours_list(request):
    cours = Cours.objects.all()
    return render(request, 'administrative/cours_list.html', {'cours': cours})

@login_required
def cours_create(request):
    if request.method == 'POST':
        form = CoursForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cours créé avec succès.')
            return redirect('administrative:cours_list')
    else:
        form = CoursForm()
    return render(request, 'administrative/cours_form.html', {'form': form})

@login_required
def cours_update(request, pk):
    cours = get_object_or_404(Cours, pk=pk)
    if request.method == 'POST':
        form = CoursForm(request.POST, instance=cours)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cours mis à jour avec succès.')
            return redirect('administrative:cours_list')
    else:
        form = CoursForm(instance=cours)
    return render(request, 'administrative/cours_form.html', {'form': form})

@login_required
def cours_delete(request, pk):
    cours = get_object_or_404(Cours, pk=pk)
    if request.method == 'POST':
        cours.delete()
        messages.success(request, 'Cours supprimé avec succès.')
        return redirect('administrative:cours_list')
    return render(request, 'administrative/cours_confirm_delete.html', {'cours': cours})

# Etablissement Views
@login_required
def etablissement_list(request):
    etablissements = Etablissement.objects.all()
    return render(request, 'administrative/etablissement_list.html', {'etablissements': etablissements})

@login_required
def etablissement_create(request):
    if request.method == 'POST':
        form = EtablissementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Établissement créé avec succès.')
            return redirect('administrative:etablissement_list')
    else:
        form = EtablissementForm()
    return render(request, 'administrative/etablissement_form.html', {'form': form})

@login_required
def etablissement_update(request, pk):
    etablissement = get_object_or_404(Etablissement, pk=pk)
    if request.method == 'POST':
        form = EtablissementForm(request.POST, request.FILES, instance=etablissement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Établissement mis à jour avec succès.')
            return redirect('administrative:etablissement_list')
    else:
        form = EtablissementForm(instance=etablissement)
    return render(request, 'administrative/etablissement_form.html', {'form': form, 'etablissement': etablissement})

@login_required
def etablissement_delete(request, pk):
    etablissement = get_object_or_404(Etablissement, pk=pk)
    if request.method == 'POST':
        etablissement.delete()
        messages.success(request, 'Établissement supprimé avec succès.')
        return redirect('administrative:etablissement_list')
    return render(request, 'administrative/etablissement_confirm_delete.html', {'etablissement': etablissement})

# CalendrierScolaire Views
@login_required
def calendrier_list(request):
    calendriers = CalendrierScolaire.objects.all()
    return render(request, 'administrative/calendrier_list.html', {'calendriers': calendriers})

@login_required
def calendrier_create(request):
    if request.method == 'POST':
        form = CalendrierScolaireForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Calendrier scolaire créé avec succès.')
            return redirect('administrative:calendrier_list')
    else:
        form = CalendrierScolaireForm()
    return render(request, 'administrative/calendrier_form.html', {'form': form})

@login_required
def calendrier_update(request, pk):
    calendrier = get_object_or_404(CalendrierScolaire, pk=pk)
    if request.method == 'POST':
        form = CalendrierScolaireForm(request.POST, instance=calendrier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Calendrier scolaire mis à jour avec succès.')
            return redirect('administrative:calendrier_list')
    else:
        form = CalendrierScolaireForm(instance=calendrier)
    return render(request, 'administrative/calendrier_form.html', {'form': form, 'calendrier': calendrier})

@login_required
def calendrier_delete(request, pk):
    calendrier = get_object_or_404(CalendrierScolaire, pk=pk)
    if request.method == 'POST':
        calendrier.delete()
        messages.success(request, 'Calendrier scolaire supprimé avec succès.')
        return redirect('administrative:calendrier_list')
    return render(request, 'administrative/calendrier_confirm_delete.html', {'calendrier': calendrier})

# Evenement Views
@login_required
def evenement_list(request):
    evenements = Evenement.objects.all()
    return render(request, 'administrative/evenement_list.html', {'evenements': evenements})

@login_required
def evenement_create(request):
    if request.method == 'POST':
        form = EvenementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Événement créé avec succès.')
            return redirect('administrative:evenement_list')
    else:
        form = EvenementForm()
    return render(request, 'administrative/evenement_form.html', {'form': form})

@login_required
def evenement_update(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    if request.method == 'POST':
        form = EvenementForm(request.POST, instance=evenement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Événement mis à jour avec succès.')
            return redirect('administrative:evenement_list')
    else:
        form = EvenementForm(instance=evenement)
    return render(request, 'administrative/evenement_form.html', {'form': form, 'evenement': evenement})

@login_required
def evenement_delete(request, pk):
    evenement = get_object_or_404(Evenement, pk=pk)
    if request.method == 'POST':
        evenement.delete()
        messages.success(request, 'Événement supprimé avec succès.')
        return redirect('administrative:evenement_list')
    return render(request, 'administrative/evenement_confirm_delete.html', {'evenement': evenement})

# HoraireCours Views
@login_required
def horaire_list(request):
    horaires = HoraireCours.objects.all()
    return render(request, 'administrative/horaire_list.html', {'horaires': horaires})

@login_required
def horaire_create(request):
    if request.method == 'POST':
        form = HoraireCoursForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horaire créé avec succès.')
            return redirect('administrative:horaire_list')
    else:
        form = HoraireCoursForm()
    return render(request, 'administrative/horaire_form.html', {'form': form})

@login_required
def horaire_update(request, pk):
    horaire = get_object_or_404(HoraireCours, pk=pk)
    if request.method == 'POST':
        form = HoraireCoursForm(request.POST, instance=horaire)
        if form.is_valid():
            form.save()
            messages.success(request, 'Horaire mis à jour avec succès.')
            return redirect('administrative:horaire_list')
    else:
        form = HoraireCoursForm(instance=horaire)
    return render(request, 'administrative/horaire_form.html', {'form': form, 'horaire': horaire})

@login_required
def horaire_delete(request, pk):
    horaire = get_object_or_404(HoraireCours, pk=pk)
    if request.method == 'POST':
        horaire.delete()
        messages.success(request, 'Horaire supprimé avec succès.')
        return redirect('administrative:horaire_list')
    return render(request, 'administrative/horaire_confirm_delete.html', {'horaire': horaire})

# Absence Views
@login_required
def absence_list(request):
    absences = Absence.objects.all()
    return render(request, 'administrative/absence_list.html', {'absences': absences})

@login_required
def absence_create(request):
    if request.method == 'POST':
        form = AbsenceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Absence enregistrée avec succès.')
            return redirect('administrative:absence_list')
    else:
        form = AbsenceForm()
    return render(request, 'administrative/absence_form.html', {'form': form})

@login_required
def absence_update(request, pk):
    absence = get_object_or_404(Absence, pk=pk)
    if request.method == 'POST':
        form = AbsenceForm(request.POST, instance=absence)
        if form.is_valid():
            form.save()
            messages.success(request, 'Absence mise à jour avec succès.')
            return redirect('administrative:absence_list')
    else:
        form = AbsenceForm(instance=absence)
    return render(request, 'administrative/absence_form.html', {'form': form, 'absence': absence})

@login_required
def absence_delete(request, pk):
    absence = get_object_or_404(Absence, pk=pk)
    if request.method == 'POST':
        absence.delete()
        messages.success(request, 'Absence supprimée avec succès.')
        return redirect('administrative:absence_list')
    return render(request, 'administrative/absence_confirm_delete.html', {'absence': absence})

# Inscription Views
@login_required
def inscription_list(request):
    inscriptions = Inscription.objects.all()
    return render(request, 'administrative/inscription_list.html', {'inscriptions': inscriptions})

@login_required
def inscription_create(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inscription créée avec succès.')
            return redirect('administrative:inscription_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = InscriptionForm()
    return render(request, 'administrative/inscription_form.html', {'form': form})

@login_required
def inscription_update(request, pk):
    inscription = get_object_or_404(Inscription, pk=pk)
    if request.method == 'POST':
        form = InscriptionForm(request.POST, request.FILES, instance=inscription)
        if form.is_valid():
            form.save()
            messages.success(request, 'Inscription mise à jour avec succès.')
            return redirect('administrative:inscription_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = InscriptionForm(instance=inscription)
    return render(request, 'administrative/inscription_form.html', {'form': form, 'inscription': inscription})

@login_required
def inscription_delete(request, pk):
    inscription = get_object_or_404(Inscription, pk=pk)
    if request.method == 'POST':
        inscription.delete()
        messages.success(request, 'Inscription supprimée avec succès.')
        return redirect('administrative:inscription_list')
    return render(request, 'administrative/inscription_confirm_delete.html', {'inscription': inscription})

# Examen Views
@login_required
def examen_list(request):
    examens = Examen.objects.all()
    return render(request, 'administrative/examen_list.html', {'examens': examens})

@login_required
def examen_create(request):
    if request.method == 'POST':
        form = ExamenForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Examen créé avec succès.')
            return redirect('administrative:examen_list')
    else:
        form = ExamenForm()
    return render(request, 'administrative/examen_form.html', {'form': form})

@login_required
def examen_update(request, pk):
    examen = get_object_or_404(Examen, pk=pk)
    if request.method == 'POST':
        form = ExamenForm(request.POST, instance=examen)
        if form.is_valid():
            form.save()
            messages.success(request, 'Examen mis à jour avec succès.')
            return redirect('administrative:examen_list')
    else:
        form = ExamenForm(instance=examen)
    return render(request, 'administrative/examen_form.html', {'form': form, 'examen': examen})

@login_required
def examen_delete(request, pk):
    examen = get_object_or_404(Examen, pk=pk)
    if request.method == 'POST':
        examen.delete()
        messages.success(request, 'Examen supprimé avec succès.')
        return redirect('administrative:examen_list')
    return render(request, 'administrative/examen_confirm_delete.html', {'examen': examen})

# Note Views
@login_required
def note_list(request):
    notes = Note.objects.all()
    return render(request, 'administrative/note_list.html', {'notes': notes})

@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note créée avec succès.')
            return redirect('administrative:note_list')
    else:
        form = NoteForm()
    return render(request, 'administrative/note_form.html', {'form': form})

@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note mise à jour avec succès.')
            return redirect('administrative:note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'administrative/note_form.html', {'form': form, 'note': note})

@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note supprimée avec succès.')
        return redirect('administrative:note_list')
    return render(request, 'administrative/note_confirm_delete.html', {'note': note})

# Bulletin Views
@login_required
def bulletin_list(request):
    bulletins = Bulletin.objects.all()
    return render(request, 'administrative/bulletin_list.html', {'bulletins': bulletins})

@login_required
def bulletin_create(request):
    if request.method == 'POST':
        form = BulletinForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bulletin créé avec succès.')
            return redirect('administrative:bulletin_list')
    else:
        form = BulletinForm()
    return render(request, 'administrative/bulletin_form.html', {'form': form})

@login_required
def bulletin_update(request, pk):
    bulletin = get_object_or_404(Bulletin, pk=pk)
    if request.method == 'POST':
        form = BulletinForm(request.POST, instance=bulletin)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bulletin mis à jour avec succès.')
            return redirect('administrative:bulletin_list')
    else:
        form = BulletinForm(instance=bulletin)
    return render(request, 'administrative/bulletin_form.html', {'form': form, 'bulletin': bulletin})

@login_required
def bulletin_delete(request, pk):
    bulletin = get_object_or_404(Bulletin, pk=pk)
    if request.method == 'POST':
        bulletin.delete()
        messages.success(request, 'Bulletin supprimé avec succès.')
        return redirect('administrative:bulletin_list')
    return render(request, 'administrative/bulletin_confirm_delete.html', {'bulletin': bulletin})

# Contrat Views
@login_required
def contrat_list(request):
    contrats = Contrat.objects.prefetch_related('documents').all()
    return render(request, 'administrative/contrat_list.html', {'contrats': contrats})

@login_required
def contrat_create(request):
    if request.method == 'POST':
        form = ContratForm(request.POST, request.FILES)
        if form.is_valid():
            contrat = form.save()
            messages.success(request, 'Contrat créé avec succès.')
            return redirect('administrative:contrat_list')
    else:
        form = ContratForm()
    return render(request, 'administrative/contrat_form.html', {'form': form})

@login_required
def contrat_update(request, pk):
    contrat = get_object_or_404(Contrat, pk=pk)
    if request.method == 'POST':
        form = ContratForm(request.POST, request.FILES, instance=contrat)
        if form.is_valid():
            contrat = form.save()
            messages.success(request, 'Contrat mis à jour avec succès.')
            return redirect('administrative:contrat_list')
    else:
        form = ContratForm(instance=contrat)
    return render(request, 'administrative/contrat_form.html', {'form': form, 'contrat': contrat})

@login_required
def contrat_delete(request, pk):
    contrat = get_object_or_404(Contrat, pk=pk)
    if request.method == 'POST':
        contrat.delete()
        messages.success(request, 'Contrat supprimé avec succès.')
        return redirect('administrative:contrat_list')
    return render(request, 'administrative/contrat_confirm_delete.html', {'contrat': contrat})

@login_required
def contrat_detail(request, pk):
    contrat = get_object_or_404(Contrat.objects.prefetch_related('documents'), pk=pk)
    return render(request, 'administrative/contrat_detail.html', {'contrat': contrat})

@login_required
def document_contrat_delete(request, pk):
    document = get_object_or_404(DocumentContrat, pk=pk)
    contrat_pk = document.contrat.pk
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document supprimé avec succès.')
        return redirect('administrative:contrat_update', pk=contrat_pk)
    return render(request, 'administrative/document_contrat_confirm_delete.html', {'document': document})

# Conge Views
@login_required
def conge_list(request):
    conges = Conge.objects.all()
    return render(request, 'administrative/conge_list.html', {'conges': conges})

@login_required
def conge_create(request):
    print("=== DÉBUT conge_create ===")  # Debug
    if request.method == 'POST':
        print(f"POST data: {request.POST}")  # Debug
        print(f"FILES data: {request.FILES}")  # Debug
        print(f"Nombre de fichiers: {len(request.FILES)}")  # Debug

        form = CongeForm(request.POST, request.FILES)
        print(f"Form is valid: {form.is_valid()}")  # Debug

        if form.is_valid():
            print("Form is valid, proceeding to save...")  # Debug
            try:
                conge = form.save()
                print(f"Congé créé avec succès: ID={conge.id}")  # Debug

                # Gérer les fichiers uploadés seulement s'ils existent
                if request.FILES:
                    print(f"Fichiers détectés: {request.FILES}")  # Debug
                    fichiers = request.FILES.getlist('fichiers')
                    print(f"Liste des fichiers: {fichiers}")  # Debug
                    print(f"Nombre de fichiers dans la liste: {len(fichiers)}")  # Debug

                    for i, fichier in enumerate(fichiers):
                        print(f"Traitement du fichier {i+1}: {fichier.name}")  # Debug
                        if fichier:  # Vérifier que le fichier n'est pas vide
                            print(f"Création DocumentConge pour: {fichier.name}")  # Debug
                            try:
                                DocumentConge.objects.create(
                                    conge=conge,
                                    fichier=fichier,
                                    nom=fichier.name
                                )
                                print(f"DocumentConge créé avec succès pour: {fichier.name}")  # Debug
                            except Exception as doc_error:
                                print(f"Erreur lors de la création du DocumentConge: {str(doc_error)}")  # Debug
                        else:
                            print(f"Fichier ignoré (vide): {fichier}")  # Debug
                else:
                    print("Aucun fichier détecté dans request.FILES")  # Debug

                messages.success(request, 'Congé créé avec succès.')
                print("Redirection vers conge_list...")  # Debug
                return redirect('administrative:conge_list')
            except Exception as e:
                print(f"Erreur lors de la création du congé: {str(e)}")  # Debug
                print(f"Type d'erreur: {type(e)}")  # Debug
                import traceback
                print(f"Traceback: {traceback.format_exc()}")  # Debug
                messages.error(request, f'Erreur lors de la création du congé: {str(e)}')
        else:
            print(f"Form errors: {form.errors}")  # Debug
            print(f"Form non_field_errors: {form.non_field_errors()}")  # Debug
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Erreur de champ '{field}': {error}")  # Debug
                    messages.error(request, f"{field}: {error}")
    else:
        print("Méthode GET, affichage du formulaire")  # Debug
        form = CongeForm()

    print("=== FIN conge_create ===")  # Debug
    return render(request, 'administrative/conge_form.html', {'form': form})

@login_required
def conge_update(request, pk):
    print(f"\n{'='*50}")  # Debug
    print(f"=== DÉBUT conge_update - PK: {pk} ===")  # Debug
    print(f"Method: {request.method}")  # Debug
    print(f"URL: {request.path}")  # Debug
    print(f"{'='*50}\n")  # Debug

    conge = get_object_or_404(Conge, pk=pk)
    print(f"Modification du congé ID: {pk}")  # Debug

    if request.method == 'POST':
        print(f"POST data: {request.POST}")  # Debug
        print(f"FILES data: {request.FILES}")  # Debug
        print(f"Nombre de fichiers: {len(request.FILES)}")  # Debug

        form = CongeForm(request.POST, request.FILES, instance=conge)
        print(f"Form is valid: {form.is_valid()}")  # Debug

        if form.is_valid():
            print("Form is valid, proceeding to save...")  # Debug
            try:
                conge = form.save()
                print(f"Congé mis à jour avec succès: ID={conge.id}")  # Debug

                # Gérer les fichiers uploadés seulement s'ils existent
                if request.FILES:
                    print(f"Fichiers détectés: {request.FILES}")  # Debug
                    fichiers = request.FILES.getlist('fichiers')
                    print(f"Liste des fichiers: {fichiers}")  # Debug
                    print(f"Nombre de fichiers dans la liste: {len(fichiers)}")  # Debug

                    for i, fichier in enumerate(fichiers):
                        print(f"Traitement du fichier {i+1}: {fichier.name}")  # Debug
                        if fichier:  # Vérifier que le fichier n'est pas vide
                            print(f"Création DocumentConge pour: {fichier.name}")  # Debug
                            try:
                                DocumentConge.objects.create(
                                    conge=conge,
                                    fichier=fichier,
                                    nom=fichier.name
                                )
                                print(f"DocumentConge créé avec succès pour: {fichier.name}")  # Debug
                            except Exception as doc_error:
                                print(f"Erreur lors de la création du DocumentConge: {str(doc_error)}")  # Debug
                        else:
                            print(f"Fichier ignoré (vide): {fichier}")  # Debug
                else:
                    print("Aucun fichier détecté dans request.FILES")  # Debug

                messages.success(request, 'Congé mis à jour avec succès.')
                print("Redirection vers conge_list...")  # Debug
                return redirect('administrative:conge_list')
            except Exception as e:
                print(f"Erreur lors de la mise à jour du congé: {str(e)}")  # Debug
                print(f"Type d'erreur: {type(e)}")  # Debug
                import traceback
                print(f"Traceback: {traceback.format_exc()}")  # Debug
                messages.error(request, f'Erreur lors de la mise à jour du congé: {str(e)}')
        else:
            print(f"Form errors: {form.errors}")  # Debug
            print(f"Form non_field_errors: {form.non_field_errors()}")  # Debug
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"Erreur de champ '{field}': {error}")  # Debug
                    messages.error(request, f"{field}: {error}")
    else:
        print("Méthode GET, affichage du formulaire de modification")  # Debug
        form = CongeForm(instance=conge)

    print("=== FIN conge_update ===")  # Debug
    return render(request, 'administrative/conge_form.html', {'form': form, 'conge': conge})

@login_required
def conge_delete(request, pk):
    conge = get_object_or_404(Conge, pk=pk)
    if request.method == 'POST':
        conge.delete()
        messages.success(request, 'Conge supprimé avec succès.')
        return redirect('administrative:conge_list')
    return render(request, 'administrative/conge_confirm_delete.html', {'conge': conge})

class CongeDetailView(LoginRequiredMixin, DetailView):
    model = Conge
    template_name = 'administrative/conge_detail.html'
    context_object_name = 'conge'

# Formation Views
@login_required
def formation_list(request):
    formations = Formation.objects.all()
    return render(request, 'administrative/formation_list.html', {'formations': formations})

@login_required
def formation_create(request):
    if request.method == 'POST':
        form = FormationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formation créée avec succès.')
            return redirect('administrative:formation_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = FormationForm()
    return render(request, 'administrative/formation_form.html', {'form': form})

@login_required
def formation_update(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    if request.method == 'POST':
        form = FormationForm(request.POST, instance=formation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formation mise à jour avec succès.')
            return redirect('administrative:formation_list')
    else:
        form = FormationForm(instance=formation)
    return render(request, 'administrative/formation_form.html', {'form': form, 'formation': formation})

@login_required
def formation_delete(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    if request.method == 'POST':
        formation.delete()
        messages.success(request, 'Formation supprimée avec succès.')
        return redirect('administrative:formation_list')
    return render(request, 'administrative/formation_confirm_delete.html', {'formation': formation})

@login_required
def formation_detail(request, pk):
    formation = get_object_or_404(Formation, pk=pk)
    return render(request, 'administrative/formation_detail.html', {'formation': formation})

# Participation Views
@login_required
def participation_list(request):
    participations = ParticipationFormation.objects.all()
    return render(request, 'administrative/participation_list.html', {'participations': participations})

@login_required
def participation_create(request):
    if request.method == 'POST':
        form = ParticipationForm(request.POST, request.FILES)
        if form.is_valid():
            participation = form.save()
            # Gérer les fichiers d'attestation seulement s'ils existent
            if request.FILES:
                fichiers = request.FILES.getlist('attestation_files')
                for fichier in fichiers:
                    AttestationParticipation.objects.create(
                        participation=participation,
                        fichier=fichier,
                        nom=fichier.name
                    )
            messages.success(request, 'Participation créée avec succès.')
            return redirect('administrative:participation_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ParticipationForm()
    return render(request, 'administrative/participation_form.html', {'form': form})

@login_required
def participation_update(request, pk):
    participation = get_object_or_404(ParticipationFormation, pk=pk)
    if request.method == 'POST':
        form = ParticipationForm(request.POST, request.FILES, instance=participation)
        if form.is_valid():
            participation = form.save()
            # Gérer les nouveaux fichiers d'attestation
            fichiers = request.FILES.getlist('attestation_files')
            for fichier in fichiers:
                AttestationParticipation.objects.create(
                    participation=participation,
                    fichier=fichier,
                    nom=fichier.name
                )
            messages.success(request, 'Participation mise à jour avec succès.')
            return redirect('administrative:participation_list')
    else:
        form = ParticipationForm(instance=participation)
    return render(request, 'administrative/participation_form.html', {'form': form, 'participation': participation})

@login_required
def participation_delete(request, pk):
    participation = get_object_or_404(ParticipationFormation, pk=pk)
    if request.method == 'POST':
        participation.delete()
        messages.success(request, 'Participation supprimée avec succès.')
        return redirect('administrative:participation_list')
    return render(request, 'administrative/participation_confirm_delete.html', {'participation': participation})

class ParticipationDetailView(LoginRequiredMixin, DetailView):
    model = ParticipationFormation
    template_name = 'administrative/participation_detail.html'
    context_object_name = 'participation'

# RapportAdministratif Views
@login_required
def rapport_list(request):
    rapports = RapportAdministratif.objects.all()
    return render(request, 'administrative/rapport_list.html', {'rapports': rapports})

@login_required
def rapport_create(request):
    if request.method == 'POST':
        form = RapportAdministratifForm(request.POST, request.FILES)
        if form.is_valid():
            rapport = form.save()
            messages.success(request, 'Rapport administratif créé avec succès.')
            return redirect('administrative:rapport_list')
    else:
        form = RapportAdministratifForm()
    return render(request, 'administrative/rapport_form.html', {'form': form})

@login_required
def rapport_update(request, pk):
    rapport = get_object_or_404(RapportAdministratif, pk=pk)
    if request.method == 'POST':
        form = RapportAdministratifForm(request.POST, request.FILES, instance=rapport)
        if form.is_valid():
            rapport = form.save()
            messages.success(request, 'Rapport administratif mis à jour avec succès.')
            return redirect('administrative:rapport_list')
    else:
        form = RapportAdministratifForm(instance=rapport)
    return render(request, 'administrative/rapport_form.html', {'form': form, 'rapport': rapport})

@login_required
def rapport_delete(request, pk):
    rapport = get_object_or_404(RapportAdministratif, pk=pk)
    if request.method == 'POST':
        rapport.delete()
        messages.success(request, 'Rapport administratif supprimé avec succès.')
        return redirect('administrative:rapport_list')
    return render(request, 'administrative/rapport_confirm_delete.html', {'rapport': rapport})

class RapportAdministratifDetailView(LoginRequiredMixin, DetailView):
    model = RapportAdministratif
    template_name = 'administrative/rapport_detail.html'
    context_object_name = 'rapport'
