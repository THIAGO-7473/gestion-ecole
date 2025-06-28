from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import PersonnelAdministratif, Enseignant, SpecialiteEnseignant, DocumentPersonnel, Tuteur, Sanction, FichierPreuve
from .forms import PersonnelForm, EnseignantForm, DocumentPersonnelForm, SanctionForm
from django.db import models
from django.db.models import Q
from django.http import HttpResponse
from .resources import PersonnelAdministratifResource, EnseignantResource
import tablib
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import csv
import xlwt
import xlsxwriter
from io import BytesIO
from reportlab.pdfgen import canvas
import pandas as pd
from django.utils import timezone
import json

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'staff/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Statistiques générales
        context['total_personnel'] = PersonnelAdministratif.objects.count()
        context['total_enseignants'] = Enseignant.objects.count()
        context['total_sanctions'] = Sanction.objects.count()
        context['total_documents'] = DocumentPersonnel.objects.count()
        context['total_specialites'] = SpecialiteEnseignant.objects.count()
        context['total_tuteurs'] = Tuteur.objects.count()

        context['personnel_actif'] = PersonnelAdministratif.objects.filter(statut='actif').count()
        context['enseignants_actifs'] = Enseignant.objects.filter(statut='actif').count()
        context['sanctions_en_attente'] = Sanction.objects.filter(statut='en_attente').count()
        context['sanctions_appliquees'] = Sanction.objects.filter(statut='appliquee').count()
        context['sanctions_annulees'] = Sanction.objects.filter(statut='annulee').count()
        context['sanctions_contestees'] = Sanction.objects.filter(statut='contestee').count()

        # Préparer les données pour le graphique
        sanctions_data = {
            'labels': [
                'Avertissement oral',
                'Avertissement écrit',
                'Blâme',
                'Retenue sur salaire',
                'Suspension',
                'Licenciement',
                'Autre'
            ],
            'values': [
                Sanction.objects.filter(type_sanction='avertissement_oral').count(),
                Sanction.objects.filter(type_sanction='avertissement_ecrit').count(),
                Sanction.objects.filter(type_sanction='blame').count(),
                Sanction.objects.filter(type_sanction='retenue_salaire').count(),
                Sanction.objects.filter(type_sanction='suspension').count(),
                Sanction.objects.filter(type_sanction='licenciement').count(),
                Sanction.objects.filter(type_sanction='autre').count()
            ]
        }
        context['sanctions_data'] = json.dumps(sanctions_data)

        # Dernières sanctions
        context['dernieres_sanctions'] = Sanction.objects.select_related(
            'enseignant', 'personnel'
        ).order_by('-date_sanction')[:5]

        return context

class PersonnelListView(LoginRequiredMixin, ListView):
    model = PersonnelAdministratif
    template_name = 'staff/personnel_list.html'
    context_object_name = 'personnel'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role_choices'] = PersonnelAdministratif.ROLE_CHOICES
        context['statut_choices'] = PersonnelAdministratif.STATUT_CHOICES
        context['current_search'] = self.request.GET.get('search', '')
        context['current_role'] = self.request.GET.get('role', 'all')
        context['current_statut'] = self.request.GET.get('statut', 'all')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        role = self.request.GET.get('role')
        statut = self.request.GET.get('statut')

        if search:
            queryset = queryset.filter(
                nom__icontains=search
            ) | queryset.filter(
                postnom__icontains=search
            ) | queryset.filter(
                prenom__icontains=search
            ) | queryset.filter(
                email__icontains=search
            )

        if role and role != 'all':
            queryset = queryset.filter(role=role)

        if statut and statut != 'all':
            queryset = queryset.filter(statut=statut)

        return queryset

class PersonnelCreateView(LoginRequiredMixin, CreateView):
    model = PersonnelAdministratif
    form_class = PersonnelForm
    template_name = 'staff/personnel_form.html'
    success_url = reverse_lazy('staff:personnel_list')

    def form_valid(self, form):
        messages.success(self.request, 'Le personnel administratif a été créé avec succès.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Veuillez corriger les erreurs ci-dessous.')
        return super().form_invalid(form)

