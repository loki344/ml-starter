<h1 align="center">
    Customization
</h1>

This chapter will guide you through the process to integrate your own GUI with ML-Starter. You will only deploy the backend module, which will only serve the endpoints for the prediction. Basic HTML / Javascript templates can be served by the backend. 

# Overview

- <a href="#basic-html-template-serving">Basic HTML template serving</a>
- <a href="#deployment-with-docker">Deployment with Docker</a>
- <a href="#custom-frontend-application">Custom frontend application</a>


# Prerequisites

- Finished steps 1-3 and 5-7 from the <a href="https://github.com/loki344/ml-starter/tree/master/docs/integration">Integration</a> chapter in order to provide the prediction REST-endpoints.
- Docker installed (if you want to deploy it with docker)


# Basic HTML template serving

1) Save your landing page as "index.html" in the folder "ml-starter / backend / app / static / templates". To create a new prediction make a POST request as shown below. Make sure the requestBody matches the expected input of your model. Requests to the path "/" will be routed to the index.html. Requests to localhost:8800/examplePath will be routed to the template "examplePath.html".

    ```text
    # Most important endpoints
    
    # POST /api/predictions
    # The naming of "input_data" is mandatory
    requestBody = { "input_data": InputDataHere }
    
    #GET /api/predictions
    
    #PATCH /api/predictions
    {"id": idOfCreatedPrediction, "rating": userRating }
    
    ```
   This is an example for the Iris-PMML example from this repository.<br>
   index.html
    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Custom HTML</title>
    </head>
    <body>
    
    <h1 style="text-align: center">This is my custom HTML Frontend for the Iris PMML Model</h1>
    <h2 style="text-align: center">Enter the measurements of a flower and start the prediction</h2>
    <a href="someOtherPage">Link to other page</a>
    <form>
        <div style="margin-top: 2rem">
            <label>Sepal length</label>
            <input id="sepal-length" type="number">
        </div>
        <div style="margin-top: 2rem">
            <label>Sepal width</label>
            <input id="sepal-width" type="number">
        </div>
        <div style="margin-top: 2rem">
            <label>Petal length</label>
            <input id="petal-length" type="number">
        </div>
        <div style="margin-top: 2rem">
            <label>Petal width</label>
            <input id="petal-width" type="number">
        </div>
    
        <button onclick="function postPrediction(event) {
            let sepalLength = document.getElementById('sepal-length').value
            let sepalWidth = document.getElementById('sepal-width').value
            let petalLength = document.getElementById('petal-length').value
            let petalWidth = document.getElementById('petal-width').value
    
            var xhttp = new XMLHttpRequest();
    
            xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 201) {
            document.getElementById('predictionContainer').innerHTML = JSON.parse(this.responseText).prediction;
            }
            };
    
            xhttp.open('POST', '/api/predictions')
            xhttp.send(JSON.stringify({'input_data':[sepalLength, sepalWidth, petalLength, petalWidth]}))
    
        }
        postPrediction()" style="margin-top: 2rem" type="button">Start prediction
        </button>
    
    </form>
    
    <div id="predictionContainer" style="margin-top: 3rem; font-weight: bold">
    
    </div>
    
    </body>
    </html>

    ```
   someOtherPage.html
   ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
    <h1>This is just a page to show you how to access resources</h1>
    <a href="/">Back to home</a>
    <br>
    <img src="resources/matterhorn.jpg">
    
    </body>
    </html>

    ```
   
2) Place your resources like css or images in the folder "ml-starter / backend / app / static / resources"
    
    ```text
   # Structure of this example, only relevant directories shown
    - ml-starter
       - backend
          - app
             - static
                - resources
                   - matterhorn.jpg
                - templates
                   - index.html
                   - someOtherPage.html
    ```
3) Start the application with the commandline or <a href="#deployment">Deploy the application as a docker container</a>
    ```commandline
    # directory: ml-starter/backend/app
   uvicorn main:app --host localhost --port 8800 --reload
    ```
   Access the application on http://localhost:8800<br>
   You can discover the REST-API on http://localhost:8800/docs
   
   
   The source code is also available <a href="https://github.com/loki344/ml-starter/tree/master/backend/examples/custom-frontend">here</a>
   The template shown in this example looks very basic:
   <img src="https://raw.githubusercontent.com/loki344/ml-starter/master/docs/images/examplehtmlapplication.png">

# Deployment with Docker

## Locally

To start the docker container locally:

Open a terminal in the ml-starter/backend directory
```commandline
docker build -t ml-starter-backend .
docker run -d -p 8800:8800 ml-starter-backend
```
Access the application on http://localhost:8800<br>
You can explore the REST endpoints on http://localhost:8800/docs <br>


## Heroku

In order to deploy your application to heroku you'll need a heroku account and the CLI from heroku.

https://devcenter.heroku.com/articles/heroku-cli#download-and-install

Open a terminal in the directory "ml-starter"

If your Heroku CLI is not yet authenticated:
```commandline
heroku login
heroku container:login
```

Then create a new app with:
```commandline
heroku create
```
This will give you an output like:

```commandline
robert@tux-polaris-15:~/Repositories/ml-starter$ heroku create
Creating app... done, ??? sheltered-tundra-78112
```
Now copy the generated application name, in this example it's sheltered-tundra-78112. Replace the {yourApplicationName} in the commands below with the application name.

```commandline
docker build -t ml-starter-backend .

docker tag ml-starter-backend registry.heroku.com/{yourApplicationName}/web
docker push registry.heroku.com/{yourApplicationName}/web
heroku container:release web --app {yourApplicationName}
heroku open --app {yourApplicationName}
```

With the last command, a browser window should open the app on heroku. Note that it could take a while to start. If it does not start after a while, you can check the log with the following command:

```commandline
heroku logs --tail --app {yourApplicationName}
```



# Custom frontend application
You can also build your own frontend with a framework of your choice and only consume the endpoints of ML-Starter. To create a new prediction, POST a requestBody containing the inputData as your model expects it to /api/predictions as shown below. It is recommended to explore the backend on http:localhost:8800/docs. Start the backend with the following command:

 ```commandline
 # directory: ml-starter/backend/app
uvicorn main:app --host localhost --port 8800 --reload
 ```

<br>
<strong>Note that the deployment to heroku is not supported for this approach. It will result in a docker container running the REST-API and your frontend running separately.</strong>

 ```text
    # Most important endpoints
    
    # POST /api/predictions
    # The naming of "input_data" is mandatory
    requestBody = { "input_data": InputDataHere }
    
    #GET /api/predictions
    
    #PATCH /api/predictions
    {"id": idOfCreatedPrediction, "rating": userRating }
 ```


