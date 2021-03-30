from fastapi import FastAPI, Request
import json

from model_creation import create_model

app = FastAPI()

#TODO ERROR HANDLING WHEN FILE IS NOT THERE
config_map = 'configMap.json'
config = json.load(open(config_map))
model_output_names = []
if 'model_output_names' in config:
    model_output_names = config['model_output_names']

default_model_name = 'custom_model.onnx'
model = create_model(default_model_name, model_output_names)


@app.on_event("startup")
async def startup_event():
    pass


@app.get("/ping")
async def ping():
    return {"status": "alive"}


@app.post("/predict")
async def predict(request: Request):

    input_json = await request.json()
    input_data = input_json['input_data']

    prediction = model.predict(input_data)

    response = {'prediction': prediction}

    return response




