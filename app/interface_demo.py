from model_creation import create_model_class
import os

model = create_model_class("/home/robert/Repositories/ml-starter/external-folder/test_input_method.py")
prediction = model.run([[5, 2.9, 1, 0.2], [5, 2.9, 1, 0.2]], '/home/robert/Repositories/ml-starter/external-folder/iris.onnx')
print(prediction)
