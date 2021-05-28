import numpy as np
import torch
from transformers import RobertaTokenizer
from model.onnx_model import ONNXModel


class CustomModel(ONNXModel):

    @staticmethod
    def to_numpy(tensor):
        return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

    def pre_process(self, input_data, input_metadata):

        tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
        input_ids = torch.tensor(tokenizer.encode(input_data, add_special_tokens=True)).unsqueeze(0)
        ort_inputs = {input_metadata[0].name: self.to_numpy(input_ids)}

        return ort_inputs

    def post_process(self, model_output):

        pred = np.argmax(model_output)
        if (pred == 0):
            prediction = "The sentiment of this text is negative"
        elif (pred == 1):
            prediction = "The sentiment of this text is positive"

        return prediction
