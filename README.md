# MAIZA API- Backed API for Maize Leaf Disease Prediction
> MAIZA API is a backend project that classifies the health status of a Maize Leaf from captured Image.

    The models are trained on data from [Mensah et al](#maiza-api--backed-api-for-maize-leaf-disease-prediction)
    The model can classify the image into seven classes, ie., Fallarmyworm, Grasshopper, Healthy, Leafbeetle, Leafblight, Leafspot, and Streakvirus.


Endpoints available:
- / : Welcome page (GET)
- /status: Returns the status of the API (GET)
- /predict: Returns the prediction and recommendation (POST)

The endpoint for prediction and classification is at '/predict'. The endpoint only accepts POST requests.
    
Required data and field labels for the prediction are:
- latitude: latitude coordinate of the user
- longitude: longitude coordinate of the user
- image: uploaded image file of the maize file

> Below is a demonstration of a POST request and the returned response.

![successful response](./post-request-demo.png)

> Post request using curl
```
curl -X POST "http://127.0.0.1:5000/predict" -F "latitude=-0.1746" -F "longitude=34.9163" -F "image=@/path/to/image"
```

## Requirements
- weather API key [weatherapi](https://weatherapi.com/)
- python >=3.10 <3.12
- docker (optional)

## Installation
 - Clone this repository to your local machine and change into the directory
     ```
     git clone https://github.com/hawkinswinja/maiza-api.git && cd maiza-api
     ```
- Download and Extract the models
    ```
    wget --no-check-certificate "https://drive.google.com/uc?export=download&id=12Tk3gsAVO891rMvOhniWh5RNwsqeZSnk" -O maiza_models.tar
    tar -xf maiza_models.tar
    ```

- Create and activate a virtual environment
    ```
    python -m venv virt && source virt/bin/activate

    # windows
    python -m venv virt && source virt\Scripts\activate
    ```
- Install dependencies listed in requirements.txt
    ```
    python -m pip install -r requirements.txt
    ```
- launch the server using gunicorn (ubuntu)
    ```
    gunicorn server.app:app
    ```
    - use waitress for windows 
    ```
    waitress-serve --listen=*:8000 server.app:app
    ```

- access the url at `127.0.0.1:8000`

> alternatively if using docker, run the following command to run the image

```
docker pull hawkinswinja/maiza:v4
docker run -p 8000:5000 -v ./server/.env:/app/.env 
```

&copy; hawkinswinja