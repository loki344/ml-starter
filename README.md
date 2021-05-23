<h1 align="center">
    ML-Starter
</h1>

<p align="center">
    <strong>Let's build fast prototypes for your PMML and ONNX Models</strong>
</p>



<p align="center">
    | <a href="#quickstart">Quickstart</a> | 
   <a href="/backend/examples">Examples</a> |    
   <a href="/backend/examples">Integrate your model</a> |    
   <a href="https://github.com/loki344/ml-starter/tree/master/docs/architecture">Architecture</a> |
</p>

Tired of building web-applications for your machine learning models to enable users to interact with it? ML-Starter lets
you focus on your model performance rather than writing backend- and frontend-code. ML-Starter is built on FastAPI and
React. Its integration with Docker allows you to run your application locally or deploy it to a hosting provider such
as https://www.heroku.com. User requests and predictions can be saved in a free online MongoDB such
as https://www.mongodb.com

<sup>Alpha version: Only suggested for experimental usage.</sup>


<img style="width: 100%" src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/combined_efficientnet.png"/>

---

<p align="center">
     Try out some applications running with ML-Starter <a href="/backend/examples">here</a>.
</p>

---

# Highlights

- Provides a REST-API for your ONNX model
- Provides a React frontend for your ONNX model
- Lets you save requests and predictions in an online MongoDB
- Learn from the feedback of your users
- Runs everywhere with Docker
- Minimal configuration and implementation required

---

<h4 align="center">:star: Get started with the quickstart or explore the possibilities to integrate your own model <a href="https://github.com/loki344/ml-starter/tree/master/docs/integration">here</a> :star:</h3>

---

# Quickstart

<strong>What you'll build</strong><br/>
The "Hello World" of Machine Learning: An Iris classification model which takes in the measurements of a flowers and
predicts the classes.<br/><br/>
<strong>What you'll need</strong><br/>

1) An IDE such as PyCharm or Visual Studio Code
2) Docker installation (https://docs.docker.com/get-docker/)

## Step 1: Clone the repository

Either download the repository or copy the command in the commandline:

```commandline
git clone https://github.com/loki344/ml-starter.git
```

## Step 2: Copy the model file

Locate the <strong>custom_model.xml</strong> in the <strong>
ml-starter/backend/examples/iris-classification-pmml/</strong> directory. Copy it to the <strong>
ml-starter/app/custom_model</strong> folder.

## Step 3: Implement the pre- and postprocessing

Open the project in your IDE and locate the <strong>custom_model.py</strong> file in the <strong>
backend/app/custom_model</strong> folder. Now replace the contents of the file with the code below. If you want to, you can customize the applicationName or the description.

```python
import numpy as np
from model.pmml_model import PMMLModel


class CustomModel(PMMLModel):

    def pre_process(self, input_data, model) -> dict:
        return input_data

    @staticmethod
    def post_process(model_output: object) -> object:
        return model_output[0]

```

## Step 4: Configure the application

Open the <strong>custom_requirements.txt</strong> file from the folder <strong>backend/app/custom_model</strong> and
copy the required dependency of the pre- and postprocessing from below.

```text
numpy~=1.19.5
```

Open the <strong>configMap.json</strong> file from the folder <strong>backend/app/custom_model</strong>. In order to
define the desired user inputs and the structure of the requestObject you have to replace the content with the text
below.

<details>
<summary>configMap.json</summary>
<p>

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

</p>
</details>

## Step 5: Launch the application and try it out

Docker makes the launch of the application very easy. Open the command line in the <strong>ml-starter/</strong>
directory and execute the following code. This will take a while.

```commandline
docker build -t ml-starter-iris-pmml-example .
docker run -d -p 80:3000 -p 8800:8800 ml-starter-iris-pmml-example
```
If everything worked you should get the container-id as an output in the console:
```text
#container-id, your output can look differently
7647e273167e69e6987cbf7c4f2393203af2f940bb058ae9084c4dcefb63571f
```
<strong>Let's try it out!</strong><br/>
Open your browser and access "localhost".

<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/quickstart1.png">

Now you can enter the measurements of an iris flower and start the prediction.

The result will be displayed like this:
<img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/quickstart2.png">

<br/>
<h3 align="center">Easy - isn't it?<br></h3><h4>Ml-Starter is proven to integrate seamlessly with www.heroku.com. Learn more about integrating your model <a href="https://github.com/loki344/ml-starter/tree/master/docs/integration">here</a>.</h4>