class PersonnelUpdateView(LoginRequiredMixin, UpdateView):
    model = PersonnelAdministratif
    form_class = PersonnelForm
    template_name = 'staff/personnel_form.html'
    success_url = reverse_lazy('staff:personnel_list')

    def form_valid(self, form):
        messages.success(self.request, 'Le personnel administratif a été mis à jour avec succès.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Veuillez corriger les erreurs ci-dessous.')
        return super().form_invalid(form)

class PersonnelDeleteView(LoginRequiredMixin, DeleteView):
    model = PersonnelAdministratif
    template_name = 'staff/personnel_confirm_delete.html'
    success_url = reverse_lazy('staff:personnel_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Le personnel administratif a été supprimé avec succès.')
        return super().delete(request, *args, **kwargs)

# Vues pour les enseignants
class EnseignantListView(LoginRequiredMixin, ListView):
    model = Enseignant
    template_name = 'staff/enseignant_list.html'
    context_object_name = 'enseignants'
    paginate_by = 10

    def get_queryset(self):
        queryset = Enseignant.objects.all()
        search_query = self.request.GET.get('search')
        statut_filter = self.request.GET.get('statut')
        lieu_filter = self.request.GET.get('lieu_affectation')

        if search_query:
            queryset = queryset.filter(
                Q(nom__icontains=search_query) |
                Q(postnom__icontains=search_query) |
                Q(prenom__icontains=search_query) |
                Q(matricule__icontains=search_query)
            )

        if statut_filter and statut_filter != 'all':
            queryset = queryset.filter(statut=statut_filter)

        if lieu_filter and lieu_filter != 'all':
            queryset = queryset.filter(lieu_affectation=lieu_filter)

        return queryset.order_by('nom', 'postnom', 'prenom')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_search'] = self.request.GET.get('search', '')
        context['current_statut'] = self.request.GET.get('statut', 'all')
        context['current_lieu'] = self.request.GET.get('lieu_affectation', 'all')
        context['statut_choices'] = Enseignant.STATUT_CHOICES
        context['lieu_choices'] = Enseignant.objects.values_list('lieu_affectation', 'lieu_affectation').distinct()
        return context

class EnseignantCreateView(LoginRequiredMixin, CreateView):
    model = Enseignant
    template_name = 'staff/enseignant_form.html'
    form_class = EnseignantForm
    success_url = reverse_lazy('staff:enseignant_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"L'enseignant {form.instance.get_full_name()} a été créé avec succès.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Veuillez corriger les erreurs dans le formulaire.")
        return self.render_to_response(self.get_context_data(form=form))

class EnseignantUpdateView(LoginRequiredMixin, UpdateView):
    model = Enseignant
    form_class = EnseignantForm
    template_name = 'staff/enseignant_form.html'
    success_url = reverse_lazy('staff:enseignant_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modifier un Enseignant'
        context['action'] = 'Modifier'
        context['is_update'] = True
        context['anciennete'] = self.object.calculer_anciennete()
        return context

    def get_initial(self):
        initial = super().get_initial()
        if self.object:
            # Formatage des dates pour l'affichage dans le formulaire
            initial['date_naissance'] = self.object.date_naissance.strftime('%Y-%m-%d') if self.object.date_naissance else None
            initial['date_engagement'] = self.object.date_engagement.strftime('%Y-%m-%d') if self.object.date_engagement else None

            # Initialisation des autres champs
            initial['anciennete'] = self.object.anciennete
            initial['anciennete_unite'] = self.object.anciennete_unite
            initial['anciennete_grade'] = self.object.anciennete_grade
            initial['anciennete_grade_unite'] = self.object.anciennete_grade_unite
            initial['cote'] = self.object.cote
            initial['salaire_base'] = self.object.salaire_base
            initial['devise'] = self.object.devise
            initial['acte_nom'] = self.object.acte_nom
        return initial

    def form_valid(self, form):
        try:
            # Récupération des données du formulaire
            anciennete = form.cleaned_data.get('anciennete')
            anciennete_unite = form.cleaned_data.get('anciennete_unite')
            anciennete_grade = form.cleaned_data.get('anciennete_grade')
            anciennete_grade_unite = form.cleaned_data.get('anciennete_grade_unite')
            cote = form.cleaned_data.get('cote')
            salaire_base = form.cleaned_data.get('salaire_base')
            devise = form.cleaned_data.get('devise')
            acte_nom = form.cleaned_data.get('acte_nom')

            # Mise à jour de l'objet
            self.object = form.save(commit=False)
            self.object.anciennete = anciennete
            self.object.anciennete_unite = anciennete_unite
            self.object.anciennete_grade = anciennete_grade
            self.object.anciennete_grade_unite = anciennete_grade_unite
            self.object.cote = cote
            self.object.salaire_base = salaire_base
            self.object.devise = devise
            self.object.acte_nom = acte_nom
            self.object.save()

            messages.success(self.request, 'Enseignant modifié avec succès.')
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f'Erreur lors de la modification : {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Veuillez corriger les erreurs dans le formulaire.')
        return super().form_invalid(form)

class EnseignantDeleteView(LoginRequiredMixin, DeleteView):
    model = Enseignant
    template_name = 'staff/enseignant_confirm_delete.html'
    success_url = reverse_lazy('staff:enseignant_list')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, "L'enseignant a été supprimé avec succès.")
        return response

