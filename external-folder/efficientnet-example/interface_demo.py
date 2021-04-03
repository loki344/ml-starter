from model_creation import create_model
import json

config = json.load(open('../../app/custom_model/configMap.json'))
model_output_names = []
if 'model_output_names' in config:
    model_output_names = config['model_output_names']

model = create_model('custom_model.py.onnx', model_output_names)
with open('kitten.txt', 'r') as file:
    image = file.read()

model.predict(image)

