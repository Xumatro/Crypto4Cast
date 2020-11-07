import silence_tensorflow.auto
from keras.layers import LSTM, Dense, Activation, LeakyReLU, PReLU, ThresholdedReLU
from keras.models import Sequential, load_model

# Create a new recurrent neural network with LSTM.
def new_rnn(seq_len=30):

    # Set "input_shape" to one-dimensional
    input_shape = (None, 1)

    # Define a model with some decent defaults.
    model = Sequential()
    model.add(LSTM(units=seq_len, return_sequences=True, input_shape=input_shape))
    model.add(Dense(units=40, activation='relu'))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dense(units=60, activation=LeakyReLU(alpha=0.6)))
    model.add(LSTM(units=70, return_sequences=True))
    model.add(Dense(units=80, activation='elu'))
    model.add(LSTM(units=70, return_sequences=True))
    model.add(LSTM(units=60, return_sequences=True))
    model.add(Dense(units=50, activation='linear'))
    model.add(LSTM(units=40, return_sequences=True))
    model.add(Dense(units=30, activation=LeakyReLU(alpha=0.2)))
    model.add(LSTM(units=20, return_sequences=True))
    model.add(LSTM(units=10, return_sequences=False))
    model.add(Dense(units=1, activation='linear'))
    model.compile(optimizer='rmsprop',loss='mean_squared_error')

    return model

# Train the model on the given dataset.
def train(model, train, test, batchs=3, epochs=25, save=True):

    # Train the model with the given parameters.
    model.fit(x=train[0], y=train[1],
        batch_size=batchs,
        epochs=epochs,
        validation_data=test)

    # If "save" is set, save the trained model for later use.
    if save:
        model.save('predictor.h5')

    return model

# Load a pre-trained model to avoid training everytime.
def load(name):
    model = load_model(name, custom_objects={'LeakyReLU': LeakyReLU, 'PReLU': PReLU})
    model.compile(optimizer='rmsprop', loss='mean_squared_error')

    return model


# Predict future with model.
def predict(model, data, batchs):
    prediction = model.predict(data, batch_size=batchs)

    return prediction
