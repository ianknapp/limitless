import json
import logging

from decouple import config
from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


def loaddata(path, replacements=None, new_foreign=None, new_foreign_lookup=None, remove=None):
    """
    This is an alternative way to load a fixture
    Here we loop over the json objects in the fixture and update anything we need
    Ex: create a local test user and assign them as the owner of all projects
    """
    replacements = [] if replacements is None else replacements
    new_foreign = [] if new_foreign is None else new_foreign
    new_foreign_lookup = {} if new_foreign_lookup is None else new_foreign_lookup
    remove = [] if remove is None else remove
    data = []
    with open(path, "r") as f:
        data = json.loads(f.read())
    foreign_key_lookup = {}
    for obj in data:
        # replace key and save object
        Model = apps.get_model(obj["model"])
        creation_data = obj["fields"]
        old_pk = obj["pk"]
        for value in remove:
            creation_data.pop(value)
        for key, value in replacements:
            if value == "lookup":
                pk = creation_data[key]
                creation_data[key] = new_foreign_lookup[pk]
            else:
                creation_data[key] = value
        instance = Model(**creation_data)
        for key, value in new_foreign:
            ForeignModel = apps.get_model(value)
            instance[key] = ForeignModel.save()
        instance.save()
        foreign_key_lookup[old_pk] = instance
    return foreign_key_lookup


class Command(BaseCommand):
    help = "Create test data to seed database in dev and staging environments"

    def handle(self, *args, **kwargs):
        logger.info(f"Starting management command {__name__}")
        superuser_password = config("DJANGO_SUPERUSER_PASSWORD")
        cypress_password = config("CYPRESS_TEST_USER_PASS")
        admin = get_user_model().objects.create_superuser(
            email="admin@thinknimble.com", password=superuser_password, first_name="Admin", last_name="ThinkNimble"
        )
        get_user_model().objects.create_user(
            email="cypress@example.com", password=cypress_password, first_name="Cypress", last_name="E2E_test"
        )
        """
        Updating the below fixtures:
        heroku run python server/manage.py dumpdata --app=limitless-staging {below-command}
        Manually applying a fixture:
        heroku run python server/manage.py loaddata {fixture-name} --app=limitless-pr-{pr-number}
        """
        # projects.Printer > server/limitless/projects/fixtures/printers.json
        call_command("loaddata", "printers", verbosity=1)

        # TODO Add filaments here after we create a bunch in production
        # projects.Filament > server/limitless/projects/fixtures/filaments.json
        # call_command("loaddata", "filaments", verbosity=1)

        # NOTE - This is done this way so we can replace foreign keys in the fixture with our own
        fixture_root = "server/limitless/projects/fixtures"
        # projects.Project > server/limitless/projects/fixtures/projects.json
        replacements = [("owner", admin)]
        remove = ["settings", "created", "last_edited"]
        foreign_key_lookup = loaddata(f"{fixture_root}/projects.json", replacements, remove=remove)

        # NOTE - You can turn on USE_AWS_STORAGE in your local env and the images will fetch/load for you
        # projects.ProjectFile > server/limitless/projects/fixtures/project_files.json
        replacements = [("project", "lookup")]
        remove = ["created", "last_edited"]
        loaddata(f"{fixture_root}/project_files.json", replacements, remove=remove, new_foreign_lookup=foreign_key_lookup)

        logger.info(f"Finished management command {__name__}")
