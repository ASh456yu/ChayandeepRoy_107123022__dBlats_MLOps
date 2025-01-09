import pickle
from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np

import gdown
import pickle

GOOGLE_DRIVE_FILE_ID = "1DFRgHVZwZmXZ3zxER6F_RSdRwJ8DmjS5"
MODEL_FILE_PATH = "model1.pkl"

def download_model():
    url = f"https://drive.google.com/uc?id={GOOGLE_DRIVE_FILE_ID}"
    gdown.download(url, MODEL_FILE_PATH, quiet=False)

try:
    with open(MODEL_FILE_PATH, "rb") as f:
        model = pickle.load(f)
except FileNotFoundError:
    print("Model not found locally. Downloading from Google Drive...")
    download_model()
    with open(MODEL_FILE_PATH, "rb") as f:
        model = pickle.load(f)


app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/predict', methods=['POST'])
def predict():
    try:
        image_file = request.files['image_file']
        model_name = request.form.get('model')

        if not image_file:
            return jsonify({'error': "No image given"}), 400
        if not model_name:
            return jsonify({'error': 'No model specified'}), 400

        image = Image.open(image_file).convert('RGB')
        image = image.resize((256, 256))
        image_array = np.array(image)
        image_array = np.expand_dims(image_array, axis=0)

        result = model.predict(image_array)

        prediction = "dog" if result > 0.5 else "cat"
        return jsonify({'result': prediction}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
