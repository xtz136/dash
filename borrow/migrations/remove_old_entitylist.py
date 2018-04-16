from django.db import migrations


def remove_old_entitylist(apps, schema_editor):
    EntityList = apps.get_model('borrow', 'EntityList')
    EntityList.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('borrow', '0002_auto_20180331_2311'),
    ]

    operations = [
        migrations.RunPython(
            remove_old_entitylist,
            reverse_code=migrations.RunPython.noop
        ),
    ]
