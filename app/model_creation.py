import subprocess
import sys
from custom_model.custom_model import CustomModel
from file_helper import get_file




#TODO define type of outputnames
def create_model(onnx_file_path: str, model_output_names=[]):

    #TODO is only needed if it runs locally?
    #install_dependencies()
    return CustomModel(onnx_file_path, model_output_names)


def install_dependencies():

    path_to_custom_requirements = get_file('custom_requirements.txt')
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", path_to_custom_requirements])


