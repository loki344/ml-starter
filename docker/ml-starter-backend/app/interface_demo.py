from model_creation import create_model

model = create_model('../external-folder/efficientnet-example/custom_model.py.onnx', ["Softmax:0"])

with open('/external-folder/efficientnet-example/kitten.txt', 'r') as file:
    image = file.read()

model.predict(image)

