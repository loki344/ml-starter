import ast
from abstract_model import AbstractModel


def extract_function(function_name: str, file_path: str):

    file = open(file_path, "r")
    source_code = file.read()
    ast_tree = ast.parse(source_code)
    code = compile(ast_tree, "", mode='exec')

    namespace = {}
    exec(code, namespace)

    return namespace[function_name]


def create_model_class(source_code_path: str):

    pre_process = extract_function("pre_process", source_code_path)
    post_process = extract_function("post_process", source_code_path)

    dynamic_model = type("DynamicModel", (AbstractModel,), {
        "pre_process": pre_process,
        "post_process": post_process
    })

    return dynamic_model()


    # Import dependencies?
