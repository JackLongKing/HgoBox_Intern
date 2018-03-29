from keras.models import load_model
from keras.utils.generic_utils import CustomObjectScope
import keras
from PIL import Image
import os
import pandas as pd
import numpy as np


MODEL_DIR = '..\\data\\model'
TEST_DIR = '..\\data\\test'
OUT_DIR = '..\\data\\submission'
SUBMISSION_NUMBER = 12800

os.chdir(os.getcwd())

df = pd.DataFrame(np.ones(shape=(SUBMISSION_NUMBER, 1), dtype=np.int), columns=['predicted'])
df.index += 1

# image_list = []
# id_list = []

# for i in os.listdir(TEST_DIR):
#     image = np.array(Image.open(os.path.join(TEST_DIR, i)))
#     image_list.append(image)
#     id_list.append(int(i[:-4]))
#
# model = load_model(os.path.join(MODEL_DIR, 'model.h5'))
# prediction = np.argmax(model.predict(np.array(image_list), batch_size=16, verbose=1), axis=1)+1
#
#
#
# for i, j in zip(id_list, prediction):
#     df.loc[i, 'predicted'] = j

with CustomObjectScope({'relu6': keras.applications.mobilenet.relu6,
                        'DepthwiseConv2D': keras.applications.mobilenet.DepthwiseConv2D}):
    model = load_model(os.path.join(MODEL_DIR, 'model.h5'))

for j, i in enumerate(os.listdir(TEST_DIR)):
    image = np.array(Image.open(os.path.join(TEST_DIR, i)).resize((224, 224)))/255
    prediction = int(np.argmax(model.predict(np.expand_dims(image, axis=0))[0])+1)
    df.loc[int(i[:-4]), 'predicted'] = int(prediction)
    if j % 100 == 0:
        print(j)

df.index.name = 'id'
df.to_csv(os.path.join(OUT_DIR, 'submission.csv'))
