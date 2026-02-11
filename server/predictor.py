import joblib, os, requests
import numpy as np
import pandas as pd
from flask import request, jsonify
from io import BytesIO
from keras.models import load_model
from PIL import Image
from datetime import datetime, timedelta

DISEASE_SOLUTIONS = {
    'fall armyworm': {
        'organic_methods': 'Use neem oil sprays, plant cilantro, and introduce trichogramma wasps.',
        'agriclinic_solutions': 'Apply biological insecticides or pheromone traps.'
    },
    'grasshoper': {
        'organic_methods': 'Plant garlic and calendula, encourage birds with perches.',
        'agriclinic_solutions': 'Use insecticides like carbaryl or malathion.'
    },
    'healthy': {
        'organic_methods': 'Implement crop rotation, enrich soil, manage water properly.',
        'agriclinic_solutions': 'Monitor regularly and use balanced fertilizers.'
    },
    'leaf beetle': {
        'organic_methods': 'Handpick beetles, use row covers, apply kaolin clay.',
        'agriclinic_solutions': 'Use pesticides like spinosad if needed.'
    },
    'leaf blight': {
        'organic_methods': 'Improve air circulation with spacing, use copper-based fungicides.',
        'agriclinic_solutions': 'Apply systemic fungicides as needed.'
    },
    'leaf spot': {
        'organic_methods': 'Remove affected leaves, improve air circulation, use sulfur or copper sprays.',
        'agriclinic_solutions': 'Apply fungicides like chlorothalonil.'
    },
    'streak virus': {
        'organic_methods': 'Control aphids, remove infected plants.',
        'agriclinic_solutions': 'Use insecticides for vectors and antiviral agents.'
    }
}

DISEASE_NAMES = list(DISEASE_SOLUTIONS.keys())

# Load the model and classifier

MODEL = load_model(os.getenv('MODEL'))
CLASSIFIER = joblib.load(os.getenv('CLASSIFIER'))


def predict_image(image_bytes):
    """Description:
        predict_image runs inference on the uploaded image and returns the predicted class and possible solution
       Args:
        image_bytes: image data in bytes
    """
    try:
        # Convert bytes to a PIL Image and ensure it is in RGB
        image = Image.open(BytesIO(image_bytes)).convert('RGB')

        # Resize the image to match the input size expected by the model
        image = image.resize((224, 224))

        # Convert the image to a numpy array
        image_array = np.array(image)

        # Normalize the image array to 0-1
        # image_array = image_array / 255.0

        # Add an extra dimension to handle batch size
        image_array = np.expand_dims(image_array, axis=0)

        # Make prediction using the loaded model
        predictions = MODEL.predict(image_array)
        predicted_class_index = np.argmax(predictions[0])
        predicted_class = DISEASE_NAMES[predicted_class_index]

        # Return both the class and its corresponding solution
        return {
            'class': predicted_class,
            'solution': DISEASE_SOLUTIONS[predicted_class],
        }
    except Exception as e:
        # Log error for debugging
        print("Error during image prediction:", str(e))
        return {'error': str(e)}


def handle_prediction():
    """Description:
        handle_prediction retrieves data from the post request then calls the crop_prediction and predict_image functions with desired arguments
        Returns the json response object.
    """
    if request.method == 'POST' and 'image' in request.files:
        try:
            image_file = request.files['image']
            image_bytes = image_file.read()
            # if crop_identifier(image_bytes):
            latitude = request.form['latitude']
            longitude = request.form['longitude']
            alt = crop_prediction(latitude, longitude)
            prediction = predict_image(image_bytes)
                # print(prediction)
            prediction['alt'] = alt
            return jsonify(prediction)
            # else:
            #     return jsonify({'error': 'Not a plant object'})
        except Exception as e:
            return str(e)
    else:
        return jsonify({'error': 'Request must contain an image.'})


def crop_prediction(lat,lon):
    """Description:
        Calls the get_geodata function to get the climatic condition of the user
        Runs prediction on the data using the CLASSIFIER model to get recommended crop for the geographical area
        Returns the predicted crop
      Args:
        lat: latitude of the user
        lon: longitude of the user
    """
    def get_geodata():
        """Description:
                Gets the climate history of location based on latitude and longitude data from the weatherapi.
                It then filter the temperature, humidity, and rainfall data of the area required for crop prediction
                Returns a list of three items [temperature, humidity, rainfall]
        """
        api_key = os.getenv('WEATHER_API')
        date = os.getenv('DATE', (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d'))
        url = f'http://api.weatherapi.com/v1/history.json?key={api_key}&q={lat},{lon}&dt={date}'
        response = requests.get(url)
        weather_data = response.json()
        temperature = weather_data['forecast']['forecastday'][0]['day']['avgtemp_c']
        print(temperature)
        humidity = weather_data['forecast']['forecastday'][0]['day']['avghumidity']
        rainfall = weather_data['forecast']['forecastday'][0]['day']['totalprecip_mm'] * 100 / 2 
        return [temperature, humidity, rainfall]
    
    geo_data = get_geodata()
    new_data = pd.DataFrame([geo_data], columns=['temperature', 'humidity', 'rainfall'])
    crop_prediction_content_based = CLASSIFIER.predict(new_data)[0]  # Access the predicted label with [0]
    # print("Crop Recommendation using Content-Based Filtering:", crop_prediction_content_based)
    return crop_prediction_content_based
