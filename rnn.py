import silence_tensorflow.auto

from keras.layers import LSTM, Dense, Activation, LeakyReLU, GRU
from keras.activations import elu, tanh
from keras.models import Sequential, load_model
from keras.optimizers import Adamax

import json


# Define RNN class to hold model and methods
class RNN:
	def __init__(self, rnn_set, data_set, trained):

		# Set given settings for network
		self.settings = RNNSettings(rnn_set)

		# If trained param is given, load model from disk instead of building from scratch
		if trained:
			self.load_model()
			return

		self.model = Sequential()
		
		# Loop through layers and build model
		for index, layer in enumerate(self.settings.layers):
			activation = get_activation(activation=layer['activation'], alpha=layer['alpha'])

			# Set 'first' to True if 'index' is zero, else False
			layer = construct_layer(type=layer['type'], units=layer['units'], activation=activation,
				ret_seq=layer['return_seq'], first=(index == 0), seq_len=data_set.series_lenght)

			# Append layer to model
			self.model.add(layer)

		self.model.build()
	
		# Set the right optimizer and loss function
		self.model.compile(optimizer=self.settings.optimizer,loss=self.settings.loss_function)
			
	# Train the model on the given dataset
	def train(self, train_data, test_data):

		# Train the model with the given parameters
		self.model.fit(x=train_data[0], y=train_data[1],
			batch_size=self.settings.batch_size,
			epochs=self.settings.epochs,
			validation_data=test_data)

		# Get accuracy metric
		loss = self.model.evaluate(test_data[0], test_data[1], verbose=1)

		self.model.save(self.settings.trained_file)
		with open(self.settings.arch_file, 'w') as arch_file:
			json_model = json.loads(self.model.to_json())
			json.dump(json_model, arch_file, indent=3)

		return loss

	# Load a pre-trained model to avoid training everytime
	def load(self):
		self.model = load_model(self.settings.trained_file, custom_objects={ 'LeakyReLU': LeakyReLU })
		self.model.compile(optimizer=self.settings.optimizer, loss=self.settings.loss_function)

	# Predict future with model
	def predict(self, data):
		prediction = self.model.predict(data, batch_size=self.settings.batch_size)

		return prediction


# Define RNNSettings class to hold all RNN related settings
class RNNSettings:
	def __init__(self, rnn_set):
		self.loss_function = rnn_set['loss_function']
		self.trained_file = rnn_set['trained_file']
		self.batch_size = rnn_set['batch_size']
		self.arch_file = rnn_set['arch_file']
		self.optimizer = rnn_set['optimizer']
		self.layers = rnn_set['layers']
		self.epochs = rnn_set['epochs']


# Return the right activation function for given input
def get_activation(activation, alpha):

	# if 'activation' is equal to 'leaky_relu' get custom activation
	if activation == 'leaky_relu':
		return LeakyReLU(alpha=alpha)

	return activation

# Return layer based on given input
def construct_layer(type, units, activation, ret_seq, first, seq_len):

	# Define type set to construct the right layer
	types = {
		'Dense': Dense(units=units, activation=activation,
			input_shape=(seq_len-1, 1) if first else ()),
		'LSTM': LSTM(units=units, activation=activation, return_sequences=ret_seq,
			input_shape=(seq_len-1, 1) if first else (), unroll=True),
		'GRU': GRU(units=units, activation=activation, return_sequences=ret_seq,
			input_shape=(seq_len-1, 1) if first else (), unroll=True)
	}

	return types.get(type)
