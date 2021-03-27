from fastapi import FastAPI, Request
import os

#TODO: move this to a separate file and handle correct input in docker..
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

# FILE END


app = FastAPI()

#TODO, take whole path from env var
model = create_model_class('../mounted_volume/' + os.getenv('SOURCE_CODE_FILE'))
#model = create_model_class("/home/robert/Repositories/ml-starter/external-folder/test_input_method.py")

@app.on_event("startup")
async def startup_event():

    pass

@app.get("/ping")
async def ping():
    return {"status": "alive"}


@app.post("/predict")
async def predict(request: Request):
    #TODO Model should be instantiated and then only infer the session, a class which is holding all path information and the session could be helpful

    input_json = await request.json()
    input_data = input_json['input_data']

    #TODO save whole path in env var
    prediction = model.run(input_data, '../mounted_volume/' + os.getenv('MODEL_FILE_NAME'))
    #prediction = model.run(input_data, '/home/robert/Repositories/ml-starter/external-folder/iris.onnx')

    response = {'prediction': prediction}

    return response


