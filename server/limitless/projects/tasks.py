import logging
import subprocess
from pathlib import Path

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

ROOT = "/tmp"


def _download_file(file_path, name):
    if not file_path.startswith("http"):
        # Local path; File already on the machine
        return Path(settings.MEDIA_ROOT, file_path.split("/")[-1])
    logger.info(f"Downloading file: {file_path}")
    response = requests.get(file_path)
    with open(f"{ROOT}/{name}", mode="wb") as f:
        f.write(response.content)
    return f"{ROOT}/{name}"


def _get_file_name_root(file_name):
    """
    We save all files like {name}_2024-07-17T192517.{ext}
    The timestamp has a fixed length, so just trim it off
    """
    return file_name.split(".")[0][:-18]


def slice_model(project):
    _download_file(project.model_3d.url, project.model_3d.name)
    _download_file(project.print_config.url, project.print_config.name)
    ls = run_command("", "ls -la")
    logger.info(f"files look like: {ls}")
    file_name_root = _get_file_name_root(project.model_3d.name)
    file_name = f"{file_name_root}.gcode"
    run_command("", f"CuraEngine slice -v -p -l {project.model_3d.name} -j {project.print_config.name} -o {file_name}")
    return Path(ROOT, file_name)


def run_command(folder, command):
    code_root = f"{ROOT}/{folder}"
    response = subprocess.run(command, cwd=code_root, capture_output=True, shell=True)
    if response.returncode or response.stderr:
        logger.info(f"Error while running '{command}' - {response.stdout.decode('UTF-8')} - {response.stderr.decode('UTF-8')}")
    return response.stdout.decode("UTF-8").rstrip("\n")