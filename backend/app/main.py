
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from model_configuration import ModelConfiguration
from persistence.mongo_db_service import MongoDbService
from persistence.sqlite_db_service import InMemoryDbService
from persistence import schemas
from model_creation import create_model

print("Starting server...")
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

configuration = ModelConfiguration()

default_model_name = './custom_model/custom_model.onnx'

model = create_model(default_model_name, configuration.model_output_names)

print("-------------------------------------------------------------------------------------------------------")
print("Configuring persistence service")
if configuration.db_name != '' and configuration.db_credentials != '' and configuration.db_user != '' and configuration.cluster_name != '':
    print('Initializing MongoDbService..')
    persistence_service = MongoDbService(configuration.cluster_name, configuration.db_name, configuration.db_user, configuration.db_credentials)
else:
    print('Initializing InMemoryDb..')
    persistence_service = InMemoryDbService(app)



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

    return {'applicationName': configuration.application_name,
            'description': configuration.description,
            'inputFields': configuration.input_fields,
            "requestObject": configuration.request_object}

