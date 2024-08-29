# Generated by Django 3.2.6 on 2024-08-28 14:48

from django.db import migrations, models
import django.db.models.deletion


def init_settings(apps, schema_editor):
    User = apps.get_model("core", "User")
    Project = apps.get_model("projects", "Project")
    UserProfile = apps.get_model("projects", "UserProfile")
    CuraSettings = apps.get_model("cura", "CuraSettings")

    for user in User.objects.all():
        UserProfile.objects.create(user=user)

    for project in Project.objects.all():
        if not hasattr(project, "settings"):
            project.settings = CuraSettings.objects.create()
            project.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cura', '0001_initial'),
        ('projects', '0013_auto_20240827_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='settings',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project', to='cura.curasettings'),
        ),
        migrations.RunPython(init_settings, reverse_code=migrations.RunPython.noop),
    ]