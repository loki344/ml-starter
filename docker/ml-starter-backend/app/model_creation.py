import ast
from abstract_model import AbstractModel
import subprocess
import sys


def extract_function(function_name: str, pre_post_processing_source_file: str):
    #TODO extract all methods
    return compile_source_code(pre_post_processing_source_file)[function_name]


def install_dependencies(source_code_file_path: str):
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


def compile_source_code(source_code_file_path: str):
    source_code_text = read_file(source_code_file_path)
    ast_tree = ast.parse(source_code_text)
    code = compile(ast_tree, "", mode='exec')

    namespace = {}
    exec(code, namespace)
    return namespace


def read_file(file_path: str):
    file = open(file_path, "r")
    text = file.read()
    return text


def create_model(onnx_file_path: str, pre_post_processing_source_file: str):
    install_dependencies(pre_post_processing_source_file)

    pre_process = extract_function("pre_process", pre_post_processing_source_file)
    post_process = extract_function("post_process", pre_post_processing_source_file)

    dynamic_model = type("DynamicModel", (AbstractModel,), {
        "pre_process": pre_process,
        "post_process": post_process
    })

    return dynamic_model(onnx_file_path)



