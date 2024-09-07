from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from PIL import Image
import numpy as np
import joblib
import io

app = Flask(__name__)
CORS(app)

# Load the model and label encoder
model = tf.keras.models.load_model('prototype_model.keras')
label_encoder = joblib.load('label_encoder.pkl')

def preprocess_image(img):
    img = img.convert('RGB')  # Convert image to RGB mode
    img = img.resize((224, 224))
    img_array = keras_image.img_to_array(img)
    img_array = preprocess_input(img_array)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})
    
    img_file = request.files['image']
    img = Image.open(io.BytesIO(img_file.read()))
    img_array = preprocess_image(img)
    
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    predicted_label = label_encoder.inverse_transform([predicted_class])[0]
    
    return jsonify({'artwork': predicted_label})

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=5000, debug=False)