@login_required
def import_personnel(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        format_type = request.POST.get('format_type')

        if not file:
            messages.error(request, 'Veuillez sélectionner un fichier.')
            return redirect('staff:accueil')

        try:
            if format_type == 'csv':
                # Lecture du fichier CSV
                decoded_file = file.read().decode('utf-8').splitlines()
                reader = csv.DictReader(decoded_file)

                for row in reader:
                    # Création d'un nouveau personnel administratif
                    PersonnelAdministratif.objects.create(
                        nom=row.get('nom', ''),
                        postnom=row.get('postnom', ''),
                        prenom=row.get('prenom', ''),
                        date_naissance=row.get('date_naissance'),
                        adresse=row.get('adresse', ''),
                        telephone=row.get('telephone', ''),
                        email=row.get('email', ''),
                        role=row.get('role', ''),
                        statut=row.get('statut', 'actif'),
                        salaire_base=row.get('salaire_base', 0),
                        devise=row.get('devise', 'USD')
                    )

            elif format_type == 'excel':
                # Lecture du fichier Excel
                df = pd.read_excel(file)

                for _, row in df.iterrows():
                    PersonnelAdministratif.objects.create(
                        nom=row.get('nom', ''),
                        postnom=row.get('postnom', ''),
                        prenom=row.get('prenom', ''),
                        date_naissance=row.get('date_naissance'),
                        adresse=row.get('adresse', ''),
                        telephone=row.get('telephone', ''),
                        email=row.get('email', ''),
                        role=row.get('role', ''),
                        statut=row.get('statut', 'actif'),
                        salaire_base=row.get('salaire_base', 0),
                        devise=row.get('devise', 'USD')
                    )

            messages.success(request, 'Importation du personnel administratif réussie.')
            return redirect('staff:personnel_list')

        except Exception as e:
            messages.error(request, f'Erreur lors de l\'importation : {str(e)}')
            return redirect('staff:accueil')

    return redirect('staff:accueil')

@login_required
def export_personnel(request, format_type):
    response = HttpResponse(content_type='text/csv' if format_type == 'csv' else
                          'application/vnd.ms-excel' if format_type == 'xls' else
                          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' if format_type == 'xlsx' else
                          'application/pdf')

    filename = f'personnel_administratif.{format_type}'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    queryset = PersonnelAdministratif.objects.all()
    fields = ['nom', 'postnom', 'prenom', 'date_naissance', 'adresse', 'telephone',
              'email', 'role', 'statut', 'salaire_base', 'devise']

    if format_type == 'csv':
        writer = csv.writer(response)
        writer.writerow(fields)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in fields])

    elif format_type == 'xls':
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Personnel Administratif')
        for col, field in enumerate(fields):
            ws.write(0, col, field)
        for row, obj in enumerate(queryset, 1):
            for col, field in enumerate(fields):
                ws.write(row, col, str(getattr(obj, field)))
        wb.save(response)

    elif format_type == 'xlsx':
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Personnel Administratif')
        for col, field in enumerate(fields):
            worksheet.write(0, col, field)
        for row, obj in enumerate(queryset, 1):
            for col, field in enumerate(fields):
                worksheet.write(row, col, str(getattr(obj, field)))
        workbook.close()
        output.seek(0)
        response.write(output.read())

    elif format_type == 'pdf':
        # Création du document PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
        elements = []

        # Style pour l'en-tête
        styles = getSampleStyleSheet()
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Centré
        )
        header = Paragraph("Liste du Personnel Administratif", header_style)
        elements.append(header)

        # Préparation des données pour le tableau
        data = [fields]  # En-tête
        for obj in queryset:
            row = []
            for field in fields:
                value = getattr(obj, field)
                if field == 'date_naissance':
                    value = value.strftime('%d/%m/%Y') if value else ''
                elif field == 'salaire_base':
                    value = f"{value} {obj.devise}" if value else ''
                row.append(str(value) if value is not None else '')
            data.append(row)

        # Création du tableau
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)
        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

    return response

