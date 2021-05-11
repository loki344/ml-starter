import numpy as np
import torch
from transformers import GPT2Tokenizer

from model.onnx_model import ONNXModel


class CustomModel(ONNXModel):

    def pre_process(self, input_data, input_metadata):

        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        inputs = torch.tensor(
            [[tokenizer.encode(input_data, add_special_tokens=True)]])
        inputs_flatten = flatten(inputs)
        inputs_flatten = update_flatten_list(inputs_flatten, [])

        ort_inputs = dict((input_metadata[i].name, to_numpy(input)) for i, input in enumerate(inputs_flatten))

        return ort_inputs

    def post_process(self, model_output):
        outputs_flatten = model_output[0].flatten()
        outputs_flatten = outputs_flatten.flatten()

        predictions = torch.tensor(outputs_flatten)
        return str(predictions)



def flatten(inputs):
    return [[flatten(i) for i in inputs] if isinstance(inputs, (list, tuple)) else inputs]


def update_flatten_list(inputs, res_list):
    for i in inputs:
        res_list.append(i) if not isinstance(i, (list, tuple)) else update_flatten_list(i, res_list)
    return res_list


def to_numpy(x):
    if type(x) is not np.ndarray:
        x = x.detach().cpu().numpy() if x.requires_grad else x.cpu().numpy()
    return x


