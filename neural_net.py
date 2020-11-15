import silence_tensorflow.auto
from keras.layers import LSTM, Dense, Activation, LeakyReLU, GRU
from keras.activations import elu, tanh
from keras.models import Sequential, load_model
from keras.optimizers import Adamax

# Create a new recurrent neural network with LSTM.
def new_rnn(layers, seq_len, optimizer, loss_function):

    # Define an empty model.
    model = Sequential()
    
    # Loop through layers and build model.
    for index, layer in enumerate(layers):
        activation = get_activation(activation=layer['activation'], alpha=layer['alpha'])

        # Set "first" to True if "index" is zero, else False.
        layer = construct_layer(type=layer['type'], units=layer['units'], activation=activation,
            ret_seq=layer['return_seq'], first=(index == 0), seq_len=seq_len)

        # Append layer to model.
        model.add(layer)

    model.build()
    
    # Set the right optimizer and loss function.
    model.compile(optimizer=optimizer,loss=loss_function)
    
    return model

# Return the right activation function for given input.
def get_activation(activation, alpha):

    # if "activation" is equal to "leaky_relu" get custom activation.
    if activation == 'leaky_relu':
        return LeakyReLU(alpha=alpha)

    return activation

# Return layer base on given input.
def construct_layer(type, units, activation, ret_seq, first, seq_len):

    # Define type set to construct the right layer.
    types = {
        'Dense': Dense(units=units, activation=activation,
            input_shape=(seq_len-1, 1) if first else ()),
        'LSTM': LSTM(units=units, activation=activation, return_sequences=ret_seq,
            input_shape=(seq_len-1, 1) if first else (), unroll=True),
        'GRU': GRU(units=units, activation=activation, return_sequences=ret_seq,
            input_shape=(seq_len-1, 1) if first else (), unroll=True)
    }

    return types.get(type)

# Train the model on the given dataset.
def train(model, train, test, batchs, epochs):

    # Train the model with the given parameters.
    model.fit(x=train[0], y=train[1],
        batch_size=batchs,
        epochs=epochs,
        validation_data=test)

    # Get accuracy metric.
    loss = model.evaluate(test[0], test[1], verbose=1)

    return model, loss

# Load a pre-trained model to avoid training everytime.
def load(filename, optimizer, loss_function):
    model = load_model(filename, custom_objects={ 'LeakyReLU': LeakyReLU })
    model.compile(optimizer=optimizer, loss=loss_function)

    return model


# Predict future with model.
def predict(model, data, batchs):
    prediction = model.predict(data, batch_size=batchs)

    return prediction
