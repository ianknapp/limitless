from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from limitless.cura.models import CuraSettings

from .models import Project, UserProfile


@receiver(post_save, sender=get_user_model())
def init_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=Project)
def init_project_settings(sender, instance, created, **kwargs):
    if created:
        printer_settings = CuraSettings.objects.create()
        instance.settings = printer_settings
        instance.save()
