from app.model_creation import create_model

model = create_model('/home/robert/Repositories/ml-starter/external-folder/iris.onnx', "/home/robert/Repositories/ml-starter/external-folder/iris.py")
prediction = model.predict([[5, 2.9, 1, 0.2], [5, 2.9, 1, 0.2]])
print(prediction)