@login_required
def export_enseignant(request, format):
    response = HttpResponse(content_type='text/csv' if format == 'csv' else
                          'application/vnd.ms-excel' if format == 'xls' else
                          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' if format == 'xlsx' else
                          'application/pdf')

    filename = f'enseignants.{format}'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    queryset = Enseignant.objects.all()
    fields = [
        'matricule', 'nom', 'postnom', 'prenom', 'sexe', 'date_naissance',
        'nationalite', 'adresse', 'telephone', 'email', 'situation_familiale',
        'date_engagement', 'anciennete', 'anciennete_grade', 'grade_echeant',
        'acte_nom', 'diplome', 'etat_civil', 'cote', 'lieu_affectation',
        'statut', 'salaire_base', 'charge_horaire'
    ]

    if format == 'csv':
        writer = csv.writer(response)
        writer.writerow(fields)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in fields])

    elif format == 'xls':
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Enseignants')
        for col, field in enumerate(fields):
            ws.write(0, col, field)
        for row, obj in enumerate(queryset, 1):
            for col, field in enumerate(fields):
                ws.write(row, col, str(getattr(obj, field)))
        wb.save(response)

    elif format == 'xlsx':
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Enseignants')
        for col, field in enumerate(fields):
            worksheet.write(0, col, field)
        for row, obj in enumerate(queryset, 1):
            for col, field in enumerate(fields):
                worksheet.write(row, col, str(getattr(obj, field)))
        workbook.close()
        output.seek(0)
        response.write(output.read())

    elif format == 'pdf':
        # Création du document PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
        elements = []

        # Style pour l'en-tête
        styles = getSampleStyleSheet()
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Centré
        )
        header = Paragraph("Liste des Enseignants", header_style)
        elements.append(header)

        # Préparation des données pour le tableau
        data = [fields]  # En-tête
        for obj in queryset:
            row = []
            for field in fields:
                value = getattr(obj, field)
                if field == 'date_naissance' or field == 'date_engagement':
                    value = value.strftime('%d/%m/%Y') if value else ''
                elif field == 'anciennete':
                    value = f"{int(value)} {obj.anciennete_unite}" if value else ''
                elif field == 'anciennete_grade':
                    value = f"{int(value)} {obj.anciennete_grade_unite}" if value else ''
                elif field == 'cote':
                    value = f"{value} %" if value else ''
                elif field == 'salaire_base':
                    value = f"{value} {obj.devise}" if value else ''
                row.append(str(value) if value is not None else '')
            data.append(row)

        # Création du tableau
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))

        elements.append(table)
        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

    return response

