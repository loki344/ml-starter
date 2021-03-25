from model_creation import create_model_class


## now dynamic
dynamic_model = create_model_class("./test_input_method.py")
output = dynamic_model.run([[5, 2.9, 1, 0.2], [5, 2.9, 1, 0.2]], "./iris.onnx")
print(output)
