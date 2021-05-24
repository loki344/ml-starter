from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from configuration.configuration_service import ConfigurationService
from model.model_creation import create_model
from persistence.mongo_db_service import MongoDbService
from persistence.schemas import Prediction, PredictionPatch, PredictionCreate
from persistence.sqlite_db_service import InMemoryDbService

"""This is the entrypoint for the FastAPI application.
    start it with: uvicorn main:app --host localhost --port 8800 --reload"""

print("Starting server...")
app = FastAPI(
    title="ML-starter REST API",
    description="This backend provides endpoints to interact with the loaded model.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

configuration = ConfigurationService()
model = create_model()

templates = Jinja2Templates(directory="static/templates")
app.mount("/resources", StaticFiles(directory="static/resources"), name="resources")

print("-------------------------------------------------------------------------------------------------------")
print("Configuring persistence service")
if configuration.db_name != '' and configuration.db_credentials != '' and configuration.db_user != '' and configuration.cluster_name != '':
    print('Initializing MongoDbService..')
    persistence_service = MongoDbService(configuration.cluster_name, configuration.db_name, configuration.db_user,
                                         configuration.db_credentials)
else:
    print('Initializing InMemoryDb..')
    persistence_service = InMemoryDbService(app)


@app.get("/api/ping")
async def ping():
    return {"status": "alive"}


@app.get("/api/predictions")
async def get_predictions() -> List[Prediction]:
    return list(map(lambda prediction: prediction.__repr__(), persistence_service.get_predictions()))


@app.post("/api/predictions",
          summary="Create a new prediction",
          description="Returns a prediction for the inputData in the requestBody",
          status_code=201)
async def predict(request: PredictionCreate):
    prediction = model.predict(request.input_data)
    return persistence_service.save_prediction(str(request.input_data), str(prediction)).__repr__()


@app.patch("/api/predictions/{prediction_id}", summary="Patch a prediction",
           description="Allows to patch the rating of a prediction")
async def patch_rating(prediction: PredictionPatch, prediction_id):
    return persistence_service.save_rating(prediction_id, prediction.rating).__repr__()


@app.get("/", summary="Only for custom frontends - returns the index.html",
         description="The index.html must be located in the static/templates directory")
async def get_index_template(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/{template_name}", summary="Only for custom frontends - returns the template",
         description="The template must be located in the static/templates directory")
async def get_template_by_name(request: Request, template_name):
    return templates.TemplateResponse(template_name + ".html", {"request": request})


@app.get("/api/configs", summary="Get configuration",
         description="Returns application related properties")
async def get_configuration() -> dict:
    return {'applicationName': configuration.application_name,
            'description': configuration.description,
            'inputFields': configuration.input_fields,
            "requestObject": configuration.request_object}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8800)
