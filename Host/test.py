import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
import numpy as np
import pandas as pd
from tqdm import tqdm

SAMPLES_PER_GESTURE = 70

punch = pd.read_csv('data/punch.csv', header=None)
flex = pd.read_csv('data/flex.csv', header=None)
print(punch)
print(flex)


def processData(d, v):
    dataX = np.empty([0, SAMPLES_PER_GESTURE*6])
    dataY = np.empty([0])

    data = d.values
    dataNum = data.shape[0] // SAMPLES_PER_GESTURE
    print(data.shape, data.shape[0])

    for i in tqdm(range(data.shape[0])):
        tmp = []
        for j in range(SAMPLES_PER_GESTURE):
            tmp += [(data[i * SAMPLES_PER_GESTURE + j][0] + 4.0) / 8.0]
            tmp += [(data[i * SAMPLES_PER_GESTURE + j][1] + 4.0) / 8.0]
            tmp += [(data[i * SAMPLES_PER_GESTURE + j][2] + 4.0) / 8.0]
            tmp += [(data[i * SAMPLES_PER_GESTURE + j][3] + 2000.0) / 4000.0]
            tmp += [(data[i * SAMPLES_PER_GESTURE + j][4] + 2000.0) / 4000.0]
            tmp += [(data[i * SAMPLES_PER_GESTURE + j][5] + 2000.0) / 4000.0]

        tmp = np.array(tmp)

        tmp = np.expand_dims(tmp, axis=0)

        dataX = np.concatenate((dataX, tmp), axis=0)
        dataY = np.append(dataY, v)

    return dataX, dataY


punchX, punchY = processData(punch, 0)
flexX, flexY = processData(flex, 1)
dataX = np.concatenate((punchX, flexX), axis=0)
dataY = np.concatenate((punchY, flexY), axis=0)

permutationTrain = np.random.permutation(dataX.shape[0])
print(permutationTrain)

dataX = dataX[permutationTrain]
dataY = dataY[permutationTrain]
print(dataY)


vfoldSize = int(dataX.shape[0]/100*20)

xTest = dataX[0:vfoldSize]
yTest = dataY[0:vfoldSize]

xTrain = dataX[vfoldSize:dataX.shape[0]]
yTrain = dataY[vfoldSize:dataY.shape[0]]
model = keras.Sequential()
model.add(keras.layers.Dense(32, input_shape=(6*SAMPLES_PER_GESTURE,), activation='relu'))
model.add(keras.layers.Dense(16, activation='relu'))
model.add(keras.layers.Dense(2, activation='softmax'))
adam = keras.optimizers.Adam()
model.compile(loss='sparse_categorical_crossentropy', optimizer=adam, metrics=['sparse_categorical_accuracy'])
model.summary()
