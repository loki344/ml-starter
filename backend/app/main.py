
from fastapi import FastAPI, Request
import json
from fastapi.middleware.cors import CORSMiddleware

from persistence.mongo_db_service import MongoDbService
from persistence.sqlite_db_service import InMemoryDbService
from file_helper import get_file
from persistence import schemas
from model_creation import create_model


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




#TODO move this code in initialization, define variables as class variables or so
config_map = get_file('configMap.json')
model_output_names = None
db_name = ''
db_credentials = ''
db_user = ''
cluster_name = ''
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

    if 'dbName' in config:
        db_name = config['dbName']

    if 'dbCredentials' in config:
        db_credentials = config['dbCredentials']

    if 'dbUser' in config:
        db_user = config['dbUser']

    if 'clusterName' in config:
        cluster_name = config['clusterName']

default_model_name = './custom_model/custom_model.onnx'
model = create_model(default_model_name, model_output_names)


if db_name != '' and db_credentials != '' and db_user != '' and cluster_name != '':
    print('Initializing MongoDbService..')
    persistence_service = MongoDbService(cluster_name, db_name, db_user, db_credentials)
else:
    print('Initializing InMemoryDb..')
    persistence_service = InMemoryDbService(app)



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

    return persistence_service.get_predictions()


#TODO make this parameter configurable
@app.post("/api/predictions",
          summary="Create a new prediction",
          description="Returns a prediction for the delivered inputData in the requestBody",
          status_code=201)
async def predict(request: Request):
    input_json = await request.json()
    input_data = input_json['inputData']

    prediction = model.predict(input_data)

    prediction_entity = persistence_service.save_prediction(str(input_data), str(prediction))
    response = {"id": str(prediction_entity.id), "input_data": prediction_entity.input_data, "prediction": prediction}

    return response


@app.patch("/api/predictions", summary="Patch a prediction",
           description="Allows to patch the rating of a prediction")
async def patch_rating(prediction: schemas.PredictionPatch):
    return persistence_service.save_rating(prediction.id, prediction.rating)


@app.get("/api/configs", summary="Get configuration",
         description="Returns application related properties")
async def get_configuration():

    return {'applicationName': application_name,
            'description': description,
            'inputFields': input_fields,
            "requestObject": request_object}

