from fastapi import FastAPI, Request
import json
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from model_creation import create_model
from persistence_service import PersistenceService

app = FastAPI(
    title="ML-starter REST API",
    description="This backend provides endpoints to interact with the loaded ONNX model.",
    version="1.0.0"
)

persistence_service = PersistenceService()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#TODO move this code in initialization, define variables as class variables or so
config_map = Path('./custom_model/configMap.json')
model_output_names = None

if config_map.is_file():

    config = json.load(open(config_map))
    if 'model_output_names' in config:
        model_output_names = config['model_output_names']

    if 'input' in config:
        input_fields = config['input']

    if 'applicationName' in config:
        application_name = config['applicationName']

    if 'requestObject' in config:
        request_object = config['requestObject']

default_model_name = './custom_model/custom_model.onnx'
model = create_model(default_model_name, model_output_names)


@app.on_event("startup")
async def startup_event():

    persistence_service.initialize()
    for input_field in input_fields:
        persistence_service.save_input_field(input_field)
    pass

@app.on_event("shutdown")
async def shutdown_event():
    #Is not needed atm
  #  con = sqlite3.connect('ml-starter-backend.db')
 #   cur = con.cursor()
  #  cur.execute('''DROP TABLE predictions
   #                ''')
   # con.commit()
  #  con.close()
    pass


@app.get("/api/ping")
async def ping():
    return {"status": "alive"}


@app.get("/api/predictions")
async def get_predictions():

    return {"predictions:": persistence_service.get_all_predictions()}


#TODO make this parameter configurable
@app.post("/api/predictions",
          summary="Create a new prediction",
          description="Returns a prediction for the delivered inputData in the requestBody")
async def predict(request: Request):

    input_json = await request.json()
    input_data = input_json['inputData']

    prediction = model.predict(input_data)

    row_id = persistence_service.save_prediction(request, prediction)
    response = {"id": row_id, "prediction": prediction}

    return JSONResponse(content=response)

@app.patch("/predictions")
async def save_rating(request: Request):
    input_json = await request.json()
    prediction_id = input_json['id']
    rating = input_json['rating']
    persistence_service.save_rating(prediction_id, rating)


@app.get("/api/configs", summary="Get configuration",
         description="Returns application related properties")
async def get_configuration():

    return {'applicationName': application_name, 'inputFields': input_fields, "requestObject": request_object}

