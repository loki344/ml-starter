import os
import subprocess
import sys

from model.abstract_model import AbstractModel
from custom_model.custom_model import CustomModel
from file_helper import get_file


#TODO define type of outputnames
def create_model(onnx_file_path: str, model_output_names: str = "") -> AbstractModel:
    """
    Creates a CustomModel object for with the given path and model_output_names. Takes care of the custom dependencies
    in case the application is not running in docker.

    :param onnx_file_path: path where to .onnx file is available
    :type onnx_file_path: str
    :param model_output_names: this param is used for the onnx InferenceSession, example value: [Softmax:0]
    :type model_output_names: str

    :return AbstractModel class which is used in the FastAPI
    """

    print("-------------------------------------------------------------------------------------------------------")
    print("Loading ONNX-Model...")

    install_dependencies()
    return CustomModel(onnx_file_path, model_output_names)


def install_dependencies() -> None:
    """
    If the application is not running in docker, this method will install the dependencies
    from the custom_requirements.txt via the commandline and pip.

    :return None
    """
    if not os.environ.get('IS_IN_DOCKER', False):
        print("Not running in docker, installing dependencies from custom_requirements.txt")

        path_to_custom_requirements = get_file('custom_requirements.txt')
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", path_to_custom_requirements])


