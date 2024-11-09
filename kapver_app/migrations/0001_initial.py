# Generated by Django 5.0.1 on 2024-02-18 19:14

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('intitule', models.CharField(blank=True, max_length=100, null=True)),
                ('nom', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('cv', models.FileField(upload_to='cv')),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Candidature',
                'verbose_name_plural': 'Candidatures',
            },
        ),
        migrations.CreateModel(
            name='CandidatureEntreprise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entreprise', models.CharField(max_length=100)),
                ('phone', models.IntegerField()),
                ('domain', models.CharField(max_length=100)),
                ('adresse_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('adresse', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('lu', models.BooleanField(default=False)),
                ('supprimer', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'CandidatureEntreprise',
                'verbose_name_plural': 'CandidatureEntreprises',
            },
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.CharField(max_length=150)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('facture', models.FileField(blank=True, null=True, upload_to='facture')),
            ],
            options={
                'verbose_name': 'Facture',
                'verbose_name_plural': 'Factures',
            },
        ),
        migrations.CreateModel(
            name='Offre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=100)),
                ('entreprise', models.CharField(blank=True, max_length=100, null=True)),
                ('lieu', models.CharField(blank=True, max_length=100, null=True)),
                ('nombre_heure', models.IntegerField(blank=True, null=True)),
                ('titre', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('expiration', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Offre',
                'verbose_name_plural': 'Offres',
            },
        ),
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('travailleur', models.BooleanField(default=False)),
                ('entreprise', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('membre_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'UserModel',
                'verbose_name_plural': 'UserModels',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('nom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nom_employer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Employer',
                'verbose_name_plural': 'Employers',
            },
        ),
        migrations.CreateModel(
            name='Compteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpt', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('employer', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kapver_app.employer')),
            ],
            options={
                'verbose_name': 'Compteur',
                'verbose_name_plural': 'Compteurs',
            },
        ),
        migrations.CreateModel(
            name='Entreprise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_entreprise', models.CharField(max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('adresse', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('BP', models.CharField(max_length=100)),
                ('nombre_travailler', models.IntegerField(blank=True, null=True)),
                ('gerant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partenaire', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Entreprise',
                'verbose_name_plural': 'Entreprises',
            },
        ),
        migrations.AddField(
            model_name='employer',
            name='entreprise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entreprseE', to='kapver_app.entreprise'),
        ),
        migrations.CreateModel(
            name='Facturier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bz', models.CharField(max_length=100)),
                ('einheit', models.CharField(max_length=100)),
                ('menge', models.IntegerField()),
                ('einzelpreis', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('imprimer', models.BooleanField(default=False)),
                ('summe', models.FloatField(blank=True, null=True)),
                ('fiche', models.FileField(blank=True, null=True, upload_to='facturier')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Facturier',
                'verbose_name_plural': 'Facturiers',
            },
        ),
        migrations.CreateModel(
            name='Fiche',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fiche', models.FileField(blank=True, null=True, upload_to='fiche/')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('valider', models.BooleanField(default=False)),
                ('signer_entreprise', models.BooleanField(default=False)),
                ('signer_employer', models.BooleanField(default=False)),
                ('date_signer_entreprise', models.DateTimeField(blank=True, null=True)),
                ('date_signer_employer', models.DateTimeField(blank=True, null=True)),
                ('employer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emp', to='kapver_app.employer')),
                ('entreprise', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kapver_app.entreprise')),
            ],
            options={
                'verbose_name': 'Fiche',
                'verbose_name_plural': 'Fiches',
            },
        ),
        migrations.CreateModel(
            name='FicheEmployer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wochentag', models.CharField(max_length=100)),
                ('datum', models.DateField(auto_now_add=True)),
                ('arbeitszeit', models.TimeField()),
                ('stunden', models.TimeField()),
                ('heurejour', models.TimeField(blank=True, null=True)),
                ('valider', models.BooleanField(default=False)),
                ('heure_sp', models.FloatField(blank=True, null=True)),
                ('semaine', models.BooleanField(default=False)),
                ('entreprise', models.CharField(blank=True, max_length=100, null=True)),
                ('employer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kapver_app.employer')),
            ],
            options={
                'verbose_name': 'FicheEmployer',
                'verbose_name_plural': 'FicheEmployers',
            },
        ),
        migrations.CreateModel(
            name='Ficheentreprise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wochentag', models.CharField(max_length=100)),
                ('datum', models.DateField(auto_now_add=True)),
                ('arbeitszeit', models.TimeField()),
                ('stunden', models.TimeField()),
                ('heurejour', models.TimeField(blank=True, null=True)),
                ('valider', models.BooleanField(default=False)),
                ('employer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='kapver_app.employer')),
            ],
            options={
                'verbose_name': 'Ficheentreprise',
                'verbose_name_plural': 'Ficheentreprises',
            },
        ),
        migrations.CreateModel(
            name='Heure_sup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nh', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kapver_app.employer')),
            ],
            options={
                'verbose_name': 'Heure_sup',
                'verbose_name_plural': 'Heure_sups',
            },
        ),
        migrations.CreateModel(
            name='Candidat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('cv', models.FileField(upload_to='cv')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('lu', models.BooleanField(default=False)),
                ('supprimer', models.BooleanField(default=False)),
                ('offre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kapver_app.offre')),
            ],
            options={
                'verbose_name': 'Candidat',
                'verbose_name_plural': 'Candidats',
            },
        ),
        migrations.CreateModel(
            name='Signature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signature', models.ImageField(upload_to='signature')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('entreprise', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='kapver_app.entreprise')),
                ('gerant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Signature',
                'verbose_name_plural': 'Signatures',
            },
        ),
    ]
