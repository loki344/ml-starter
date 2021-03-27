from abc import ABC, abstractmethod
import onnxruntime as runtime


class AbstractModel(ABC):

    def __init__(self) -> "AbstractModel":
        pass

    @staticmethod
    @abstractmethod
    def pre_process(input_data):
        pass

    @staticmethod
    @abstractmethod
    def post_process(model_output):
        print(model_output)
        pass

    def run(self, input_data, model_path):
        session = runtime.InferenceSession(model_path)
        input_name = session.get_inputs()[0].name

        input_data = self.pre_process(input_data)
        #TODO make first parameter configurable, and adapt second parameter to GPT-Problem
        output = session.run([], {input_name: input_data})

        return self.post_process(output)


