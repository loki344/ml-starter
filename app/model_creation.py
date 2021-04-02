import subprocess
import sys

from custom_model import CustomModel


#TODO define type of outputnames
def create_model(onnx_file_path: str, model_output_names=[]):
   # install_dependencies("../external-folder/gpt2-example/custom_model.py")

    return CustomModel(onnx_file_path, model_output_names)



def install_dependencies(source_code_file_path: str):
    #TODO Handle with ast instead of string parsing
    source_code_text = read_file(source_code_file_path)
    source_code_lines = source_code_text.split("\n")
    packages = []

    for line in source_code_lines:
        first_word = line.split(" ")[0]
        if first_word in ["import", "from"]:
            packages.append(line.split(" ")[1])

    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    pass

def read_file(file_path: str):
    file = open(file_path, "r")
    text = file.read()
    return text
