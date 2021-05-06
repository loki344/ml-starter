import os
import subprocess
import sys

from backend.app.model.abstract_model import AbstractModel
from custom_model.custom_model import CustomModel
from util.file_helper import get_file


#TODO define type of outputnames
def create_model(onnx_file_path: str, model_output_names=[]) -> AbstractModel:
    print("-------------------------------------------------------------------------------------------------------")
    print("Loading ONNX-Model...")

    install_dependencies()
    return CustomModel(onnx_file_path, model_output_names)


def install_dependencies():

    if not os.environ.get('IS_IN_DOCKER', False):
        print("Not running in docker, installing dependencies from custom_requirements.txt")

        path_to_custom_requirements = get_file('custom_requirements.txt')
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", path_to_custom_requirements])


