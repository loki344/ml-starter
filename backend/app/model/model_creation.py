import os
import subprocess
import sys

from custom_model.custom_model import CustomModel
from file_helper import get_file
from model.abstract_model import AbstractModel


def create_model(model_file_path: str) -> AbstractModel:
    """
    Creates a CustomModel object for with the given path and model_output_names. Takes care of the custom dependencies
    in case the application is not running in docker.

    :param model_file_path: path where to .onnx file is available
    :type model_file_path: str

    :return AbstractModel class which is used in the FastAPI
    """

    print("-------------------------------------------------------------------------------------------------------")
    print("Loading model...")

    install_dependencies()
    return CustomModel(model_file_path)


def install_dependencies() -> None:
    """
    If the application is not running in docker, this method will install the dependencies
    from the custom_requirements.txt via the commandline and pip.

    :return None
    """
    if not os.environ.get('IS_IN_DOCKER', False):
        print("Not running in docker, installing dependencies from custom_requirements.txt")
        if not get_file('custom_requirements.txt').is_file():
            return

        path_to_custom_requirements = get_file('custom_requirements.txt')
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", path_to_custom_requirements])
