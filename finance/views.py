from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import (
    Facture, Paiement, Depense, Revenue, Budget, Bourse,
    Retenue, FichePaiementPersonnel, FicheEmprunt, RapportGeneralFinance, Eleve
)
from .forms import (
    FactureForm, PaiementForm, DepenseForm, RevenueForm, BudgetForm,
    BourseForm, RetenueForm, FichePaiementForm, FicheEmpruntForm, RapportGeneralFinanceForm
)

# Factures
class FactureListView(LoginRequiredMixin, ListView):
    model = Facture
    template_name = 'finance/facture_list.html'
    context_object_name = 'factures'
    paginate_by = 10

    def get_queryset(self):
        return Facture.objects.select_related(
            'eleve',
            'enseignant',
            'created_by'
        ).all()

class FactureDetailView(LoginRequiredMixin, DetailView):
    model = Facture
    template_name = 'finance/facture_detail.html'

class FactureCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Facture
    form_class = FactureForm
    template_name = 'finance/facture_form.html'
    success_url = reverse_lazy('finance:facture_list')
    success_message = "La facture a été créée avec succès."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class FactureUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Facture
    form_class = FactureForm
    template_name = 'finance/facture_form.html'
    success_url = reverse_lazy('finance:facture_list')
    success_message = "La facture a été mise à jour avec succès."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class FactureDeleteView(LoginRequiredMixin, DeleteView):
    model = Facture
    template_name = 'finance/facture_confirm_delete.html'
    success_url = reverse_lazy('finance:facture_list')
    success_message = "La facture a été supprimée avec succès."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

# Paiements
class PaiementListView(ListView):
    model = Paiement
    template_name = 'finance/base_list.html'
    context_object_name = 'object_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Liste des Paiements'
        context['subtitle'] = 'Gestion des paiements'
        context['create_url'] = 'finance:paiement_create'
        context['detail_url'] = 'finance:paiement_detail'
        context['update_url'] = 'finance:paiement_update'
        context['delete_url'] = 'finance:paiement_delete'
        
        # Ajouter les listes pour les filtres
        context['eleves'] = Eleve.objects.all()
        context['factures'] = Facture.objects.all()
        
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtre par élève
        eleve_id = self.request.GET.get('eleve')
        if eleve_id:
            queryset = queryset.filter(eleve_id=eleve_id)
            
        # Filtre par facture
        facture_id = self.request.GET.get('facture')
        if facture_id:
            queryset = queryset.filter(facture_id=facture_id)
            
        # Filtre par date
        date = self.request.GET.get('date')
        if date:
            queryset = queryset.filter(date=date)
            
        return queryset.order_by('-date')

class PaiementDetailView(LoginRequiredMixin, DetailView):
    model = Paiement
    template_name = 'finance/paiement_detail.html'

class PaiementCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Paiement
    form_class = PaiementForm
    template_name = 'finance/paiement_form.html'
    success_url = reverse_lazy('finance:paiement_list')
    success_message = "Le paiement a été créé avec succès."

class PaiementUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Paiement
    form_class = PaiementForm
    template_name = 'finance/paiement_form.html'
    success_url = reverse_lazy('finance:paiement_list')
    success_message = "Le paiement a été mis à jour avec succès."

class PaiementDeleteView(LoginRequiredMixin, DeleteView):
    model = Paiement
    template_name = 'finance/paiement_confirm_delete.html'
    success_url = reverse_lazy('finance:paiement_list')
    success_message = "Le paiement a été supprimé avec succès."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

# Dépenses
class DepenseListView(LoginRequiredMixin, ListView):
    model = Depense
    template_name = 'finance/depense_list.html'
    context_object_name = 'depenses'
    paginate_by = 10

class DepenseDetailView(LoginRequiredMixin, DetailView):
    model = Depense
    template_name = 'finance/depense_detail.html'

class DepenseCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Depense
    form_class = DepenseForm
    template_name = 'finance/depense_form.html'
    success_url = reverse_lazy('finance:depense_list')
    success_message = "La dépense a été créée avec succès."

class DepenseUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Depense
    form_class = DepenseForm
    template_name = 'finance/depense_form.html'
    success_url = reverse_lazy('finance:depense_list')
    success_message = "La dépense a été mise à jour avec succès."

class DepenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Depense
    template_name = 'finance/depense_confirm_delete.html'
    success_url = reverse_lazy('finance:depense_list')
    success_message = "La dépense a été supprimée avec succès."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

# Revenus
class RevenueListView(LoginRequiredMixin, ListView):
    model = Revenue
    template_name = 'finance/revenue_list.html'
    context_object_name = 'revenus'
    paginate_by = 10

