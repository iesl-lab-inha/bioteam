import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, Layer, Flatten, SimpleRNN, Bidirectional
from sklearn.model_selection import train_test_split
from scipy import io
from nested_lstm import NestedLSTMCell

import matplotlib.pyplot as plt
import numpy

mat_file = io.loadmat('Shimmer_data(MERTI-APPs)_ppg_zero_signal.mat')
data = mat_file.get('ppg_zero_signal')[:, 0:1100]
data = data.reshape(data.shape[0], data.shape[1], 1)

target = mat_file.get('ppg_zero_signal')[:, 1100]

for i in range(0, 49026):
    if target[i] > 0.:
        target[i] = 1
    else:
        target[i] = 0

print("data.shape:", data.shape)
print("target.shape:", target.shape)

print("data: ", data)
print("target: ", target)

x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.2, shuffle=False, random_state=34)
x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.25, shuffle=False, random_state=34)

print(x_train.shape)

# bulid model

model = Sequential()
model.add(Dense(128, input_shape=(1100, 1), activation='relu'))
model.add(LSTM(128, input_shape=(1100, 1), activation='tanh', return_sequences=False))
model.add(Dense(1, activation='sigmoid'))

opt = tf.keras.optimizers.Adam(learning_rate=0.001,
    beta_1=0.9,
    beta_2=0.999,
    epsilon=1e-07,
    amsgrad=False,
    name="Adam",)

# opt = tf.keras.optimizers.SGD(lr=0.01, decay=0, momentum=0.9, nesterov=True)
model.compile(loss='binary_crossentropy', optimizer='adam',
             metrics=['accuracy', 'binary_accuracy'])

model.summary()

history = model.fit(x_train, y_train, epochs=20, validation_data=(x_valid, y_valid), batch_size=256)

print('\nAccuracy: {:.4f}'.format(model.evaluate(x=x_test, y=y_test)[1]))

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

y_vloss = history.history['val_loss']
y_loss = history.history['loss']

x_len = numpy.arange(len(y_loss))

plt.plot(x_len, y_vloss, marker='.', c='red', label="Validation-set Loss")
plt.plot(x_len, y_loss, marker='.', c='blue', label="Train-set Loss")

plt.legend(loc='upper right')
plt.grid()
plt.xlabel('epoch')
plt.ylabel('loss')
plt.show()

# for i in range(len(y_test)):
#     print('True : ' + str(y_test[i]) + ', Predict : ' + (model.predict(y_test[i]) > 0.5).astype("int32"))

model.save('PPG_Lstm.model')