@login_required
def export_utilisateur(request, format):
    response = HttpResponse(content_type='text/csv' if format == 'csv' else
                          'application/vnd.ms-excel' if format == 'xls' else
                          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' if format == 'xlsx' else
                          'application/pdf')

    filename = f'utilisateurs.{format}'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    queryset = User.objects.all()
    fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'date_joined', 'last_login']

    if format == 'csv':
        writer = csv.writer(response)
        writer.writerow(fields)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in fields])

    elif format == 'xls':
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Utilisateurs')
        for col, field in enumerate(fields):
            ws.write(0, col, field)
        for row, obj in enumerate(queryset, 1):
            for col, field in enumerate(fields):
                ws.write(row, col, str(getattr(obj, field)))
        wb.save(response)

    elif format == 'xlsx':
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Utilisateurs')
        for col, field in enumerate(fields):
            worksheet.write(0, col, field)
        for row, obj in enumerate(queryset, 1):
            for col, field in enumerate(fields):
                worksheet.write(row, col, str(getattr(obj, field)))
        workbook.close()
        output.seek(0)
        response.write(output.read())

    elif format == 'pdf':
        # Création du document PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
        elements = []

        # Style pour l'en-tête
        styles = getSampleStyleSheet()
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Centré
        )
        header = Paragraph("Liste des Utilisateurs", header_style)
        elements.append(header)

        # Préparation des données pour le tableau
        data = [fields]  # En-tête
        for obj in queryset:
            row = []
            for field in fields:
                value = getattr(obj, field)
                if field == 'date_joined' or field == 'last_login':
                    value = value.strftime('%d/%m/%Y %H:%M') if value else ''
                elif field == 'is_active':
                    value = 'Actif' if value else 'Inactif'
                row.append(str(value) if value is not None else '')
            data.append(row)

        # Création du tableau
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))

        elements.append(table)
        doc.build(elements)
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

    return response

# Vues pour SpecialiteEnseignant
class SpecialiteEnseignantListView(LoginRequiredMixin, ListView):
    model = SpecialiteEnseignant
    template_name = 'staff/specialite_list.html'
    context_object_name = 'specialites'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(enseignant__nom__icontains=search_query) |
                Q(enseignant__postnom__icontains=search_query) |
                Q(enseignant__prenom__icontains=search_query) |
                Q(matiere__nom__icontains=search_query)
            )
        return queryset.order_by('enseignant__nom', 'enseignant__postnom', 'enseignant__prenom')

class SpecialiteEnseignantCreateView(LoginRequiredMixin, CreateView):
    model = SpecialiteEnseignant
    template_name = 'staff/specialite_form.html'
    fields = ['enseignant', 'matiere', 'niveau_competence', 'annees_experience']
    success_url = reverse_lazy('staff:specialite_list')

    def form_valid(self, form):
        messages.success(self.request, 'Spécialité ajoutée avec succès.')
        return super().form_valid(form)

class SpecialiteEnseignantUpdateView(LoginRequiredMixin, UpdateView):
    model = SpecialiteEnseignant
    template_name = 'staff/specialite_form.html'
    fields = ['enseignant', 'matiere', 'niveau_competence', 'annees_experience']
    success_url = reverse_lazy('staff:specialite_list')

    def form_valid(self, form):
        messages.success(self.request, 'Spécialité mise à jour avec succès.')
        return super().form_valid(form)

class SpecialiteEnseignantDeleteView(LoginRequiredMixin, DeleteView):
    model = SpecialiteEnseignant
    template_name = 'staff/specialite_confirm_delete.html'
    success_url = reverse_lazy('staff:specialite_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Spécialité supprimée avec succès.')
        return super().delete(request, *args, **kwargs)

