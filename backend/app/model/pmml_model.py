from abc import abstractmethod

from pypmml import Model

from model.abstract_model import AbstractModel


# TODO doc
class PMMLModel(AbstractModel):

    def __init__(self, pmml_file_path: str):
        """
        Initializes an AbstractModel with the path to the model and the model_output_names

        :param onnx_file_path: path where to .onnx file is available
        :type onnx_file_path: str
        """

        self.pmml_file_path = pmml_file_path
        self.model = Model.load(pmml_file_path)

        print("Model has " + str(len(self.model.inputFields)) + " inputs defined.")
        for input in self.model.inputFields:
            print("Inputname: " + str(input.name) + ", displayName: " + str(input.displayName) + ", type: " + str(
                input.dataType))

        print("Model has " + str(len(self.model.outputFields)) + " outputs defined.")
        for output in self.model.outputFields:
            print("Outputname: " + str(output.name) + ", displayName: " + str(output.displayName) + ", feature: " + str(
                output.feature) + ", type: " + str(output.dataType))

        print("Model has " + str(len(self.model.outputNames)) + " outputNames defined.")
        for outputName in self.model.outputNames:
            print("Outputname: " + str(outputName))

    @abstractmethod
    def pre_process(self, input_data, model) -> dict:

        return input_data

    @staticmethod
    @abstractmethod
    def post_process(model_output: object) -> object:
        return model_output

    def predict(self, input_data: object) -> object:
        pre_processed_data = self.pre_process(input_data, self.model)
        return self.post_process(self.model.predict(pre_processed_data))
