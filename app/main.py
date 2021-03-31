from fastapi import FastAPI, Request
import json

from model_creation import create_model

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    input_data = input_json['inputData']

    prediction = model.predict(input_data)

    response = {'prediction': prediction}

    return response




