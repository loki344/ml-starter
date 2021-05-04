<h1 align="center">
    ML-Starter
</h1>

<p align="center">
    <strong>Let's build fast prototypes for your ONNX Models</strong>
</p>





<p align="center">
    | <a href="#getting-started">Getting Started</a> | 
   <a href="/backend/examples">Examples</a> |     
   <a href="#preprocessing-and-postprocessing">Pre- and postprocessing</a> | <br/>
   | <a href="#configuration">Configuration</a> | 
   <a href="#persistence">Persistence</a> | 
   <a href="#deployment">Deployment</a> | 
   <a href="#how-does-it-work">How does it work?</a> |
</p>

Tired of building web-applications for your machine learning models to enable users to interact with it? ML-Starter lets you focus on your model performance rather than writing backend- and frontend-code. ML-Starter is built on FastAPI and React. Its integration with Docker allows you to run your application locally or deploy it to a hosting provider such as https://www.heroku.com. User requests and predictions can be saved in a free online MongoDB such as https://www.mongodb.com

<sup>Alpha version: Only suggested for experimental usage.</sup>


<img style="width: 100%" src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/combined_efficientnet.png"/>

---

<p align="center">
     Try out some applications running with ML-Starter <a href="#">here (link tbd)</a>.
</p>

---

# Highlights

- Provides a REST-API for your ONNX model
- Provides a React frontend for your ONNX model
- Saves requests and predictions in an online MongoDB
- Lets your user rate the prediction
- Runs everywhere with Docker
- Minimal configuration and implementation required

# Getting started

## Prerequisites

- Docker installation (https://docs.docker.com/get-docker/)
- ONNX model
- Pre- and postprocessing written in Python

## Instructions

1) Train your model with a ML-Framework which supports the serialization in the ONNX format. See https://onnx.ai/supported-tools.html. Alternatively you can browse https://github.com/onnx/models and download most of the state-of-the-art ML-models already pretrained.
2) Clone the ml-starter repository
3) Save your trained model in the folder "ml-starter / backend / app / custom_model" with the file name <strong>"custom_model.onnx"</strong>
4) Implement the pre- and postprocessing method to specify the data processing of the user requests and the prediction. Use the file "ml-starter / backend / app / custom_model / <strong>custom_model.py</strong>".</br> A simple pre- and postprocessing function for the famous iris-classification model looks like this:
   
    ```python
    #custom_model.py    
   
    import numpy as np
    from abstract_model import AbstractModel


    class CustomModel(AbstractModel):

        def pre_process(self, input_data, input_metadata):
            input_data = np.array(input_data).astype(np.float32)
            return {input_metadata[0].name: input_data}

        def post_process(self, model_output):
    
            labels = ['Setosa', 'Versicolor', 'Virginica']
            predicted_labels = list(map(lambda prediction: labels[prediction], model_output[0]))
            return predicted_labels
    ```
    See <a href="#pre-and-post-processing">Pre- and postprocessing</a> for further instructions.


5) If needed, copy custom methods, files and classes into the directory "ml-starter / backend / app / custom_model" (Optional)
6) Add your dependencies for your implementation in the file "ml-starter / backend / app / custom_model / <strong>custom_requirements.txt</strong>" just as you would do in the usual requirements.txt file.<br/> For the Iris model it looks like this:
   ```text
   #custom_requirements.txt
   
   numpy~=1.19.5
   ```
   
7) Define the configuration in the file "ml-starter / backend / app / custom_model / <strong>configMap.json</strong>". See <a href="#configuration">Configuration</a> for instructions. The most important parts are the inputFields and the requestObject. For the Iris model it looks like this:<br/>
   
   <details><summary>Show configMap.json</summary>
   <p>
   
   ```json
   {
     "applicationName": "My demo-application with the basic Iris-Model",
     "description": "This is a basic regression model trained with the famous iris-data set. Please provide the measurement of two flowers and start the prediction!",
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
       },    {
       "id": "input3",
       "label": "Flower 1, Petal length",
       "type": "number"
       },    {
       "id": "input4",
       "label": "Flower 1, Petal width",
       "type": "number"
       },
       {
       "id": "input5",
       "label": "Flower 2, Sepal length",
       "type": "number"
       },    {
       "id": "input6",
       "label": "Flower 2, Sepal width",
       "type": "number"
       },    {
       "id": "input7",
       "label": "Flower 2, Petal length",
       "type": "number"
       },    {
       "id": "input8",
       "label": "Flower 2, Petal width",
       "type": "number"
       }
     ],
     "requestObject": {"inputData": [["input1", "input2", "input3", "input4"],["input5", "input6", "input7", "input8"]]}
   
   }

   ```
   </p>
   </details>
   <br/>

8) To start the Application locally execute the following command in the terminal in the directory ml-starter/
   ```commandline
   docker build -t ml-starter .
   docker run -d -p 80:3000 -p 8800:8800 ml-starter
   ```
   💡 To deploy your application to a hosting provider see <a href="#deployment">Deployment</a> for instructions.
   

9) Access the frontend on http://localhost, and the backend on http://localhost:8800/docs

---

<p align="center">
     👉&nbsp; Try out and explore some examples <a href="/backend/examples">here</a>  

</p>

---

# Configuration
The file configMap.json contains the configuration which is mainly used by the frontend. The following list defines all available configuration keys. The names of the keys cannot be changed.

