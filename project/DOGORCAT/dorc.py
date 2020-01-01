import cv2,numpy as np
from tensorflow import keras
from keras.models import load_model
import glob

def dogorcat(path):

    model=load_model('classifier.h5')
    file_path=path
    image=cv2.resize(cv2.imread(file_path),(64,64)).astype(np.float32)
    image = np.expand_dims(image, axis=0)
    out=model.predict(image)

    if out[0][0]==1:
        prediction='dog'
    else:
        prediction='cat'
    return(prediction)