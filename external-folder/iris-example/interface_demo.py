from model_creation import create_model

model = create_model('custom_model.py.onnx')
prediction = model.predict([[5, 2.9, 1, 0.2], [5, 2.9, 1, 0.2]])
print(prediction)
