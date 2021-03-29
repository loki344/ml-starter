from custom_model import CustomModel


def create_model(onnx_file_path: str):

    return CustomModel(onnx_file_path)
