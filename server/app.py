from flask import Flask
from .predictor import handle_prediction


app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/')
def home():
    return "Welcome to the API!"

@app.route('/status')
def status():
    # Example data, replace with real data or logic as needed
    return {'status': 'API is running'}


@app.route('/predict', methods=['POST'])
def predict():
    return handle_prediction()



# @app.route('/crop', methods=['POST'])
# def crop():
    # Replace this with actual logic to fetch crop information
    # return jsonify({'crop': crop_name, 'details': 'Crop details'})
    # return crop_identifier()
    # pass


# if __name__ == '__main__':
#     app.run(debug=True)

