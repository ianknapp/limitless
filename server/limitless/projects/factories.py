# Factories go here
import factory

from limitless.core.factories import UserFactory

from .models import Project


class ProjectFactory(factory.Factory):
    user = factory.RelatedFactory(UserFactory, factory_related_name="project")
    title = factory.Sequence(lambda n: "Project %03d" % n)

    class Meta:
        model = Project
