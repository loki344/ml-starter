from fastapi import FastAPI, Request
import json
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from model_creation import create_model
from persistence_service import PersistenceService

app = FastAPI(
    title="ML-starter REST API",
    description="This backend provides endpoints to interact with the loaded ONNX model.",
    version="1.0.0"
)

persistence_service = PersistenceService()

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

#TODO move this code in initialization, define variables as class variables or so
config_map = Path('./custom_model/configMap.json')
if config_map.is_file():

    config = json.load(open(config_map))
    if 'model_output_names' in config:
        model_output_names = config['model_output_names']

    if'input' in config:
        input_fields = config['input']


default_model_name = './custom_model/custom_model.onnx'
model = create_model(default_model_name, model_output_names)


@app.on_event("startup")
async def startup_event():

    persistence_service.initialize()
    for input_field in input_fields:
        persistence_service.save_input_field(input_field)
        print(input_field)
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


class PredictionRequest(BaseModel):
    inputData: input_fields[0]['type']


@app.get("/ping")
async def ping():
    return {"status": "alive"}


@app.get("/predictions")
async def get_predictions():

    return {"predictions:": persistence_service.get_all_predictions()}


#TODO make this parameter configurable
@app.post("/predictions",
          summary="Create a new prediction",
          description="Returns a prediction for the delivered inputData in the requestBody")
async def predict(request: PredictionRequest):

    prediction = model.predict(request.inputData)

    response = {'prediction': str(prediction)}

    persistence_service.save_prediction(request, prediction)

    return response


@app.get("/input-fields", summary="Get information about the input-fields",
         description="Returns detailed information about the configured input-fields")
async def get_input_fields():

    return input_fields




