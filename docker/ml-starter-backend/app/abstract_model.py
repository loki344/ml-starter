from abc import ABC, abstractmethod
import onnxruntime as runtime


class AbstractModel(ABC):

    def __init__(self, onnx_file_path: str) -> "AbstractModel":
        self.onnx_file_path = onnx_file_path

    @staticmethod
    @abstractmethod
    def pre_process(input_data):
        pass

    @staticmethod
    @abstractmethod
    def post_process(model_output):
        print('post_process, model_output: ' + model_output)
        pass

    def predict(self, input_data):
        inference_session = runtime.InferenceSession(self.onnx_file_path)

        input_name = inference_session.get_inputs()[0].name
        input_data = self.pre_process(input_data)

        #TODO make first parameter configurable, and adapt second parameter to GPT-Problem
        output = inference_session.run([], {input_name: input_data})

        return self.post_process(output)
