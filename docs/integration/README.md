<h1 align="center">
    Integrate your own model
</h1>

<p align="center">This chapter will guide you through the process to integrate your own model with ML-Starter.</p>
<p align="center">:exclamation: If you plan to use the REST-API with your custom HTML-Frontend please check the <a href="https://github.com/loki344/ml-starter/tree/master/docs/customization"> Customization</a> section :exclamation:</p>


# Overview

- <a href="#step-by-step">Step by step</a>
- <a href="#configuration">Configuration</a>
- <a href="#preprocessing-and-postprocessing">Preprocessing and Postprocessing</a>
- <a href="#persistence">Persistence</a>
- <a href="#deployment">Deployment</a>
- <a href="#limitations">Limitations</a>

# Prerequisites

- Docker installation (https://docs.docker.com/get-docker/)
- ONNX or PMML model
- Pre- and postprocessing written in Python
- Java 1.8+ (Only for PMML models if you want to debug them locally)

# Intro

The picture below shows the data-flow of a request in ML-Starter. The blue methods must be implemented by you. Follow
the step by step guide to provide all necessary information.<br><br>
<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/inversionofcontrol.png">

# Step by Step

<ol>
   <li style="margin-top: 10px">
      Train your model with an ML-Framework which supports the serialization in the ONNX or PMML format. For ONNX
         see https://onnx.ai/supported-tools.html. Alternatively you can browse https://github.com/onnx/models and download
         most of the state-of-the-art ML-models already pretrained.
</li>
<li style="margin-top: 10px">
Download or clone the ml-starter repository
   ```git
   git clone https://github.com/loki344/ml-starter.git
   ```
</li>
<li style="margin-top: 10px">
Save your trained model in the folder "ml-starter / backend / app / custom_model" with the filename <strong>"
   custom_model.onnx" or "custom_model.xml"</strong>
</li>
<li style="margin-top: 10px">
 Define the configuration in the file <strong>configMap.json</strong> in the directory "ml-starter / backend / app / custom_model". The most important configurations are the requestObject, and the inputFields. The input fields define the necessary fields a user has to enter in order to start a prediction. The requestObject defines the structure in which the data is transmitted to the backend.<br>
Here's an example configuration for an application that expects an image and a number:

<details style="margin-top: 10px;">
<summary>Show configMap.json</summary>
 <p>

```json
{
  "applicationName": "My first ML-Prototype",
  "description": "This algorithm predicts your name based on a picture and your age",
  "input": [
    {
      "id": "ageField",
      "label": "Enter your age",
      "type": "number"
    },
    {
      "id": "pictureField",
      "label": "Upload a selfie",
      "type": "image"
    }
  ],
  "requestObject": {
    "inputData": {
      "picture": "pictureField",
      "age": "ageField"
    }
  }
}
```

</p>
</details>
:mag: Find out more about the configuration possibilites, such as an online Mongo-DB <a href="#configuration">in the
configuration section</a>

</li>
<li style="margin-top: 10px">
Implement the pre- and postprocessing in the file <strong>custom_model.py</strong> in the directory "ml-starter /
   backend / app / custom_model". <br>

<details style="margin-top: 15px"><summary>ONNX template</summary>
<p>

```python
from model.onnx_model import ONNXModel


class CustomModel(ONNXModel):


   def pre_process(self, input_data, input_metadata):
   # the input_data has the shape of the configured requestObject
   # transform the data according to the specification of your ONNX model
   # ONNX models expect a dictionary of: {input_name: input_value}
   # To access the first expected input name call: input_metadata[0].name
   
   return pre_processed_data


   def post_process(self, model_output):
   # transform the model_output to a human readable form
   # for most onnx models, the prediction is stored in model_output[0]
   
   return post_processed_data
```

</p>
</details>

<details style="margin-top: 15px"><summary>PMML template</summary>
<p>

```python
from model.pmml_model import PMMLModel


   class CustomModel(PMMLModel):


   def pre_process(self, input_data, model):
   # the input_data has the shape of the configured requestObject
   # transform the data according to the specification of your PMML model
   # access the model variable to gather information about the inputs if needed
   
   return pre_processed_data


   def post_process(model_output):
   # transform the model_output to a human readable form
   # for most PMML models, the prediction is stored in model_output[0]
   
   return model_output[0]

```

</p>
</details>
:mag: See <a href="#preprocessing-and-postprocessing">Pre- and postprocessing</a> for further instructions.

</li>
<li style="margin-top: 10px">
If needed, copy custom methods, files and classes into the directory "ml-starter / backend / app / custom_model" (
   Optional)
</li>
<li style="margin-top: 10px">
Add your dependencies for your implementation in the file "ml-starter / backend / app / custom_model / <strong>
   custom_requirements.txt</strong>" just as you would do in the usual requirements.txt file.<br/> Example for a numpy
   requirement:

```text
#custom_requirements.txt

numpy~=1.19.5
```

</li>
<li style="margin-top: 10px">
To start the Application locally execute the following command in the terminal in the directory ml-starter/

   ```commandline
   docker build -t ml-starter .
   docker run -d -p 80:3000 -p 8800:8800 ml-starter
   ```
   💡 To deploy your application to Heroku see <a href="#deployment">Deployment</a> for instructions.
</li>
<li style="margin-top: 10px">
Access the frontend on <strong>http://localhost</strong>, and the backend on <strong>http://localhost:8800/docs</strong>
</li>
</ol>

# Configuration

The file configMap.json contains the configuration which is mainly used by the frontend. The following list defines all
available configuration keys. The names of the keys cannot be changed.

<h3>applicationName</h3>
<p><strong>optional</strong></p>
<p><strong>Description:</strong> This name is displayed in the header of the web application.</p>
<p><strong>Type: </strong>String</p>
<p><strong>Example: </strong>My demoapplication</p>
<p><strong>Default value: </strong>My ML-starter demo application</p>

<h3>description</h3>
<p><strong>optional</strong></p>
<p><strong>Description:</strong> Short text to introduce your model to the user.</p>
<p><strong>Type: </strong>String</p>
<p><strong>Example: </strong>This model recognizes classes in a given image</p>
<p><strong>Default value: </strong>Please provide the data in the input fields below and start the prediction.</p>

<h3>inputFields</h3>
<p><strong>Description:</strong> Array containing an element for each expected input. The frontend creates one inputfield for the user for each element. An element has 3 attributes id (str), label (str), type (str). The id is used to link input fields to the requestObject. The label is the text which is displayed above the field. The type is one of "number", "str", or "image" and is used to display the field accordingly.</p>
<p><strong>Type: </strong>Array</p>
<p><strong>Example: </strong></p>

```json
    "inputFields": 
    [
        {
            "id": "ageFieldId",
            "type": "number",
            "label": "Please enter your age"
        },
        {
            "id": "firstNameFieldId",
            "type": "str",
            "label": "Please enter your first name"
        }
    ]
```

<h3>requestObject</h3>
<p><strong>Description:</strong> Object defining the shape of the expected input data of the backend. Use the id's of the input fields as placeholder for the input values.</p>
<p><strong>Type: </strong>Object</p>
<p><strong>Example: </strong></p>

```json
    "inputData": { "firstName": "firstNameFieldId", "age": "ageFieldId" }
```
💡 Note: The input type "image" is internally handled as a base64 encoded string representing the image content.

---
Please check the <a href="/backend/examples">examples</a> for some sample configurations.

---


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

ML-Starter provides an SPI to let you handle the datastructure from and to the model. In order to implement your custom
preprocessing and postprocessing you have to extend the class ONNXModel or PMMLModel according to your underlying model in the file "custom_model.py" and place it
in the folder "ml-starter / backend / app / custom_model".

If you use an ONNX model, I recommend you to search your model in the <a href="https://github.com/onnx/models">ONNX Model Zoo</a> and look at the implementation example of your model. In most cases, you can just copy the pre- and postprocessing code into the ML-Starter implementation.

For ONNX:

```python
from model.onnx_model import ONNXModel


class CustomModel(ONNXModel):


   def pre_process(self, input_data, input_metadata):
   # the input_data has the shape of the configured requestObject
   # transform the data according to the specification of your ONNX model
   # ONNX models expect a dictionary of: {input_name: input_value}
   # To access the first expected input name call: input_metadata[0].name
   
   return pre_processed_data


   def post_process(self, model_output):
   # transform the model_output to a human readable form
   # for most onnx models, the prediction is stored in model_output[0]
   
   return post_processed_data

```

For PMML:

```python
from model.pmml_model import PMMLModel


   class CustomModel(PMMLModel):


   def pre_process(self, input_data, model):
   # the input_data has the shape of the configured requestObject
   # transform the data according to the specification of your PMML model
   # access the model variable to gather information about the inputs if needed
   
   return pre_processed_data


   def post_process(model_output):
   # transform the model_output to a human readable form
   # for most PMML models, the prediction is stored in model_output[0]
   
   return model_output[0]


```

This is an overview of the dataflow of a user request: <br/>
Input data ⟶ Request object ⟶ pre_process() ⟶ model.predict() ⟶ post_process() ⟶ Response

💡 The inference with ONNX models is achieved with the ONNX InferenceSession. <a href="https://www.onnxruntime.ai/python/modules/onnxruntime/capi/onnxruntime_inference_collection.html#InferenceSession">Learn more about it. </a>
💡 The inference with PMML models is achieved with pypmml. <a href="https://pypi.org/project/pypmml/">Learn more about it. </a>


<strong>Pro tip:</strong><br/>
If you don't know the implementation of your pre- and post processing start a debug session as follows:
<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/debugging.png">

Create a breakpoint in the custom_model.py and make a HTTP POST request with your favorite tool
on: http://localhost:8800/api/predictions
<br>
Make sure to format the requestBody as the configured requestObject.
<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/examplepostiris.png">

This allows you to learn more about the necessary transformations.
<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/debugdetail.png">

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
The post_process method receives the output of the model.predict(pre_processed_data) call. If necessary, transform it. For most models, you can access the output with model_output[0].

The return value of the post_process method is used as a response for the REST interface without further processing.
Therefore, numerical values should be rounded accordingly and any field names should be capitalized.

Example:
If you return an object like this {"Classname": "{PredictedClass}", "Probability": "{Probability}"}, it will be displayed like
this:
<img style="width=10rem" src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/objectPrediction.png">

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
docker build -t ml-starter .

docker tag ml-starter registry.heroku.com/{yourApplicationName}/web
docker push registry.heroku.com/{yourApplicationName}/web
heroku container:release web --app {yourApplicationName}
heroku open --app {yourApplicationName}
```

# Limitations

- Heroku has a maximum RAM use of 512Mb - large models won't start in the free version due to memory shortage
- Nested objects as RequestObject are not supported. This does not work: 
    ```json
    {"firstName": "inputFieldId", "address": {"street":"streetInputFieldId"} }
    ```
