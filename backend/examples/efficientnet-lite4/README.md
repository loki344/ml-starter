# Example with the EfficientNet-Lite4

The ONNX model included in this example is the pretrained version available on https://github.com/onnx/models/tree/master/vision/classification/efficientnet-lite4.

## Instructions

### Local deployment

```commandline
git clone https://github.com/loki344/ml-starter.git
find ./backend/app/custom_model -type f ! -name '__init__.py' -delete
cp -a ./backend/examples/efficientnet-lite4/. ./backend/app/custom_model
docker build -t ml-starter-efficientnet-example .
docker run -d -p 80:3000 -p 8800:8800 ml-starter-efficientnet-example
```
Access your browser on localhost (frontend) or localhost:8800/docs (backend)

### Deployment to Heroku

In order to deploy your application to heroku you'll need a heroku account and the CLI from heroku.

https://devcenter.heroku.com/articles/heroku-cli#download-and-install

```commandline
heroku create
#COPY the your application name and replace it in the commands below
```

```commandline
git clone https://github.com/loki344/ml-starter.git
find ./backend/app/custom_model -type f ! -name '__init__.py' -delete
cp -a ./backend/examples/efficientnet-lite4/. ./backend/app/custom_model
docker build -t ml-starter-efficientnet-example .

docker tag ml-starter-efficientnet-example registry.heroku.com/{yourApplicationName}/web
docker push registry.heroku.com/{yourApplicationName}/web
heroku container:release web --app {yourApplicationName}
heroku open --app  {yourApplicationName}
```

## Result

<img style="width: 100%" src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/efficientnet/efficientnet-1.png"/>
<br/>
<img style="width: 100%" src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/efficientnet/efficientnet-2.png"/>


## Model input

An image file to be classified. The frontend expects the user to upload an image. Internally the REST-API expects a string representing the base64 encoded content of the image. <br/>
Example: <br/>
<img style="width: 25rem" src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/efficientnet/Matterhorn.jpg"/>

## Configuration

The applicationName and the description are interchangeable, whereas the configuration of the input and the requestObject should match the above definition of the input data.
```json
{
  "applicationName": "My demo-application with EfficientNet",
  "description": "This application uses the EfficientNet model to predict classes in a given image. Try it and upload your image below!",

  "input": [
    {
    "id": "imageInput",
    "label": "Please upload an image file",
    "type": "image"
    }
  ],
  "requestObject": {"inputData": "imageInput"}

}
```


### Preprocessing

The preprocess method has to decode the image data from the input string. Afterwards the same processing as used in the training of the model should be applied. Lastly, the data is wrapped in a dictionary using the expected input keys from the input metadata.

```python
def pre_process(self, input_data, input_metadata):

    decoded_data = base64.b64decode(input_data)
    np_data = np.fromstring(decoded_data, np.uint8)
    img = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = self.pre_process_edgetpu(img, (224, 224, 3))

    return {input_metadata[0].name: np.expand_dims(img, axis=0)}
```

## Model output

Output of model is an inference score with array shape float32[1,1000]. The output references the labels_map.txt file which maps an index to a label to classify the type of image.

Example:
```text
[[2.13733227e-08 6.26663876e-08 5.44992176e-08 1.99169605e-08
  2.24667804e-08 3.61451136e-08 4.48802862e-09 4.56697258e-09 ...]]

```

### Postprocessing

The postprocessing builds a response containing the classname, and the probability for classes with a probability greater than 1%. The response is used in the frontend. Therefore, the classnames must be capitalized.

```python
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

    return response
```

## Helper methods

```python


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


```

