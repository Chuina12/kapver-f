from django.db import migrations

def load_initial_data(apps, schema_editor):
    from django.core.management import call_command
    call_command('loaddata', 'kapver_app/fixtures/initial_data.json')

class Migration(migrations.Migration):

    dependencies = [
        ('kapver_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_initial_data),
    ]
