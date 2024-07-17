import logging
import subprocess

import requests

logger = logging.getLogger(__name__)

ROOT = "/tmp"


def slice_model(project):
    logger.info(f"About to slice model at location: {project.model_3d.url}")
    output = run_command("", "CuraEngine help")
    logger.info(f"Cura response: {output}")
    response = requests.get(project.model_3d.url)
    with open(project.model_3d.name, mode="wb") as f:
        f.write(response.content)
    ls = run_command("", "ls -la")
    logger.info(f"files look like: {ls}")


def run_command(folder, command):
    code_root = f"{ROOT}/{folder}"
    response = subprocess.run(command, cwd=code_root, capture_output=True, shell=True)
    if response.returncode:
        logger.info(f"Error while running '{command}' - {response.stdout.decode('UTF-8')} - {response.stderr.decode('UTF-8')}")
    return response.stdout.decode("UTF-8").rstrip("\n")
