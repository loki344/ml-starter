from abc import ABC, abstractmethod


#TODO update doc
class AbstractModel(ABC):
    """Abstract class to define the functionality which is needed to integrate the model with the FastAPI"""

    @abstractmethod
    def pre_process(self, input_data, input_metadata) -> dict:
        """
        Pre processes the input of the REST-API. The input_data has the shape of the defined config 'requestObject'.
        The return value of this object is used to run the prediction in the onnx InferenceSession.
        Therefore the return value MUST correspond to the expected inputValue of your onnx model.
        Usually it is a dictionary of {'inputKeys': 'inputValue'}
        To access the expected inputNames of the onnx model, you can access the input_metadata.
        example: input_metadata[0].name

        :param input_data: inputs from the REST-API in the shape of the defined requestObject

        :param input_metadata: the input metadata provided by the InferenceSession.get_inputs() method

        :return dict representing the prepared data for the onnx InferenceSession
        """

        pass

    @staticmethod
    @abstractmethod
    def post_process(model_output: object) -> object:
        """
        Post processes the output of the method InferenceSession.run(). The return value of this method is used to
        display the prediction in the frontend. Consider using capitalized fieldNames and rounded numbers.
        The shape of the output is dependent of your model in use.

        :param model_output: Prediction output of InferenceSession.run() method.
        :type model_output: object

        :return: object representing the formatted prediction for the REST-API
        """

        pass

    @abstractmethod
    def predict(self, input_data: object) -> object:
        """
        This method is used by the FastAPI to provide the prediction. It is responsible for the dataflow
        between the pre_process -> InferenceSession.run() -> post_process().

        :param input_data: inputData in the shape of the configured requestObject.
        :type input_data: object

        :return: object representing the formatted prediction for the REST-API
        """
        pass