# Vues pour DocumentPersonnel
class DocumentPersonnelListView(LoginRequiredMixin, ListView):
    model = DocumentPersonnel
    template_name = 'staff/document_list.html'
    context_object_name = 'documents'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('fichiers')
        search_query = self.request.GET.get('search')
        type_doc = self.request.GET.get('type_document')

        if search_query:
            queryset = queryset.filter(
                Q(titre__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(enseignant__nom__icontains=search_query) |
                Q(personnel__nom__icontains=search_query)
            )

        if type_doc:
            queryset = queryset.filter(type_document=type_doc)

        return queryset.order_by('-date_depot')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_choices'] = DocumentPersonnel.TYPE_CHOICES
        return context

class DocumentPersonnelCreateView(LoginRequiredMixin, CreateView):
    model = DocumentPersonnel
    form_class = DocumentPersonnelForm
    template_name = 'staff/document_form.html'
    success_url = reverse_lazy('staff:document_list')

    def get_initial(self):
        return {
            'date_depot': timezone.now().date()
        }

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Le document a été créé avec succès.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Veuillez corriger les erreurs dans le formulaire.')
        return super().form_invalid(form)

class DocumentPersonnelUpdateView(LoginRequiredMixin, UpdateView):
    model = DocumentPersonnel
    form_class = DocumentPersonnelForm
    template_name = 'staff/document_form.html'
    success_url = reverse_lazy('staff:document_list')

    def get_initial(self):
        initial = super().get_initial()
        if self.object:
            initial['date_depot'] = self.object.date_depot
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.object:
            form.fields['date_depot'].initial = self.object.date_depot
        return form

    def form_valid(self, form):
        # Si aucune nouvelle date n'est fournie, conserver l'ancienne date
        if not form.cleaned_data.get('date_depot') and self.object:
            form.instance.date_depot = self.object.date_depot
        messages.success(self.request, 'Document mis à jour avec succès.')
        return super().form_valid(form)

class DocumentPersonnelDeleteView(LoginRequiredMixin, DeleteView):
    model = DocumentPersonnel
    template_name = 'staff/document_confirm_delete.html'
    success_url = reverse_lazy('staff:document_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Document supprimé avec succès.')
        return super().delete(request, *args, **kwargs)

# Vues pour Tuteur
class TuteurListView(LoginRequiredMixin, ListView):
    model = Tuteur
    template_name = 'staff/tuteur_list.html'
    context_object_name = 'tuteurs'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(nom__icontains=search_query) |
                Q(postnom__icontains=search_query) |
                Q(prenom__icontains=search_query) |
                Q(profession__icontains=search_query)
            )
        return queryset.order_by('nom', 'postnom', 'prenom')

class TuteurCreateView(LoginRequiredMixin, CreateView):
    model = Tuteur
    template_name = 'staff/tuteur_form.html'
    fields = ['nom', 'postnom', 'prenom', 'contact_tuteur', 'email', 'profession']
    success_url = reverse_lazy('staff:tuteur_list')

    def form_valid(self, form):
        messages.success(self.request, 'Tuteur ajouté avec succès.')
        return super().form_valid(form)

class TuteurUpdateView(LoginRequiredMixin, UpdateView):
    model = Tuteur
    template_name = 'staff/tuteur_form.html'
    fields = ['nom', 'postnom', 'prenom', 'contact_tuteur', 'email', 'profession']
    success_url = reverse_lazy('staff:tuteur_list')

    def form_valid(self, form):
        messages.success(self.request, 'Tuteur mis à jour avec succès.')
        return super().form_valid(form)

class TuteurDeleteView(LoginRequiredMixin, DeleteView):
    model = Tuteur
    template_name = 'staff/tuteur_confirm_delete.html'
    success_url = reverse_lazy('staff:tuteur_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Tuteur supprimé avec succès.')
        return super().delete(request, *args, **kwargs)

# Vues pour Sanction
class SanctionListView(LoginRequiredMixin, ListView):
    model = Sanction
    template_name = 'staff/sanction_list.html'
    context_object_name = 'sanctions'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search')
        type_sanction = self.request.GET.get('type_sanction')
        statut = self.request.GET.get('statut')

        if search_query:
            queryset = queryset.filter(
                Q(reference__icontains=search_query) |
                Q(motif__icontains=search_query) |
                Q(enseignant__nom__icontains=search_query) |
                Q(personnel__nom__icontains=search_query)
            )

        if type_sanction:
            queryset = queryset.filter(type_sanction=type_sanction)

        if statut:
            queryset = queryset.filter(statut=statut)

        return queryset.order_by('-date_sanction')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_choices'] = Sanction.TYPE_CHOICES
        context['statut_choices'] = Sanction.STATUT_CHOICES
        return context

