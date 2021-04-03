from fastapi import FastAPI, Request
import json
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
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


config_map = Path('./custom_model/configMap.json')
if config_map.is_file():

    config = json.load(open(config_map))
    if 'model_output_names' in config:
        model_output_names = config['model_output_names']

default_model_name = './custom_model/custom_model.onnx'
model = create_model(default_model_name, model_output_names)


@app.on_event("startup")
async def startup_event():
    persistence_service.initialize()
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



@app.get("/ping")
async def ping():
    return {"status": "alive"}


@app.get("/predictions")
async def get_predictions():

    return {"predictions:": persistence_service.get_all_predictions()}


@app.post("/predictions")
async def predict(request: Request):

    input_json = await request.json()
    input_data = input_json['inputData']

    prediction = model.predict(input_data)

    response = {'prediction': str(prediction)}

    persistence_service.save_prediction(input_data, prediction)

    return response




