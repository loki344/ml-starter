import numpy as np

from model.onnx_model import ONNXModel


class CustomModel(ONNXModel):

    def pre_process(self, input_data, input_metadata):
        input_data = np.array(input_data).astype(np.float32)
        return {input_metadata[0].name: input_data}

    def post_process(self, model_output):
        labels = ['Setosa', 'Versicolor', 'Virginica']
        predicted_labels = list(map(lambda prediction: labels[prediction], model_output[0]))
        return predicted_labels