| **Key** | **Description** | **Type** | **Example** | **Default** |
|---|---|---|---|---|
| applicationName (optional) | This name is displayed in the header of the web application. | String | My demoapplication | My ML-starter demo application |
| description (optional) | Short text to introduce your model to the user. This text is displayed above the input fields. | String | This model recognizes classes in a given image | Please provide the data in the input fields below and start the prediction. |
| input | Array containing an element for each expected input. The frontend creates one inputfield for the user for each element. An element has 3 attributes id (str), label (str), type (str). The id is used to link input fields to the requestObject. The label is the text which is displayed above the field. The type is one of "number", "str", or "image" and is used to display the field accordingly. | Array[Object] | [  {   "id": "textInput",    "label": "Enter text for prediction",     "type": "str"  } ] | - |
| requestObject | Object defining the shape of the expected input data of the backend. Use the id's of the input fields as placeholder for the input values. | Object | { "inputData": "inputText" } <br/><br/>  { "inputData": { "firstName": "firstNameId", "lastName": "lastNameId" } }  | - |

Please check the <a href="/backend/examples">examples</a> for some sample configurations. <br/><br/>
💡 Note: The input type "image" is internally represented by a base64 encoded string representing the image content. Learn more about it in the <a href="#preprocessing">Preprocessing</a> section.

## Optional database configuration
In case you have set up a free MongoDB instance in the section <a href="#persistence">Persistence</a> there are some additional configurations available:

### dbName
You can find the name of your database on www.cloud.mongodb.com in the upper left corner.
<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/dbName.png">

### clusterName
You can find the name of your cluster on www.cloud.mongodb.com in the section "Clusters".
<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/clusterName.png">

### dbUser
Username for the configured database. Make sure the user has sufficient reading and writing rights for the database. You can find the username on www.cloud.mongodb.com in the section "Database Access".
<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/dbUser.png">

### dbCredentials
The credentials for the configured user. You can find them on www.cloud.mongodb.com in the section "Database Access" 🡒 Edit

# Preprocessing and postprocessing

ML-Starter provides an SPI to let you control the dataflow from and to the model. In order to implement your custom preprocessing and postprocessing you have to extend the class AbstractModel in the file "custom_model.py" and place it in the folder "ml-starter / backend / app / custom_model".

```python
from abstract_model import AbstractModel


class CustomModel(AbstractModel):

    def pre_process(self, input_data, input_metadata):

        #Your implementation

        return None

    def post_process(self, model_output):
        
        #Your implementation

        return None

```

This is an overview of the dataflow of a user request: <br/>
Input data ⟶ Request object ⟶ pre_process() ⟶ inferenceSession.run() ⟶ post_process() ⟶ Response

💡 <a href="https://www.onnxruntime.ai/python/modules/onnxruntime/capi/onnxruntime_inference_collection.html#InferenceSession">Learn more about the ONNX InferenceSession</a>

## Preprocessing

The input data is passed to the method pre_process as parameter input_data in the form of the configured requestObject. The metadata about the expected input provided by the onnx session is passed to the pre_process method as the input_metadata parameter. They correspond to the call to onnxruntime.InferenceSession({model-path}).get_inputs(). The return value of the pre_process method is passed directly to the onnx InferenceSession and therefore must be a dictionary in the format {"input_name": input_data}.

Images are passed as base64 encoded strings. In order to process them convert the string to an image: 
```python
def pre_process(self, input_data, input_metadata):

  decoded_data = base64.b64decode(input_data)
  np_data = np.fromstring(decoded_data, np.uint8)
  img = cv2.imdecode(np_data, cv2.IMREAD_UNCHANGED)
```

## Postprocessing

The post_process method receives as parameter the model_output, which corresponds to the direct output of the call to onnxruntime.InferenceSession({onnx-model-path}).run({model_output_names}, {pre_processed_input_data}). For most models, you can access the output with model_output[0] and transform it accordingly. The return value of the post_process method is used as a response for the REST interface without further processing. Therefore, numerical values should be rounded accordingly and any field names should be capitalized. 

## Custom methods, files and requirements

During pre- and postprocessing you can access other methods, classes or files (labels etc.) of your own. Just copy them into  the folder "ml-starter / backend / app / custom_model". If your implementation needs any external libraries, you must add them in the file "custom_requirements.txt" in the folder "ml-starter / backend / app / custom_model".

## Access files
In order to access files during the processing you must 1) provide them according to the above instructions (Custom methods, files and requirements) and 2) access them via the helper method get_file() from the file_helper.py. This ensures a safe access even in a containerized environment.
```python
from abstract_model import AbstractModel
from file_helper import get_file


class CustomModel(AbstractModel):

    labels = json.load(open(get_file("labels_map.txt"), "r"))

    #rest of the code omitted..
```

# Persistence
Without further configuration, the user requests as well as the corresponding response of their model are persisted in a SQLite in-memory database. For operation on Heroku, it cannot be ensured that the data is persisted for a longer period of time. For persistent data storage, we recommend creating a no-SQL database at www.cloud.mongodb.com. You can specify the access data to the database afterwards in the <a href="#configuration">Configuration</a>. 

💡 Setting up a MongoDB allows you to gain insights from the user rating of the prediction and use the userdata to improve your model performance.



# Deployment

The integration with docker allows you to run your ML-Starter easily on your local machine or deploy it to a hosting provider. Please make sure, that the running environment provides enough resources (RAM / CPU) to run your model. 

## Local deployment
Open a terminal in the directory "ml-starter /"
```commandline
docker build -t ml-starter .
docker run -d -p 80:3000 -p 8800:8800 ml-starter
```

Access your browser on localhost:#TBD

## Deploy to Heroku
TBD

# How does it work?
The main functionality of ML-Starter is provided by the Python backend. The REST-API is implemented with FastAPI and provides the following endpoints: 

<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/rest-endpoints.png">

The UML sequence diagram shows the message flow of the application:

<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/sequence_diagram.png">



