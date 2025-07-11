# Generated by Django 5.1.7 on 2025-05-06 11:05

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import finance.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administrative', '0002_initial'),
        ('staff', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee_scolaire', models.CharField(max_length=20)),
                ('montant_prevu', models.FloatField()),
                ('montant_realise', models.FloatField(default=0)),
                ('remarques', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Depense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intitule', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('montant', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('categorie', models.CharField(choices=[('salaires', 'Salaires'), ('maintenance', 'Maintenance'), ('achat_materiel', 'Achat de matériel'), ('services', 'Services'), ('autre', 'Autre')], max_length=20)),
                ('date_depense', models.DateField()),
                ('moyen_paiement', models.CharField(choices=[('especes', 'Espèces'), ('cheque', 'Chèque'), ('virement', 'Virement bancaire'), ('mobile_money', 'Mobile Money')], max_length=20)),
                ('personne_beneficiaire', models.CharField(max_length=100)),
                ('justificatif', models.FileField(blank=True, null=True, upload_to='justificatifs/depenses/')),
                ('service_concerne', models.CharField(max_length=50)),
                ('statut', models.CharField(choices=[('en_attente', 'En attente'), ('valide', 'Validé'), ('rejete', 'Rejeté')], default='en_attente', max_length=20)),
                ('date_validation', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FicheEmprunt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emprunteur', models.CharField(max_length=100)),
                ('montant_emprunte', models.FloatField()),
                ('taux_interet', models.FloatField()),
                ('date_emprunt', models.DateField()),
                ('date_echeance', models.DateField()),
                ('montant_rembourse', models.FloatField(default=0)),
                ('statut', models.CharField(choices=[('en_cours', 'En cours'), ('rembourse', 'Remboursé'), ('en_retard', 'En retard')], default='en_cours', max_length=20)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Retenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heure_non_prestee', models.IntegerField(default=0)),
                ('impots', models.FloatField(default=0)),
                ('cotisations_sociales', models.FloatField(default=0)),
                ('pret_recu', models.FloatField(default=0)),
                ('total_retenue', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Revenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intitule', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('montant', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('date_reception', models.DateField()),
                ('moyen_paiement', models.CharField(choices=[('especes', 'Espèces'), ('cheque', 'Chèque'), ('virement', 'Virement bancaire'), ('mobile_money', 'Mobile Money')], max_length=20)),
                ('personne_payeur', models.CharField(max_length=100)),
                ('justificatif', models.FileField(blank=True, null=True, upload_to='justificatifs/revenus/')),
                ('statut', models.CharField(choices=[('en_attente', 'En attente'), ('valide', 'Validé'), ('rejete', 'Rejeté')], default='en_attente', max_length=20)),
                ('date_validation', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_beneficiaire', models.CharField(choices=[('eleve', 'Élève'), ('enseignant', 'Enseignant')], max_length=20)),
                ('montant', models.FloatField()),
                ('source', models.CharField(choices=[('etat', 'État'), ('ong', 'ONG'), ('etablissement', 'Établissement'), ('autre', 'Autre')], max_length=20)),
                ('criteres', models.TextField()),
                ('motif', models.TextField()),
                ('date_attribution', models.DateField()),
                ('justificatifs', models.FileField(blank=True, null=True, upload_to='justificatifs/bourses/')),
                ('condition', models.TextField()),
                ('date_debut', models.DateField()),
                ('date_fin', models.DateField()),
                ('beneficiaire', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bourses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FichierFacture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fichier', models.FileField(upload_to='factures/', verbose_name='Fichier')),
                ('date_upload', models.DateTimeField(auto_now_add=True, verbose_name="Date d'upload")),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Uploadé par')),
            ],
            options={
                'verbose_name': 'Fichier de facture',
                'verbose_name_plural': 'Fichiers de facture',
                'ordering': ['-date_upload'],
            },
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(default=finance.models.generate_facture_reference, editable=False, help_text='Numéro unique généré automatiquement', max_length=20, unique=True, validators=[django.core.validators.RegexValidator(message='Format de référence invalide (ex: FACT-20240515-ABCD)', regex='^FACT-\\d{8}-[A-Z]{4}$')], verbose_name='Référence')),
                ('date_emission', models.DateField(auto_now_add=True, verbose_name="Date d'émission")),
                ('date_echeance', models.DateField(blank=True, null=True, verbose_name="Date d'échéance")),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Montant TTC')),
                ('devise', models.CharField(choices=[('FC', 'Franc Congolais'), ('$', 'Dollar Américain'), ('Shs', 'Shillings Ougandais')], default='FC', max_length=3, verbose_name='Devise')),
                ('statut', models.CharField(choices=[('payee', 'Payée'), ('non_payee', 'Non payée'), ('partielle', 'Partiellement payée'), ('annulee', 'Annulée')], db_index=True, default='non_payee', max_length=20)),
                ('type', models.CharField(choices=[('frais_scolarite', 'Frais de scolarité'), ('inscription', "Frais d'inscription"), ('salaires', 'Salaires enseignants'), ('fournitures', 'Fournitures scolaires'), ('autre', 'Autre')], db_index=True, default='frais_scolarite', max_length=20)),
                ('description', models.TextField(blank=True, help_text='Détails de la facture', max_length=500)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Créée par')),
                ('eleve', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='factures', to='administrative.eleve', verbose_name='Élève lié')),
                ('enseignant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='factures', to='staff.enseignant', verbose_name='Enseignant lié')),
                ('fichiers', models.ManyToManyField(blank=True, related_name='factures', to='finance.fichierfacture', verbose_name='Fichiers joints')),
            ],
            options={
                'verbose_name': 'Facture',
                'verbose_name_plural': 'Factures',
                'ordering': ['-date_emission'],
            },
        ),
        migrations.CreateModel(
            name='Paiement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('montant', models.FloatField()),
                ('devise', models.CharField(choices=[('FC', 'Franc Congolais'), ('$', 'Dollar Américain'), ('Shs', 'Shillings Ougandais')], default='FC', max_length=3, verbose_name='Devise')),
                ('mode_paiement', models.CharField(choices=[('especes', 'Espèces'), ('cheque', 'Chèque'), ('virement', 'Virement bancaire'), ('mobile_money', 'Mobile Money')], max_length=20)),
                ('remarques', models.TextField(blank=True, null=True)),
                ('eleve', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paiements', to='administrative.eleve')),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paiements', to='finance.facture')),
            ],
        ),
        migrations.CreateModel(
            name='RapportGeneralFinance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee_scolaire', models.CharField(max_length=20)),
                ('total_revenus', models.FloatField()),
                ('total_depenses', models.FloatField()),
                ('total_bourses', models.FloatField()),
                ('solde_final', models.FloatField()),
                ('date_generation', models.DateField()),
                ('statut', models.CharField(choices=[('en_attente', 'En attente'), ('valide', 'Validé'), ('rejete', 'Rejeté')], default='en_attente', max_length=20)),
                ('observation', models.TextField(blank=True, null=True)),
                ('document_pdf', models.FileField(blank=True, null=True, upload_to='rapports/finances/')),
                ('responsable_validation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FichePaiementPersonnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_emission', models.DateField(default=django.utils.timezone.now)),
                ('date_echeance', models.DateField(blank=True, null=True)),
                ('montant_base', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('devise', models.CharField(choices=[('FC', 'Franc Congolais'), ('$', 'Dollar Américain'), ('Shs', 'Shillings Ougandais')], default='FC', max_length=3)),
                ('prime_anciennete', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('prime_charge', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('prime_risque', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('prime_transport', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('prime_logement', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('prime_autre', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('deduction_cnss', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('deduction_impot', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('deduction_autre', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('statut', models.CharField(choices=[('payee', 'Payée'), ('non_payee', 'Non payée'), ('partiellement_payee', 'Partiellement payée'), ('annulee', 'Annulée')], default='non_payee', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('enseignant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fiches_paiement', to='staff.enseignant')),
            ],
            options={
                'verbose_name': 'Fiche de paiement',
                'verbose_name_plural': 'Fiches de paiement',
                'ordering': ['-date_emission'],
                'indexes': [models.Index(fields=['statut'], name='finance_fic_statut_89ab79_idx'), models.Index(fields=['date_emission'], name='finance_fic_date_em_cfaeaf_idx'), models.Index(fields=['date_echeance'], name='finance_fic_date_ec_1adaf1_idx')],
            },
        ),
        migrations.AddIndex(
            model_name='facture',
            index=models.Index(fields=['reference'], name='finance_fac_referen_f3ba2d_idx'),
        ),
        migrations.AddIndex(
            model_name='facture',
            index=models.Index(fields=['statut', 'type'], name='finance_fac_statut_5d449b_idx'),
        ),
        migrations.AddIndex(
            model_name='facture',
            index=models.Index(fields=['date_emission', 'date_echeance'], name='finance_fac_date_em_c33176_idx'),
        ),
        migrations.AddConstraint(
            model_name='facture',
            constraint=models.CheckConstraint(condition=models.Q(('montant__gt', 0)), name='montant_positif'),
        ),
        migrations.AddConstraint(
            model_name='facture',
            constraint=models.UniqueConstraint(fields=('reference',), name='reference_unique'),
        ),
    ]
