<h1 align="center">
    ML-Starter
</h1>

<p align="center">
    <strong>Let's build fast prototypes for your ONNX Models</strong>
</p>





<p align="center">
    | <a href="#getting-started">Getting Started</a> | 
   <a href="/backend/examples">Examples</a> |     
   <a href="#preprocessing-and-postprocessing">Pre- and postprocessing</a> | 
   <a href="#configuration">Configuration</a> | 
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

## Highlights

- Provides a REST-API for your ONNX model
- Provides a React frontend for your ONNX model
- Saves requests and predictions in an online MongoDB
- Lets your user rate the prediction
- Runs everywhere with Docker
- Minimal configuration and implementation required

## Getting started

### Prerequisites

- Docker installation (https://docs.docker.com/get-docker/)
- ONNX model
- Pre- and postprocessing written in Python

### Instructions

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
   docker run
   ```
   💡 To deploy your application to a hosting provider see <a href="#deployment">Deployment</a> for instructions.
   

9) Access the frontend on http://localhost, and the backend on http://localhost:8800/docs

---

<p align="center">
     👉&nbsp; Try out and explore some examples <a href="/backend/examples">here</a>  

</p>

---

# Preprocessing and postprocessing

# Configuration
The file configMap.json contains the configuration which is mainly used by the frontend. The following list defines all available configuration keys. The names of the keys cannot be changed.

| **Key** | **Description** | **Type** | **Example** | **Default** |
|---|---|---|---|---|
| applicationName (optional) | This name is displayed in the header of the web application. | String | My demoapplication | My ML-starter demo application |
| description (optional) | Short text to introduce your model to the user. This text is displayed above the input fields. | String | This model recognizes classes in a given image | Please provide the data in the input fields below and start the prediction. |
| input | Array containing an element for each expected input. The frontend creates one inputfield for the user for each element. An element has 3 attributes id (str), label (str), type (str). The id is used to link input fields to the requestObject. The label is the text which is displayed above the field. The type is one of "number", "str", or "image" and is used to display the field accordingly. | Array[Object] | [  {   "id": "textInput",    "label": "Enter text for prediction",     "type": "str"  } ] | - |
| requestObject | Object defining the shape of the expected input data of the backend. Use the id's of the input fields as placeholder for the input values. | Object | {"inputData": "inputText"} | - |


# Persistence

# Deployment

# How does it work?

