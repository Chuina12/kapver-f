# Generated by Django 5.0.1 on 2024-02-18 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kapver_app', '0002_mesfactures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mesfactures',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]