from fastapi import FastAPI, Request
import json
import sqlite3
import uuid

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
    con = sqlite3.connect('ml-starter-backend.db')
    cur = con.cursor()
    # Create table
    cur.execute('''CREATE TABLE predictions
                   (request text, prediction text )''')
    con.commit()
    con.close()
    pass

@app.on_event("shutdown")
async def shutdown_event():
    con = sqlite3.connect('ml-starter-backend.db')
    cur = con.cursor()
    cur.execute('''DROP TABLE predictions
                   ''')
    con.commit()
    con.close()
    pass



@app.get("/ping")
async def ping():
    return {"status": "alive"}


@app.get("/predictions")
async def get_predictions():
    con = sqlite3.connect('ml-starter-backend.db')
    cur = con.cursor()

    predictions = []
    for row in cur.execute("SELECT * FROM predictions"):
        predictions.append(row)

    con.close()
    return {"predictions:": predictions}


@app.post("/predictions")
async def predict(request: Request):

    input_json = await request.json()
    input_data = input_json['inputData']

    prediction = model.predict(input_data)

    response = {'prediction': str(prediction)}

    con = sqlite3.connect('ml-starter-backend.db')
    cur = con.cursor()
    sql = '''INSERT INTO predictions VALUES (?, ?)'''
    row = (str(input_data), str(response))
    cur.execute(sql, row)
    con.commit()
    con.close()

    return response




