from flask import Flask, jsonify
from .predictor import handle_prediction
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False

limiter = Limiter(
  get_remote_address,
  app=app,
  storage_uri=getenv('REDIS'),
  storage_options={"socket_connect_timeout": 30},
  default_limits=["100 per day", "10 per minute"],
  strategy="fixed-window", # or "moving-window"
)


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(error=f"ratelimit exceeded {e.description}"), 429

@app.route('/')
def home():
    return "Welcome to the API!"

@app.route('/status')
def status():
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