class SanctionCreateView(LoginRequiredMixin, CreateView):
    model = Sanction
    template_name = 'staff/sanction_form.html'
    form_class = SanctionForm
    success_url = reverse_lazy('staff:sanction_list')

    def form_valid(self, form):
        form.instance.donneur_sanction = form.cleaned_data['donneur_sanction']
        messages.success(self.request, 'Sanction ajoutée avec succès.')
        return super().form_valid(form)

class SanctionUpdateView(LoginRequiredMixin, UpdateView):
    model = Sanction
    template_name = 'staff/sanction_form.html'
    form_class = SanctionForm
    success_url = reverse_lazy('staff:sanction_list')

    def get_initial(self):
        initial = super().get_initial()
        if self.object:
            initial['date_sanction'] = self.object.date_sanction
            initial['date_effet'] = self.object.date_effet
            initial['date_validation'] = self.object.date_validation
            initial['donneur_sanction'] = self.object.donneur_sanction

            # Récupérer les descriptions des fichiers existants
            fichiers = self.object.fichiers_preuves.all()
            if fichiers:
                initial['descriptions_preuves'] = '\n'.join(
                    f.description for f in fichiers if f.description
                )
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['fichiers_existants'] = self.object.fichiers_preuves.all()
        return context

    def form_valid(self, form):
        form.instance.donneur_sanction = form.cleaned_data['donneur_sanction']

        # Si aucune nouvelle date n'est fournie, conserver l'ancienne
        if not form.cleaned_data.get('date_sanction') and self.object.date_sanction:
            form.instance.date_sanction = self.object.date_sanction
        if not form.cleaned_data.get('date_effet') and self.object.date_effet:
            form.instance.date_effet = self.object.date_effet
        if not form.cleaned_data.get('date_validation') and self.object.date_validation:
            form.instance.date_validation = self.object.date_validation

        # Gérer les fichiers de preuves
        fichiers = form.cleaned_data.get('fichiers_preuves')
        descriptions = form.cleaned_data.get('descriptions_preuves', '').split('\n')

        if fichiers:
            for i, fichier in enumerate(fichiers):
                description = descriptions[i].strip() if i < len(descriptions) else ''
                FichierPreuve.objects.create(
                    sanction=form.instance,
                    fichier=fichier,
                    description=description
                )

        messages.success(self.request, 'Sanction mise à jour avec succès.')
        return super().form_valid(form)

class SanctionDeleteView(LoginRequiredMixin, DeleteView):
    model = Sanction
    template_name = 'staff/sanction_confirm_delete.html'
    success_url = reverse_lazy('staff:sanction_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Sanction supprimée avec succès.')
        return super().delete(request, *args, **kwargs)

@login_required
def valider_sanction(request, pk):
    sanction = get_object_or_404(Sanction, pk=pk)
    if request.method == 'POST':
        sanction.statut = 'appliquee'
        sanction.date_validation = timezone.now().date()
        sanction.validation_par = request.user
        sanction.save()
        messages.success(request, 'Sanction validée avec succès.')
    return redirect('staff:sanction_list')

@login_required
def annuler_sanction(request, pk):
    sanction = get_object_or_404(Sanction, pk=pk)
    if request.method == 'POST':
        sanction.statut = 'annulee'
        sanction.save()
        messages.success(request, 'Sanction annulée avec succès.')
    return redirect('staff:sanction_list')

class SanctionDetailView(LoginRequiredMixin, DetailView):
    model = Sanction
    template_name = 'staff/sanction_detail.html'
    context_object_name = 'sanction'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fichiers_existants'] = self.object.fichiers_preuves.all()
        return context
