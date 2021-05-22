import numpy as np
import cv2
import json
import base64

from file_helper import get_file
from model.onnx_model import ONNXModel


class CustomModel(ONNXModel):

    labels = json.load(open(get_file("labels_map.txt"), "r"))

    @staticmethod
    def center_crop(img, out_height, out_width):
        height, width, _ = img.shape
        left = int((width - out_width) / 2)
        right = int((width + out_width) / 2)
        top = int((height - out_height) / 2)
        bottom = int((height + out_height) / 2)
        img = img[top:bottom, left:right]
        return img

    @staticmethod
    def resize_with_aspectratio(img, out_height, out_width, scale=87.5, inter_pol=cv2.INTER_LINEAR):
        height, width, _ = img.shape
        new_height = int(100. * out_height / scale)
        new_width = int(100. * out_width / scale)
        if height > width:
            w = new_width
            h = int(new_height * height / width)
        else:
            h = new_height
            w = int(new_width * width / height)
        img = cv2.resize(img, (w, h), interpolation=inter_pol)
        return img

    def pre_process_edgetpu(self,img, dims):
        output_height, output_width, _ = dims
        img = self.resize_with_aspectratio(img, output_height, output_width, inter_pol=cv2.INTER_LINEAR)
        img = self.center_crop(img, output_height, output_width)
        img = np.asarray(img, dtype='float32')
        img -= [127.0, 127.0, 127.0]
        img /= [128.0, 128.0, 128.0]
        return img

    def pre_process(self, input_data, input_metadata):

        decoded_data = base64.b64decode(input_data)
        np_data = np.fromstring(decoded_data, np.uint8)
        img = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = self.pre_process_edgetpu(img, (224, 224, 3))

        return {input_metadata[0].name: np.expand_dims(img, axis=0)}

    def post_process(self, model_output):
        model_output = model_output[0]
        result = reversed(model_output[0].argsort()[-5:])

        response = []
        for r in result:
            classnames = self.labels[str(r)].split(',')
            probability = model_output[0][r] * 100
            probability = round(probability, 2)
            if probability > 1:
                response.append({
                    'Classname': classnames[len(classnames)-1].capitalize(),
                    'Probability': str(probability) + '%'
                })
            print({
                        'Classname': classnames[len(classnames)-1].capitalize(),
                        'Probability': str(probability) + '%'
                    })
        return response
