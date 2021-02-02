import datetime, pandas, numpy


# Define Data class to hold all the gathered data and methods to transform it
class Data:
	def __init__(self, response, data_set):
		self.settings = data_set
		self.history = response['Data']['Data']
		
		self.data_frame = None
		self.price_matrix = None

	# Clean the history data by filtering out unneeded parts
	def clean_history(self):
		stop_trim = False
		start_index = 0

		# Loop through data, enumerating entries
		for index, entry in enumerate(self.history):

			# Convert 'time' timestamp to readable date format 'date'
			entry['date'] = (datetime.datetime.fromtimestamp(entry['time'])
				.strftime('%Y-%m-%d'))
			del entry['time']

			to_predict = {
				"open": entry['open'],
				"close": entry['close'],
				"high": entry['high'],
				"low": entry['low'],
				"oc_avg": (entry['open'] + entry['close']) / 2,
				"hl_avg": (entry['high'] + entry['low']) / 2,
			}
			
			# Add a 'course field to every entry of the history data
			entry['course'] = to_predict.get(self.settings.to_predict)

			# If trim is set, set startindex to the index of the first nonzero value
			if self.settings.trim_leading_blank:
				if entry['high'] == 0 and not stop_trim:
					start_index = index + 1
				else:
					stop_trim = True

			# Delete all unnecessary info, we will only need a datestamp and an average price
			unnecessary_data = (["conversionSymbol", "conversionType", "volumeto",
			"volumefrom", 'close', 'open', 'high', 'low'])

			for data_entry in unnecessary_data:
				del entry[data_entry]

		self.history = self.history[start_index:]

	# Convert our json data into a pandas dataframe
	def create_data_frame(self):

		# Create a new pandas dataframe from the given data
		data_frame = pandas.DataFrame(self.history, columns=['course', 'date'])

		# Convert the given date in string format to a pandas datetime
		data_frame['date'] = pandas.to_datetime(data_frame['date'], format='%Y-%m-%d')

		# Group our data by date
		self.data_frame = data_frame.groupby('date').mean()['course']

	# Convert our data to a series of nested lists where every
	# list contains data from 'series_lenght' entries
	def create_price_matrix(self):
		matrix = []

		# Loop over data in chunks of 'series_lenght' and add a sublist to the price matrix
		for index in range(0, len(self.data_frame) - (self.settings.series_lenght - 1)):
			matrix.append(self.data_frame[index:(index + self.settings.series_lenght)])
			# If we started with data of lenght n, our matrix would now look like this:
			# [[0..series_lenght],
			# [1..series_lenght+1],
			# ....
			# [n-series_lenght..n]]
	
		self.price_matrix = numpy.array(matrix)

	# Normalize the price matrix to reflect percent change from starting point
	def normalize_matrix(self):
		normalized_matrix = []

		# Loop over price matrix and get the sublists
		for sublist in self.price_matrix:
			# Calculate the percent change of the entry compared to the first entry in the sublist
			normalized_matrix.append([((price / sublist[0]) - 1.0) for price in sublist])

		self.price_matrix = numpy.array(normalized_matrix)

	# Split the price matrix into test and train datasets
	def split_test_train(self):

		# Define spliting point base on 'train_size'
		split_point = int(round(self.settings.train_test_ratio * len(self.price_matrix)))

		# Set train dataset to everything up to 'split_point'
		train_set = self.price_matrix[:split_point]
		test_set =self.price_matrix[split_point:]

		# Remove last entry from 'x_' lists, and everything but last the last entry from 'y_' lists
		x_train, y_train = (train_set[:, :-(self.settings.prediction_len)],
			train_set[:, -(self.settings.prediction_len):])
		x_test, y_test = (test_set[:, :-(self.settings.prediction_len)],
			test_set[:, -(self.settings.prediction_len):])

		# Reshape lists into Tensorflow format.
		x_train = numpy.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
		x_test = numpy.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
		y_train = numpy.reshape(y_train, (y_train.shape[0], y_train.shape[1], 1))
		y_test = numpy.reshape(y_test, (y_test.shape[0], y_test.shape[1], 1))
		
		return x_train, y_train, x_test, y_test


# Define DataSettings class to hold all data related settings
class DataSettings:
	def __init__(self, data_set):
		self.trim_leading_blank = data_set['trim_leading_blank']
		self.train_test_ratio = data_set['train_test_ratio']
		self.prediction_len = data_set['prediction_len']
		self.series_lenght = data_set['series_lenght']
		self.granularity = data_set['granularity']
		self.to_predict = data_set['to_predict']
		self.timeframe = data_set['timeframe']
		self.save_file = data_set['save_file']
		self.req_sym = data_set['req_sym']
		self.res_sym = data_set['res_sym']
