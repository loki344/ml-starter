import os
import subprocess
import sys

from custom_model.custom_model import CustomModel
from file_helper import get_file
from model.abstract_model import AbstractModel


def create_model() -> AbstractModel:
    """
    Creates a CustomModel object by looking for the model files. Takes care of the custom dependencies
    in case the application is not running in docker.

    :return AbstractModel class which is used in the FastAPI
    """

    print("-------------------------------------------------------------------------------------------------------")
    print("Loading model...")

    model_path = None

    if get_file("custom_model.onnx").is_file():
        model_path = "./custom_model/custom_model.onnx"
    elif get_file("custom_model.xml").is_file():
        model_path = './custom_model/custom_model.xml'
    elif get_file("custom_model.pmml").is_file():
        model_path = './custom_model/custom_model.pmml'
    else:
        raise Exception(
            "No model found. Check if there is a custom_model.onnx, custom_model.xml or custom_model.pmml "
            "in the backend/app/custom_model directory")

    install_dependencies()
    return CustomModel(model_path)


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
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", path_to_custom_requirements])
