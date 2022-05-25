import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
import numpy as np
import pandas as pd
from tqdm import tqdm

SAMPLES_PER_GESTURE = 70

punch = pd.read_csv('data/punch.csv', header=None).values
flex = pd.read_csv('data/flex.csv', header=None).values

punch = np.array(punch)
flex = np.array(flex)

for n in range(6):
    punch = np.concatenate((punch, punch))
    flex = np.concatenate((flex, flex))

print(punch)
print(flex)


def processData(data, v):
    dataX = np.empty([0, SAMPLES_PER_GESTURE * 6])
    dataY = np.empty([0, 2])

    dataNum = data.shape[0] // SAMPLES_PER_GESTURE
    print(data.shape, data.shape[0])

    for i in tqdm(range(dataNum)):
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
        dataY = np.concatenate((dataY, [[0, 1]] if v == 0 else [[1, 0]]))

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
model.add(keras.layers.Dense(32, input_shape=(6 * SAMPLES_PER_GESTURE,), activation='relu'))
model.add(keras.layers.Dense(16, activation='relu'))
model.add(keras.layers.Dense(2, activation='softmax'))

adam = keras.optimizers.Adam()
model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['categorical_accuracy'])
model.summary()


vfoldSize = int(dataX.shape[0]/100*20)

xTest = dataX[0:vfoldSize]
yTest = dataY[0:vfoldSize]

xTrain = dataX[vfoldSize:dataX.shape[0]]
yTrain = dataY[vfoldSize:dataY.shape[0]]

history = model.fit(xTrain, yTrain, batch_size=1, validation_data=(xTest, yTest), epochs=200, verbose=1)