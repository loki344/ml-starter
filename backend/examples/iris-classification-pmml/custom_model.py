
from model.pmml_model import PMMLModel


class CustomModel(PMMLModel):

    def pre_process(self, input_data, model) -> dict:
        return input_data

    @staticmethod
    def post_process(model_output: object) -> object:
        return model_output[0]
