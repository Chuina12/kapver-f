# Generated by Django 5.0.1 on 2024-08-06 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kapver_app', '0014_kapver_info_criteresatisfaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='kapver_info',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='kapver_info'),
        ),
    ]
