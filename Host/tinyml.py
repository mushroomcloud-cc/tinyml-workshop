import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import math
import numpy as np
import tensorflow as tf


from tensorflow.keras import layers

SAMPLES_PER_GESTURE = 200

Model = None

def CreateModel():
    # create a NN with 2 layers of 16 neurons
    model = tf.keras.Sequential()
    model.add(layers.Dense(16, activation='relu', input_shape=(6, SAMPLES_PER_GESTURE, )))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])   
        
    model.summary()
    
    return model


def PrepareModel(model):
    SAMPLES = 1000
    np.random.seed(1337)
    
    x_values = np.random.uniform(low=0, high=2 * math.pi, size=(SAMPLES, 6, SAMPLES_PER_GESTURE))
    # shuffle and add noise
    np.random.shuffle(x_values)
    y_values = np.random.uniform(low=0, high=1, size=SAMPLES)
    #y_values = np.random.randn(*y_values.shape)

    # split into train, validation, test
    TRAIN_SPLIT =  int(0.8 * SAMPLES)
    x_train, x_validate = np.split(x_values, [TRAIN_SPLIT, ])
    y_train, y_validate = np.split(y_values, [TRAIN_SPLIT, ])
   
    model.fit(x_train, y_train, epochs=200, batch_size=16, validation_data=(x_validate, y_validate))
    
    return

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



Model = CreateModel()
PrepareModel(Model)
ConvertModel(Model)
Hex2H(Model, "model")