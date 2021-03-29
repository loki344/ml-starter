from custom_model import CustomModel

#TODO define type of outputnames
def create_model(onnx_file_path: str, onnx_output_names=[]):

    return CustomModel(onnx_file_path, onnx_output_names)
