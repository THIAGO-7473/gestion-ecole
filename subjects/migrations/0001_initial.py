# Generated by Django 5.1.7 on 2025-04-27 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Matiere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('coefficient', models.FloatField(default=1.0)),
            ],
            options={
                'verbose_name': 'Matière',
                'verbose_name_plural': 'Matières',
            },
        ),
    ]
