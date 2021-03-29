from fastapi import FastAPI, Request
import os

from model_creation import create_model

app = FastAPI()

#TODO, take whole path from env var
#model = create_model('../mounted_directory/' + os.getenv('MODEL_FILE_NAME'))
#model = create_model('../external-folder/iris-example/iris.onnx')
#TODO how can we read the additional argument dynamically??
model = create_model('/home/robert/Repositories/ml-starter-backend/app/efficientnet-lite4-11.onnx', ["Softmax:0"])


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




