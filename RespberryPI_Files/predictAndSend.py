import os
import shutil
import tensorflow as tf
import numpy as np
import firebase_admin
from firebase_admin import credentials, db
from PIL import Image
from datetime import datetime

model_path = "/home/poison-ivy/trained_model.keras"
model = tf.keras.models.load_model(model_path)
class_name = ['Coleus_Blumei', 'Green_Pepper', 'Guldawari']
source_dir = '/home/poison-ivy/Cur_Run'
base_destination_dir = '/home/poison-ivy/Prev_Run'

def model_prediction(test_image):
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(256, 256))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.expand_dims(input_arr, axis=0)
    predictions = model.predict(input_arr)
    return predictions

def initialize_firebase():
    cred = credentials.Certificate('/home/poison-ivy/myKey.json')
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://plantcare-5de83-default-rtdb.europe-west1.firebasedatabase.app/'
        })
def update_last_run():
    cur_time = datetime.now().strftime("%B %d, %Y: Time %H:%M:%S")
    date_ref = db.reference('date')  
    date_ref.set({'time': cur_time})
    
def create_new_prev_run_directory(base_dir):
    i = 1
    while True:
        new_dir = os.path.join(base_dir, f"Prev_Run_{i}")
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
            return new_dir
        i += 1

initialize_firebase()
ref = db.reference('predictions')

prev_run_subdir = create_new_prev_run_directory(base_destination_dir)

for filename in os.listdir(source_dir):
    if filename.endswith('.jpeg'):
        full_path = os.path.join(source_dir, filename)
        predictions = model_prediction(full_path)
        result_index = np.argmax(predictions)
        pred_round = np.round(predictions[0], 20)
        
        # Determine prediction and confidence
        if pred_round[result_index] >= 0.65:
            prediction = class_name[result_index]
        else:
            prediction = "Unknown Entity"
        
        # Data to push to Firebase
        position = filename.split('.')[0]
        moisture = "45%"
        data = {
            'position': position,
            'prediction': prediction,
            'moisture': moisture
        }
        
        position_ref = ref.order_by_child('position').equal_to(position).get()
        if position_ref:
            for key in position_ref:
                ref.child(key).update(data)
        else:
            ref.push(data)
        
        shutil.move(full_path, os.path.join(prev_run_subdir, filename))
update_last_run()

print("All images processed, predictions made, and data updated successfully.")
