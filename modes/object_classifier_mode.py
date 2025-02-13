import tensorflow as tf
import numpy as np
import cv2

# Load pre-trained MobileNet model
model = tf.keras.applications.MobileNetV2(weights='imagenet')

def preprocess_image(image):
    image = cv2.resize(image, (224, 224))  # Resize for MobileNet
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

def classify_object(frame):

    print("entered classifcation mode")
    image = preprocess_image(frame)
    predictions = model.predict(image)
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=1)[0]
    object_name, _, confidence = decoded_predictions[0]
    print(f"Detected: {object_name} with {confidence*100:.2f}% confidence")
    return frame
