# Generated by Django 5.0.1 on 2024-08-07 09:44

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kapver_app', '0021_caroussel1_image_caroussel1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='kapver_info',
            name='critere',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='CritereSatisfaction',
        ),
    ]