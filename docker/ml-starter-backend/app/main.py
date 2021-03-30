from fastapi import FastAPI, Request
import json

from model_creation import create_model

app = FastAPI()

#TODO, take whole path from env var
#model = create_model('../mounted_directory/' + os.getenv('MODEL_FILE_NAME'))

#TODO ERROR HANDLING WHEN FILE IS NOT THERE
config = json.load(open('../external-folder/iris-example/configMap.json'))
model_output_names = []
if 'model_output_names' in config:
    model_output_names = config['model_output_names']

#model = create_model('/external-folder/iris-example/custom_model.onnx', model_output_names)
model = create_model('./efficientnet-lite4-11.onnx', model_output_names)


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




