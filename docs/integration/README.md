<h1 align="center">
    Integrate your own model
</h1>

This tutorial will guide you through the process of integration your own model with ML-Starter.

##Overview

- <a href="#configuration">Configuration</a>
- <a href="#preprocesing-and-postprocessing">Preprocessing and Postprocessing</a>
- <a href="#persistence">Persistence</a>
- <a href="#deployment">Deployment</a>
- <a href="#limitations">Limitations</a>

## Prerequisites

- Docker installation (https://docs.docker.com/get-docker/)
- ONNX or PMML model
- Pre- and postprocessing written in Python (Optional for PMML)
- Java 1.8+ (Only for PMML models if you want to debug them locally)

# Configuration

The file configMap.json contains the configuration which is mainly used by the frontend. The following list defines all
available configuration keys. The names of the keys cannot be changed.

| **Key** | **Description** | **Type** | **Example** | **Default** |
|---|---|---|---|---|
| applicationName (optional) | This name is displayed in the header of the web application. | String | My demoapplication | My ML-starter demo application |
| description (optional) | Short text to introduce your model to the user. This text is displayed above the input fields. | String | This model recognizes classes in a given image | Please provide the data in the input fields below and start the prediction. |
| input | Array containing an element for each expected input. The frontend creates one inputfield for the user for each element. An element has 3 attributes id (str), label (str), type (str). The id is used to link input fields to the requestObject. The label is the text which is displayed above the field. The type is one of "number", "str", or "image" and is used to display the field accordingly. | Array[Object] | [  {   "id": "textInput",    "label": "Enter text for prediction",     "type": "str"  } ] | - |
| requestObject | Object defining the shape of the expected input data of the backend. Use the id's of the input fields as placeholder for the input values. | Object | { "inputData": "inputText" } <br/><br/>  { "inputData": { "firstName": "firstNameId", "lastName": "lastNameId" } }  | - |

Please check the <a href="/backend/examples">examples</a> for some sample configurations. <br/><br/>
💡 Note: The input type "image" is internally represented by a base64 encoded string representing the image content.
Learn more about it in the <a href="#preprocessing">Preprocessing</a> section.

## Optional database configuration

In case you have set up a free MongoDB instance in the section <a href="#persistence">Persistence</a> there are some
additional configurations available:

### dbName

You can find the name of your database on www.cloud.mongodb.com in the upper left corner.
<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/dbName.png">

### clusterName

You can find the name of your cluster on www.cloud.mongodb.com in the section "Clusters".
<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/clusterName.png">

### dbUser

Username for the configured database. Make sure the user has sufficient reading and writing rights for the database. You
can find the username on www.cloud.mongodb.com in the section "Database Access".
<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/dbUser.png">

### dbCredentials

The credentials for the configured user. You can find them on www.cloud.mongodb.com in the section "Database Access" 🡒
Edit

# Preprocessing and postprocessing

ML-Starter provides an SPI to let you control the dataflow from and to the model. In order to implement your custom
preprocessing and postprocessing you have to extend the class AbstractModel in the file "custom_model.py" and place it
in the folder "ml-starter / backend / app / custom_model".

For ONNX:

```python
from model.onnx_model import ONNXModel


class CustomModel(ONNXModel):

    def pre_process(self, input_data, input_metadata):
        # Your implementation

        return prepared_input_data

    def post_process(self, model_output):
        # Your implementation

        return prettified_model_output

```

For PMML:

```python
from model.pmml_model import PMMLModel


class CustomModel(PMMLModel):

    def pre_process(self, input_data, model):
        # Your implementation

        return prepared_input_data

    def post_process(self, model_output):
        # Your implementation

        return prettified_model_output

```

This is an overview of the dataflow of a user request: <br/>
Input data ⟶ Request object ⟶ pre_process() ⟶ model.predict() ⟶ post_process() ⟶ Response

💡 <a href="https://www.onnxruntime.ai/python/modules/onnxruntime/capi/onnxruntime_inference_collection.html#InferenceSession">
Learn more about the ONNX InferenceSession</a>

<strong>Pro tip:</strong><br/>
If you don't know the implementation of your pre- and post processing start a debug session as follows:
<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/debugging.png">

Create a breakpoint in the custom_model.py and make a HTTP POST request with your favorite tool
on: http://localhost:8800/api/predictions
<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/debuggingdetail.png">

## Preprocessing

The input data is passed to the method pre_process as parameter input_data in the form of the configured requestObject.
If needed convert it to the format your model expects.
<br/>
<strong>For ONNX:</strong> The metadata about the expected input provided by the onnx session is passed to the
pre_process method as the input_metadata parameter. They correspond to the call to onnxruntime.InferenceSession(
{model-path}).get_inputs(). The return value of the pre_process method is passed directly to the onnx InferenceSession
and therefore must be a dictionary in the format {"input_name": input_data}.

<strong>For PMML:</strong> The second parameter is the loaded model in case you need information about the expected
inputs or outputs.

Images are passed as base64 encoded strings. In order to process them convert the string to an image:

```python
def pre_process(self, input_data, input_metadata):
    decoded_data = base64.b64decode(input_data)
    np_data = np.fromstring(decoded_data, np.uint8)
    img = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
```

## Postprocessing

<strong>For ONNX: </strong>
The post_process method receives the model_output as parameter, which corresponds to the direct output of the call to
onnxruntime.InferenceSession({onnx-model-path}).run({model_output_names}, {pre_processed_input_data}). For most models,
you can access the output with model_output[0] and transform it accordingly.

<strong>For PMML: </strong>
The post_process method receives the output of the model.predict(pre_processed_data) call. If necessary, transform it.

The return value of the post_process method is used as a response for the REST interface without further processing.
Therefore, numerical values should be rounded accordingly and any field names should be capitalized.

Example:
If you return an object like this {"Classname": "Predicted Class", "Probability": "23%"}, it will be displayed like
this:
<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/objectPrediction.png">

## Custom methods, files and requirements

During pre- and postprocessing you can access other methods, classes or files (labels etc.) of your own. Just copy them
into the folder "ml-starter / backend / app / custom_model". If your implementation needs any external libraries, you
must add them in the file "custom_requirements.txt" in the folder "ml-starter / backend / app / custom_model".

## Access files

In order to access files during the processing you must 1) provide them according to the above instructions (Custom
methods, files and requirements) and 2) access them via the helper method get_file() from the file_helper.py. This
ensures a safe access even in a containerized environment.

