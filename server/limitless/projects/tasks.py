import logging
import subprocess

import requests

logger = logging.getLogger(__name__)

ROOT = "/tmp"


def _download_file(url, name):
    logger.info(f"Downloading file: {url}")
    response = requests.get(url)
    with open(f"{ROOT}/{name}", mode="wb") as f:
        f.write(response.content)


def slice_model(project):
    _download_file(project.model_3d.url, project.model_3d.name)
    _download_file(project.print_config.url, project.print_config.name)
    ls = run_command("", "ls -la")
    logger.info(f"files look like: {ls}")
    output = run_command("", f"CuraEngine slice -v -p -l {project.model_3d.name} -j {project.print_config.name} -o output.gcode")
    logger.info(f"Cura response: {output}")


def run_command(folder, command):
    code_root = f"{ROOT}/{folder}"
    response = subprocess.run(command, cwd=code_root, capture_output=True, shell=True)
    if response.returncode or response.stderr:
        logger.info(f"Error while running '{command}' - {response.stdout.decode('UTF-8')} - {response.stderr.decode('UTF-8')}")
    return response.stdout.decode("UTF-8").rstrip("\n")
