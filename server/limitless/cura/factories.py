# Factories go here
import factory

from limitless.core.factories import UserFactory
from limitless.cura.models import CuraSettings
from limitless.projects.models import Project


class SettingsFactory(factory.Factory):
    class Meta:
        model = CuraSettings


class ProjectFactory(factory.Factory):
    user = factory.RelatedFactory(UserFactory, factory_related_name="project")
    title = factory.Sequence(lambda n: "Project %03d" % n)
    settings = factory.RelatedFactory(SettingsFactory, factory_related_name="owner")

    class Meta:
        model = Project
