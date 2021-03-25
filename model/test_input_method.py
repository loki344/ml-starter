import numpy as np


def pre_process(self, input_data):
    input_data = np.array(input_data).astype(np.float32)
    return input_data


def post_process(self, model_output):
    return model_output[0]