```python
from model.onnx_model import ONNXModel
from file_helper import get_file


class CustomModel(ONNXModel):
    labels = json.load(open(get_file("labels_map.txt"), "r"))

    # rest of the code omitted..
```

# Persistence

Without further configuration, the user requests as well as the corresponding response of their model are persisted in a
SQLite in-memory database. For operation on Heroku, it cannot be ensured that the data is persisted for a longer period
of time. For persistent data storage, we recommend creating a no-SQL database at www.cloud.mongodb.com. You can specify
the access data to the database afterwards in the <a href="#configuration">Configuration</a>.

💡 Setting up a MongoDB allows you to gain insights from the user rating of the prediction and use the userdata to
improve your model performance.

# Deployment

The integration with docker allows you to run your ML-Starter easily on your local machine or deploy it to a hosting
provider. Please make sure, that the running environment provides enough resources (RAM / CPU) to run your model.

## Local deployment

Open a terminal in the directory "ml-starter /"

```commandline
docker build -t ml-starter .
docker run -d -p 80:3000 -p 8800:8800 ml-starter
```

Or if you want to start your services seperately (Make sure you have installed all requirements):

```commandline
#ml-starter/backend/app
uvicorn main:app --host locahost --port 8800 --reload

#ml-starter/frontend
npm start
```

Access your browser on localhost (frontend) or localhost:8800/docs (backend)

## Deploy to Heroku

In order to deploy your application to heroku you'll need a heroku account and the CLI from heroku.

https://devcenter.heroku.com/articles/heroku-cli#download-and-install

```commandline
heroku create
#COPY the your application name and replace it in the commands below
```

```commandline
docker build -t ml-starter-efficientnet-example .

docker tag ml-starter registry.heroku.com/{yourApplicationName}/web
docker push registry.heroku.com/{yourApplicationName}/web
heroku container:release web --app {yourApplicationName}
heroku open --app  {yourApplicationName}
```


# Limitations

- Heroku has a maximum RAM use of 512Mb - large models won't start
- Nested objects as RequestObject are not supported. This does not work: {"firstName": "inputFieldId", "address": {"
  street":"streetInputFieldId"}}


