import numpy as np
from abstract_model import AbstractModel


# TODO CONVENTION: FILE NAME AND STRUCTURE: HAS TO BE IN FOLDER CUSTOM_FILES, what about imports?
class CustomModel(AbstractModel):

    def pre_process(self, input_data):
        input_data = np.array(input_data).astype(np.float32)
        return input_data

    def post_process(self, model_output):

        labels=['Setosa', 'Versicolor', 'Virginica']
        predicted_labels = list(map(lambda prediction: labels[prediction], model_output[0]))
        return predicted_labels
