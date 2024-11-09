# Generated by Django 5.0.1 on 2024-02-20 14:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kapver_app', '0004_alter_mesfactures_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Masignature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sig', models.FileField(upload_to='signature_travailleur')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kapver_app.employer')),
            ],
            options={
                'verbose_name': 'Masignature',
                'verbose_name_plural': 'Masignatures',
            },
        ),
    ]
