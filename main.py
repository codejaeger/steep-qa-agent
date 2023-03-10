from __future__ import print_function, division
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
set_session(tf.Session(config=config))
import numpy as np
import pytesseract as pt
from keras.layers.core import Dense
from keras.models import Sequential
from keras.models import model_from_json
from keras.optimizers import sgd
from matplotlib import pyplot as plt

from Steep import Steep
from train import train
from test import test


def baseline_model(grid_size, num_actions, hidden_size):
    # setting up the model with keras
    model = Sequential()
    model.add(Dense(hidden_size, input_shape=(grid_size,), activation='relu'))
    model.add(Dense(hidden_size, activation='relu'))
    model.add(Dense(num_actions))
    model.compile(sgd(lr=.01), "mse")
    return model


def moving_average_diff(a, n=100):
    diff = np.diff(a)
    ret = np.cumsum(diff, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def load_model():
    # load json and create model
    json_file = open('model_epoch1000/model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model_epoch1000/model.h5")
    print("Loaded model from disk")
    loaded_model.compile(loss='mse', optimizer='sgd')
    return loaded_model

# To retrain a new model uncomment the 50th line
# model = baseline_model(grid_size=128, num_actions=4, hidden_size=512)
#this will load a pretrained model and continue training
model = load_model() 
#next line will give a model summary after training
# model.summary()
#atmost one line should be uncommented at a time

game = Steep()
# print("game object created")

epoch = 1600    # Number of games played in training
train_mode = 1

if train_mode == 1:
    # Train the model
    hist = train(game, model, epoch, verbose=1)
    print("Training done")
else:
    # Test the model
    hist = test(game, model, epoch, verbose=1)

print(hist)
np.savetxt('model_epoch1000/win_hstory.txt', hist)
plt.plot(moving_average_diff(hist))
plt.ylabel('Average of victories per game')
plt.show()
