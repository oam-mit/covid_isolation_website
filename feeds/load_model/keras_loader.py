from keras.models import model_from_json

import os
from distancing import settings

def load_keras_model(*args):
    try:
        model = model_from_json(open(str(os.path.join(settings.BASE_DIR,'feeds/model/face_mask_detection.json'))).read())
        model.load_weights(os.path.join(settings.BASE_DIR,'feeds/model/face_mask_detection.hdf5'))
    except Exception as e:
        print("Not loaded")
        print(e)
    return model


def keras_inference(model, img_arr):
    try:
     
        result = model.predict(img_arr)
    except Exception as e:
       
        print(e)
    y_bboxes= result[0]
    y_scores = result[1]
    return y_bboxes, y_scores