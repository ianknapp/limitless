import logging

from django.core.management.base import BaseCommand

from limitless.projects.models import Project

logger = logging.getLogger(__name__)


def create_project_test_data():
    pass


class Command(BaseCommand):
    help = "Create a bunch of dummy projects to test search, list display, etc"

    def handle(self, *args, **kwargs):
        logger.info(f"Starting management command {__name__}")
        create_project_test_data()
        logger.info(f"Finished management command {__name__}")
