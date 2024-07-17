import logging
import subprocess

logger = logging.getLogger(__name__)

ROOT = "/tmp"


def slice_model(project):
    logger.info(f"About to slice model at location: {project.model_3d.url}")
    output = run_command("", "CuraEngine help")
    logger.info(f"Cura response: {output}")


def run_command(folder, command):
    code_root = f"{ROOT}/{folder}"
    response = subprocess.run(command, cwd=code_root, capture_output=True, shell=True)
    if response.returncode:
        logger.info(f"Error while running '{command}' - {response.stdout.decode('UTF-8')} - {response.stderr.decode('UTF-8')}")
    return response.stdout.decode("UTF-8").rstrip("\n")