class RevenueDetailView(LoginRequiredMixin, DetailView):
    model = Revenue
    template_name = 'finance/revenue_detail.html'

class RevenueCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Revenue
    form_class = RevenueForm
    template_name = 'finance/revenue_form.html'
    success_url = reverse_lazy('finance:revenue_list')
    success_message = "Le revenu a été créé avec succès."

class RevenueUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Revenue
    form_class = RevenueForm
    template_name = 'finance/revenue_form.html'
    success_url = reverse_lazy('finance:revenue_list')
    success_message = "Le revenu a été mis à jour avec succès."

class RevenueDeleteView(LoginRequiredMixin, DeleteView):
    model = Revenue
    template_name = 'finance/revenue_confirm_delete.html'
    success_url = reverse_lazy('finance:revenue_list')
    success_message = "Le revenu a été supprimé avec succès."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

# Budgets
class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'finance/budget_list.html'
    context_object_name = 'budgets'
    paginate_by = 10

class BudgetDetailView(LoginRequiredMixin, DetailView):
    model = Budget
    template_name = 'finance/budget_detail.html'

class BudgetCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'finance/budget_form.html'
    success_url = reverse_lazy('finance:budget_list')
    success_message = "Le budget a été créé avec succès."

class BudgetUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = 'finance/budget_form.html'
    success_url = reverse_lazy('finance:budget_list')
    success_message = "Le budget a été mis à jour avec succès."

class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    template_name = 'finance/budget_confirm_delete.html'
    success_url = reverse_lazy('finance:budget_list')
    success_message = "Le budget a été supprimé avec succès."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

# Bourses
class BourseListView(LoginRequiredMixin, ListView):
    model = Bourse
    template_name = 'finance/bourse_list.html'
    context_object_name = 'bourses'
    paginate_by = 10

class BourseDetailView(LoginRequiredMixin, DetailView):
    model = Bourse
    template_name = 'finance/bourse_detail.html'

class BourseCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Bourse
    form_class = BourseForm
    template_name = 'finance/bourse_form.html'
    success_url = reverse_lazy('finance:bourse_list')
    success_message = "La bourse a été créée avec succès."

class BourseUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Bourse
    form_class = BourseForm
    template_name = 'finance/bourse_form.html'
    success_url = reverse_lazy('finance:bourse_list')
    success_message = "La bourse a été mise à jour avec succès."

class BourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Bourse
    template_name = 'finance/bourse_confirm_delete.html'
    success_url = reverse_lazy('finance:bourse_list')
    success_message = "La bourse a été supprimée avec succès."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

# Retenues
class RetenueListView(LoginRequiredMixin, ListView):
    model = Retenue
    template_name = 'finance/retenue_list.html'
    context_object_name = 'retenues'
    paginate_by = 10

class RetenueDetailView(LoginRequiredMixin, DetailView):
    model = Retenue
    template_name = 'finance/retenue_detail.html'

class RetenueCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Retenue
    form_class = RetenueForm
    template_name = 'finance/retenue_form.html'
    success_url = reverse_lazy('finance:retenue_list')
    success_message = "La retenue a été créée avec succès."

class RetenueUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Retenue
    form_class = RetenueForm
    template_name = 'finance/retenue_form.html'
    success_url = reverse_lazy('finance:retenue_list')
    success_message = "La retenue a été mise à jour avec succès."

class RetenueDeleteView(LoginRequiredMixin, DeleteView):
    model = Retenue
    template_name = 'finance/retenue_confirm_delete.html'
    success_url = reverse_lazy('finance:retenue_list')
    success_message = "La retenue a été supprimée avec succès."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

# Fiches de paiement
class FichePaiementListView(LoginRequiredMixin, ListView):
    model = FichePaiementPersonnel
    template_name = 'finance/fiche_paiement_list.html'
    context_object_name = 'fiches_paiement'
    paginate_by = 10

class FichePaiementDetailView(LoginRequiredMixin, DetailView):
    model = FichePaiementPersonnel
    template_name = 'finance/fiche_paiement_detail.html'

class FichePaiementCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = FichePaiementPersonnel
    form_class = FichePaiementForm
    template_name = 'finance/fiche_paiement_form.html'
    success_url = reverse_lazy('finance:fiche_paiement_list')
    success_message = "La fiche de paiement a été créée avec succès."

class FichePaiementUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = FichePaiementPersonnel
    form_class = FichePaiementForm
    template_name = 'finance/fiche_paiement_form.html'
    success_url = reverse_lazy('finance:fiche_paiement_list')
    success_message = "La fiche de paiement a été mise à jour avec succès."

