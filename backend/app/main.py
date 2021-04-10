from fastapi import FastAPI, Request
import json
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

from backend.app.file_helper import get_file
from persistence import models, schemas
from model_creation import create_model
from persistence.database import engine, SQLALCHEMY_DATABASE_URL
from fastapi_sqlalchemy import db
from fastapi_sqlalchemy import DBSessionMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ML-starter REST API",
    description="This backend provides endpoints to interact with the loaded ONNX model.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.add_middleware(DBSessionMiddleware,
                    db_url=SQLALCHEMY_DATABASE_URL)


#TODO move this code in initialization, define variables as class variables or so
config_map = get_file('configMap.json')
model_output_names = None
description = "Please provide the data in the input fields below and start the prediction."

if config_map.is_file():

    config = json.load(open(config_map))
    if 'model_output_names' in config:
        model_output_names = config['model_output_names']

    if 'input' in config:
        input_fields = config['input']

    if 'applicationName' in config:
        application_name = config['applicationName']

    if 'description' in config:
        description = config['description']

    if 'requestObject' in config:
        request_object = config['requestObject']

default_model_name = './custom_model/custom_model.onnx'
model = create_model(default_model_name, model_output_names)


@app.on_event("startup")
async def startup_event():
    pass


@app.on_event("shutdown")
async def shutdown_event():
    pass


@app.get("/api/ping")
async def ping():
    return {"status": "alive"}


@app.get("/api/predictions")
async def get_predictions():

    return db.session.query(models.Prediction).all()


#TODO make this parameter configurable
@app.post("/api/predictions",
          summary="Create a new prediction",
          description="Returns a prediction for the delivered inputData in the requestBody",
          status_code=201)
async def predict(request: Request):
    input_json = await request.json()
    input_data = input_json['inputData']

    prediction = model.predict(input_data)

    prediction_entity = models.Prediction(input_data=str(input_data), prediction=str(prediction))
    db.session.add(prediction_entity)
    db.session.commit()
    db.session.refresh(prediction_entity)

    response = {"id": prediction_entity.id, "input_data": prediction_entity.input_data, "prediction": prediction}

    return response


@app.patch("/api/predictions", summary="Patch a prediction",
           description="Allows to patch the rating of a prediction")
async def patch_rating(prediction: schemas.PredictionPatch):

    existing_prediction = db.session.query(models.Prediction).get(prediction.id)
    existing_prediction.rating = prediction.rating
    db.session.commit()
    db.session.refresh(existing_prediction)

    return existing_prediction


@app.get("/api/configs", summary="Get configuration",
         description="Returns application related properties")
async def get_configuration():

    return {'applicationName': application_name,
            'description': description,
            'inputFields': input_fields,
            "requestObject": request_object}

