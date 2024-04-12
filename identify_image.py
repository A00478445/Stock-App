import streamlit as st
from PIL import Image, ImageOps
import numpy as np
from tensorflow.keras.models import load_model

# Load the model
model = load_model('image_classifier.keras')

def preprocess_image(image):
    """Resize and format the uploaded image to meet model's expectation."""
    image = ImageOps.grayscale(image)  # Convert to grayscale first if not already
    image = image.resize((28, 28), Image.Resampling.LANCZOS)  # Resize image to 28x28 using high-quality downsampling
    image = np.array(image)  # Convert image to array
    image = image / 255.0  # Normalize the image data to 0-1 range
    image = np.expand_dims(image, axis=0)  # Model expects a batch of images
    return image

def predict(image):
    """Run model prediction on the image and return results."""
    image = preprocess_image(image)
    preds = model.predict(image)
    return np.argmax(preds, axis=1)  # Assuming your model returns a softmax

# Streamlit application
st.title('Image Classifier App')
st.write("Please upload your digit image here:")

uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Classifying...")
    label = predict(image)
    st.write(f"Predicted Digit: {label}")