class FichePaiementDeleteView(LoginRequiredMixin, DeleteView):
    model = FichePaiementPersonnel
    template_name = 'finance/fiche_paiement_confirm_delete.html'
    success_url = reverse_lazy('finance:fiche_paiement_list')
    success_message = "La fiche de paiement a été supprimée avec succès."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

# Emprunts
class FicheEmpruntListView(LoginRequiredMixin, ListView):
    model = FicheEmprunt
    template_name = 'finance/emprunt_list.html'
    context_object_name = 'emprunts'
    paginate_by = 10

class FicheEmpruntDetailView(LoginRequiredMixin, DetailView):
    model = FicheEmprunt
    template_name = 'finance/emprunt_detail.html'

class FicheEmpruntCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = FicheEmprunt
    form_class = FicheEmpruntForm
    template_name = 'finance/emprunt_form.html'
    success_url = reverse_lazy('finance:emprunt_list')
    success_message = "L'emprunt a été créé avec succès."

class FicheEmpruntUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = FicheEmprunt
    form_class = FicheEmpruntForm
    template_name = 'finance/emprunt_form.html'
    success_url = reverse_lazy('finance:emprunt_list')
    success_message = "L'emprunt a été mis à jour avec succès."

class FicheEmpruntDeleteView(LoginRequiredMixin, DeleteView):
    model = FicheEmprunt
    template_name = 'finance/emprunt_confirm_delete.html'
    success_url = reverse_lazy('finance:emprunt_list')
    success_message = "L'emprunt a été supprimé avec succès."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

# Rapports financiers
class RapportGeneralFinanceListView(LoginRequiredMixin, ListView):
    model = RapportGeneralFinance
    template_name = 'finance/rapport_list.html'
    context_object_name = 'rapports'
    paginate_by = 10

class RapportGeneralFinanceDetailView(LoginRequiredMixin, DetailView):
    model = RapportGeneralFinance
    template_name = 'finance/rapport_detail.html'

class RapportGeneralFinanceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = RapportGeneralFinance
    form_class = RapportGeneralFinanceForm
    template_name = 'finance/rapport_form.html'
    success_url = reverse_lazy('finance:rapport_list')
    success_message = "Le rapport financier a été créé avec succès."

class RapportGeneralFinanceUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = RapportGeneralFinance
    form_class = RapportGeneralFinanceForm
    template_name = 'finance/rapport_form.html'
    success_url = reverse_lazy('finance:rapport_list')
    success_message = "Le rapport financier a été mis à jour avec succès."

class RapportGeneralFinanceDeleteView(LoginRequiredMixin, DeleteView):
    model = RapportGeneralFinance
    template_name = 'finance/rapport_confirm_delete.html'
    success_url = reverse_lazy('finance:rapport_list')
    success_message = "Le rapport financier a été supprimé avec succès."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

class FinanceHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'finance/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Accueil Finance'
        context['subtitle'] = 'Tableau de bord financier'
        
        # Statistiques
        context['total_factures'] = Facture.objects.count()
        context['total_paiements'] = Paiement.objects.count()
        context['total_depenses'] = Depense.objects.count()
        context['total_revenus'] = Revenue.objects.count()
        
        # Dernières transactions
        dernieres_factures = Facture.objects.order_by('-date_emission')[:5]
        dernieres_paiements = Paiement.objects.order_by('-date')[:5]
        dernieres_depenses = Depense.objects.order_by('-date_depense')[:5]
        dernieres_revenus = Revenue.objects.order_by('-date_reception')[:5]
        
        transactions = []
        for facture in dernieres_factures:
            transactions.append({
                'date': facture.date_emission,
                'type': 'Facture',
                'montant': facture.montant,
                'statut': facture.get_statut_display()
            })
        
        for paiement in dernieres_paiements:
            transactions.append({
                'date': paiement.date,
                'type': 'Paiement',
                'montant': paiement.montant,
                'statut': 'Payé'
            })
        
        for depense in dernieres_depenses:
            transactions.append({
                'date': depense.date_depense,
                'type': 'Dépense',
                'montant': depense.montant,
                'statut': depense.get_statut_display()
            })
        
        for revenu in dernieres_revenus:
            transactions.append({
                'date': revenu.date_reception,
                'type': 'Revenu',
                'montant': revenu.montant,
                'statut': revenu.get_statut_display()
            })
        
        # Trier les transactions par date
        context['dernieres_transactions'] = sorted(transactions, key=lambda x: x['date'], reverse=True)[:10]
        
        return context
