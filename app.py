import pickle
from flask import Flask, render_template, request, jsonify, g
from PIL import Image
import numpy as np

app = Flask(__name__, template_folder='templates')

def load_model1():
    if 'model1' not in g:
        with open("Saved Models/model_pickle1", "rb") as f:
            g.model1 = pickle.load(f)
    return g.model1

def load_model2():
    if 'model2' not in g:
        with open("Saved Models/model_pickle2", "rb") as f:
            g.model2 = pickle.load(f)
    return g.model2

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

        if model_name == "Deep Neural Network":
            model = load_model1()
        elif model_name == "Resnet 152":
            model = load_model2()
        else:
            return jsonify({'error': 'Invalid model specified'}), 400

        result = model.predict(image_array)
        prediction = "dog" if result > 0.5 else "cat"
        return jsonify({'result': prediction}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
