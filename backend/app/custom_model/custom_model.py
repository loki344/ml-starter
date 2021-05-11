from typing import List

from onnxruntime import NodeArg

from model.onnx_model import ONNXModel
from model.pmml_model import PMMLModel

#IMPLEMENT THIS IF YOU HAVE AN ONNX MODEL
class CustomModel(ONNXModel):

    def pre_process(self, input_data: object, input_metadata: List[NodeArg]) -> dict:
        #see doc in class ONNXModel
        pass

    @staticmethod
    def post_process(model_output: object) -> object:
        #see doc in class ONNXModel
        pass

#IMPLEMENT THIS IF YOU HAVE A PMML MODEL
class CustomModel(PMMLModel):

    def pre_process(self, input_data, model) -> dict:
        #see doc in class PMMLModel

        pass

    @staticmethod
    def post_process(model_output: object) -> object:
        #see doc in class PMMLModel
        pass
