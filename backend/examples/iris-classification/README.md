# Example with the Iris classification model

The ONNX model included in this example is a simple decision tree built with Scikitlearn.

## Instructions
To run this example locally
```commandline
git clone https://github.com/loki344/ml-starter.git
find ./backend/app/custom_model -type f ! -name '__init__.py' -delete
cp -a ./backend/examples/iris-classification/. ./backend/app/custom_model
docker run #WIP
```

To deploy it on www.heroku.com
```commandline
#TBD
```

## Result
<img style="width: 100%" src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/iris/result_iris.png"/>
<img style="width: 100%" src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/iris/result_iris.png"/>





##Model input
An array containing two arrays which represent the measurements of a flower. <br/>
```json
[ [ Measurements flower 1 ], [ Measurements flower 2 ] ]
```
One measurement contains 4 floats in the following order: 
```json
'sepal_length', 'sepal_width', 'petal_length', 'petal_width'
```
Example: 
```json
[ [ 3.4, 2.1, 4.0, 2.8 ], [ 1.5, 2.0, 0.98, 1.45 ] ]
```

###Preprocessing
The preprocessing method transforms the array to a numpy array and wraps the input data in a dictionary with the expected input name from the metadata object.

```python
def pre_process(self, input_data, input_metadata):
    input_data = np.array(input_data).astype(np.float32)
    return {input_metadata[0].name: input_data}
```

##Model output
The raw output of the model is a list containing two numbers which represent the two predictions for the input.

Example:
```json
[1 0]
```

###Postprocessing
The postprocessing maps the class number of the prediction to the according label.

```python
def post_process(self, model_output):

    labels = ['Setosa', 'Versicolor', 'Virginica']
    predicted_labels = list(map(lambda prediction: labels[prediction], model_output[0]))
    return predicted_labels
```
