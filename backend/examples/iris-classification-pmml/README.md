# Example with the Iris classification model

The PMML model included in this example is a simple decision tree
from <a href="http://dmg.org/pmml/pmml_examples/index.html">http://dmg.org/pmml/pmml_examples/index.html </a>

### Local deployment

To run this example locally

```commandline
git clone https://github.com/loki344/ml-starter.git
find ./backend/app/custom_model -type f ! -name '__init__.py' -delete
cp -a ./backend/examples/iris-classification-pmml/. ./backend/app/custom_model
docker build -t ml-starter-iris-pmml-example .
docker run -d -p 80:3000 -p 8800:8800 ml-starter-iris-pmml-example
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
cp -a ./backend/examples/iris-classification-pmml/. ./backend/app/custom_model
docker build -t ml-starter-iris-pmml-example .

docker tag ml-starter-iris-pmml-example registry.heroku.com/{yourApplicationName}/web
docker push registry.heroku.com/{yourApplicationName}/web
heroku container:release web --app {yourApplicationName}
heroku open {yourApplicationName}
```

## Result

<img style="width: 100%" src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/iris/result_iris.png"/>
<img style="width: 100%" src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/iris/result_iris2.png"/>

## Model input

An array containing an array which represent the measurements of a flower. <br/>

```json
[
  Measurements
  flower
  1
]
```

One measurement contains 4 floats in the following order:

```json
'sepal_length', 'sepal_width', 'petal_length', 'petal_width'
```

Example:

```json
[
  3.4,
  2.1,
  4.0,
  2.8
]
```

### Configuration

The applicationName and the description are interchangeable, whereas the configuration of the input and the
requestObject should match the above definition of the input data.

```json
{
  "applicationName": "My demo-application with the basic Iris-Model",
  "description": "This is a basic regression model trained with the famous iris-data set. Please provide the measurement of a flower and start the prediction!",
  "input": [
    {
      "id": "input1",
      "label": "Flower 1, Sepal length",
      "type": "number"
    },
    {
      "id": "input2",
      "label": "Flower 1, Sepal width",
      "type": "number"
    },
    {
      "id": "input3",
      "label": "Flower 1, Petal length",
      "type": "number"
    },
    {
      "id": "input4",
      "label": "Flower 1, Petal width",
      "type": "number"
    }
  ],
  "requestObject": {
    "inputData": [
      "input1",
      "input2",
      "input3",
      "input4"
    ]
  }
}

```

### Preprocessing

The preprocessing method is straight forward and does need any transformation of the input data.

```python
def pre_process(self, input_data, model) -> dict:
    return input_data

```

## Model output

The raw output of the model is a list containing two numbers which represent the two predictions for the input.

Example:

```json
[
  1
  0
]
```

### Postprocessing

The postprocessing returns the classname of the predicted value. It is always the first value in the list. In case you're not sure which value you should return, start a debug session for the main.py, create a breakpoint in the post_processing of your custom_model.py and send a request to the http://localhost:8800/api/predictions endpoint with a well formed request body ( {
    "inputData":[5, 2.9, 1, 0.2]
} )

<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/irispmmlpostprocessing.png">


```python
@staticmethod
def post_process(model_output: object) -> object:
    return model_output[0]
```
