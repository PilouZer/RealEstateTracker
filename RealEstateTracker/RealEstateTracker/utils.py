import joblib
import numpy as np
import base64

# from google.cloud import storage

# def upload_model_to_gcp(self):

#     client = storage.Client()

#     bucket = client.bucket(self.BUCKET_NAME)

#     blob = bucket.blob(self.STORAGE_LOCATION)

#     blob.upload_from_filename('model.joblib')

def save_model(model):
    """ Save the trained model into a model.joblib file """
    joblib.dump(model, 'model.joblib')
    print("Model saved as model.joblib")
#     self.upload_model_to_gcp()
#     print(f"uploaded model.joblib to gcp cloud storage under \n => {self.STORAGE_LOCATION}")

def load_model(model):
    """ Loads the trained model from a joblib file in the specified path """
    print(f"Model loaded from path {model}")
    return joblib.load(model)

def custom_pred(model,X_test):
    """Custom prediction function. It's going to do the same as the model.predict
    but returning the exponent of the values"""
    y_pred_log = model.predict(X_test)
    return np.exp(y_pred_log)

def load_image(path):
    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded

def image_tag(path):
    encoded = load_image(path)
    tag = f'<img src="data:image/png;base64,{encoded}">'
    return tag
