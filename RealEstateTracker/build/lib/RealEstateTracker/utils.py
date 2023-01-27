import joblib
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
