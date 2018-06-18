'''
Driver program for detection of hand written digits.
Draw your digits in real time and hit the 'go' button to see the prediction.

Model trained using the MNIST dataset
'''

import paint
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import pandas as pd
import os

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("model.h5")
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

p = paint.Paint(model)
