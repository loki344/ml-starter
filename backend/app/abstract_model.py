from abc import ABC, abstractmethod
import onnxruntime as runtime


class AbstractModel(ABC):
    #TODO what is the type of outputnames
    def __init__(self, onnx_file_path: str, model_output_names=None):
        if model_output_names is None:
            model_output_names = []

        self.onnx_file_path = onnx_file_path
        self.model_output_names = model_output_names
        self.inference_session = runtime.InferenceSession(self.onnx_file_path)

        print("Model has " + str(len(self.inference_session.get_inputs())) + " inputs defined.")
        for input in self.inference_session.get_inputs():
            print("Inputname: " + str(input.name) + ", shape: " + str(input.shape) + ", type: " + str(input.type))

        print("Model has " + str(len(self.inference_session.get_outputs())) + " outputs defined.")
        for output in self.inference_session.get_outputs():
            print("Outputname: " + str(output.name) + ", shape: " + str(output.shape) + ", type: " + str(output.type))

    @abstractmethod
    def pre_process(self, input_data, input_metadata):
        pass

    @staticmethod
    @abstractmethod
    def post_process(model_output):
        pass

    def predict(self, input_data):

        input_data = self.pre_process(input_data, self.inference_session.get_inputs())

        output = self.inference_session.run(self.model_output_names, input_data)

        return self.post_process(output)
