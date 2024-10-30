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


def slice_model(obj, filament_config, printer_config_filename, cura_settings_str="", minimize_supports=False):
    _download_file(obj.file.url, obj.file.name)
    # _download_file(obj.print_config.url, obj.print_config.name)
    file_name_root = _get_file_name_root(obj.file.name)
    file_name = f"{file_name_root}.gcode"
    optimize_model_position(obj.file.name, minimize_supports)
    # Need to export this here for reasons. See buildpack-run.sh
    export_cmd = "export CURA_ENGINE_SEARCH_PATH=/app/Cura-$(cat /app/cura_version.txt)/resources/definitions"
    config_path = f"$(echo $CURA_ENGINE_SEARCH_PATH)/{printer_config_filename}"
    cura_args = f"-j {config_path} -l {obj.file.name} -o /tmp/{file_name}"
    cura_command = f"{export_cmd} && CuraEngine slice {cura_args} {filament_config} {cura_settings_str}"
    logger.info(f"Running Cura with command: '{cura_command}'")
    run_command("", cura_command)
    return Path(ROOT, file_name)


def optimize_model_position(file_path, minimize_supports):
    # https://github.com/ChristophSchranz/Tweaker-3
    if settings.USE_TWEAKER:
        command = f"tweaker3 -i {file_path} -o {file_path} -vb -x"
        if minimize_supports:
            command += " --minimize surfaces"
        logger.info(f"Optimizing STL file: '{command}'")
        run_command("", command)


def run_command(folder, command):
    code_root = f"{ROOT}/{folder}"
    response = subprocess.run(command, cwd=code_root, capture_output=True, shell=True)
    if response.returncode or response.stderr:
        logger.info(f"Error while running '{command}' - {response.stdout.decode('UTF-8')} - {response.stderr.decode('UTF-8')}")
    return response.stdout.decode("UTF-8").rstrip("\n")
