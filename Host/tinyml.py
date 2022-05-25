import numbers
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import math
import numpy as np
import tensorflow as tf

from tensorflow import keras
layers = keras.layers

SAMPLES_PER_GESTURE = 120

Model = None

def CreateModel():
    # create a NN with 2 layers of 16 neurons
    model = tf.keras.Sequential()
    model.add(layers.Dense(32, activation='relu', input_shape=(6 * SAMPLES_PER_GESTURE,)))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(2, activation='softmax'))

    opt_adam = keras.optimizers.Adam()
    model.compile(optimizer=opt_adam, loss='categorical_crossentropy', metrics=['categorical_accuracy'])   
    model.summary()
    
    return model


def PrepareModel(model):
    SAMPLES = 100
    np.random.seed(1337)
    
    x_values = np.random.uniform(low=0, high=2 * math.pi, size=(SAMPLES, 6 * SAMPLES_PER_GESTURE))
    # shuffle and add noise
    np.random.shuffle(x_values)
    y_values = np.random.uniform(low=0, high=1, size=(SAMPLES, 2))
    #y_values = np.random.randn(*y_values.shape)

    Train(model, x_values, y_values)
    

def TrainModel(model, x, y):
    # split into train, validation, test
    TRAIN_SPLIT =  int(0.8 * SAMPLES)
    x_train, x_validate = np.split(x, [TRAIN_SPLIT, ])
    y_train, y_validate = np.split(y, [TRAIN_SPLIT, ])
   
    model.fit(x_train, y_train, epochs=200, batch_size=16, validation_data=(x_validate, y_validate))


def ConvertModel(model):
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    with open("model.tflite", "wb") as f:
        f.write(tflite_model)


# Function: Convert some hex value into an array for C programming
def Hex2H(model, h_model_name):
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    
    c_str = ''
    model_len = len(tflite_model)

    # Create header guard
    c_str += '#ifndef ' + h_model_name.upper() + '_H\n'
    c_str += '#define ' + h_model_name.upper() + '_H\n'

    # Add array length at top of file
    c_str += '\nunsigned int ' + h_model_name + '_len = ' + str(model_len) + ';\n'

    # Declare C variable
    c_str += 'unsigned char ' + h_model_name + '[] = {'
    hex_array = []
    for i, val in enumerate(tflite_model) :
        # Construct string from hex
        hex_str = format(val, '#04x')

        # Add formatting so each line stays within 80 characters
        if (i + 1) < model_len:
          hex_str += ','
        if (i + 1) % 12 == 0:
          hex_str += '\n '
        hex_array.append(hex_str)

    # Add closing brace
    c_str += '\n ' + format(' '.join(hex_array)) + '\n};\n\n'

    # Close out header guard
    c_str += '#endif //' + h_model_name.upper() + '_H\n'
        
    # Write TFLite model to a C source (or header) file
    with open(h_model_name + '.h', 'w') as file:
        file.write(c_str)   


def ReadData(file, v):
    size = SAMPLES_PER_GESTURE * 6

    dataX = np.empty([0, size])
    dataY = np.empty([0, 2])

    base_path = os.path.dirname(__file__)
    file = open(base_path + "/data/" + file, "r")

    data = []
    for line in file.readlines():
        items = line.split()
        values = [int(v) for v in items ]
        data += values

    count = len(data)

    for i in range(0, count, size):
        tmp = np.array(data[i: i + size])
        if len(tmp) == size:
            tmp = np.expand_dims(tmp, axis=0)

            dataX = np.concatenate((dataX, tmp), axis=0)
            dataY = np.concatenate((dataY, [[0, 1]] if v == 0 else [[1, 0]]))

    return dataX, dataY

ReadData("circle.csv", 1)

Model = CreateModel()
PrepareModel(Model)
ConvertModel(Model)
Hex2H(Model, "model")