import json
import logging
from os import walk
from os.path import join

from django.core.management.base import BaseCommand

from limitless.cura.tasks import run_command
from limitless.projects.models import Printer

logger = logging.getLogger(__name__)


def _get_list_of_files(folder):
    all_files = []
    for (dirpath, dirnames, filenames) in walk(folder):
        for f in filenames:
            all_files.append(join(dirpath, f).split(folder)[1])
    return all_files


class Command(BaseCommand):
    help = "Runs on release. Makes sure we have all the printers in the DB that Cura has available"

    def handle(self, *args, **kwargs):
        logger.info(f"Starting management command {__name__}")
        version = run_command("", "cat /app/cura_version.txt")
        folder = f"/app/Cura-{version}/resources/definitions/"
        file_names = _get_list_of_files(folder)
        for file_name in file_names:
            with open(f"{folder}{file_name}", "r") as f:
                data = json.loads(f.read())
                Printer.objects.get_or_create(slug=file_name, defaults={"name": data["name"], "hidden": False})
        logger.info(f"Finished management command {__name__}")
