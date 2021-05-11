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
        """
        Pre processes the input of the REST-API. The input_data has the shape of the defined config 'requestObject'.
        The return value of this object is used to run the prediction with the PMML Model.
        Therefore the return value MUST correspond to the expected inputValue of your PMML model.
        To access the expected inputValues of the model, you can access the model.
        example: model.inputFields

        :param input_data: inputs from the REST-API in the shape of the defined requestObject

        :param model: the pypmml Model class representing your model

        :return value which is passed to run the prediction with the model
        """
        return input_data

    @staticmethod
    @abstractmethod
    def post_process(model_output: object) -> object:
        """
        Post processes the output of the method model.predict(). The return value of this method is used to
        display the prediction in the frontend. Consider using capitalized fieldNames and rounded numbers.
        The shape of the output is dependent of your model in use.

        :param model_output: Prediction output of InferenceSession.run() method.
        :type model_output: object

        :return: object representing the formatted prediction for the REST-API
        """
        return model_output

    def predict(self, input_data: object) -> object:
        """
        This method is used by the FastAPI to provide the prediction. It is responsible for the dataflow
        between the pre_process -> Model.predict() -> post_process().

        :param input_data: inputData in the shape of the configured requestObject.
        :type input_data: object

        :return: object representing the formatted prediction for the REST-API
        """
        pre_processed_data = self.pre_process(input_data, self.model)
        return self.post_process(self.model.predict(pre_processed_data))
