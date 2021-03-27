import ast
from abstract_model import AbstractModel
import subprocess
import sys


def extract_function(function_name: str, file_path: str):

    return compile_source_code(file_path)[function_name]


def install_dependencies(file_path: str):

    file = open(file_path, "r")
    source_code = file.read()
    source_code_lines = source_code.split("\n")
    packages = []

    for line in source_code_lines:
        first_word = line.split(" ")[0]
        if first_word in ["import", "from"]:
            packages.append(line.split(" ")[1])

    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package ])

    pass


def compile_source_code(file_path: str):

    file = open(file_path, "r")
    source_code = file.read()
    ast_tree = ast.parse(source_code)
    code = compile(ast_tree, "", mode='exec')

    namespace = {}
    exec(code, namespace)
    return namespace


def create_model_class(file_path: str):

    install_dependencies(file_path
                         )
    pre_process = extract_function("pre_process", file_path)
    post_process = extract_function("post_process", file_path)


    dynamic_model = type("DynamicModel", (AbstractModel,), {
        "pre_process": pre_process,
        "post_process": post_process
    })

    return dynamic_model()



