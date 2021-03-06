import requests, data


# Define API class to hold API and methods
class API:
	def __init__(self, api_set):
		self.settings = APISettings(api_set)

	# Retreive history data from specified API
	def get_history_data(self, data_set):

		# Use appropriate settings for data
		data_set = data.DataSettings(data_set)

		# Build up URL from components
		url = (self.settings.base_url + "data/v2/histo" + data_set.granularity
			+ "?fsym=" + data_set.req_sym + "&tsym="
			+ data_set.res_sym + "&limit=" + str(data_set.timeframe - 1)
			+ "&e=" + self.settings.exchange + "&extraParams=Crypto4Cast"
			+ "&api_key=" + str(self.settings.api_key))

		response = requests.get(url).json()

		if response['Response'] == "Error":
			return ("Failure retrieving data!\n" + response['Message']), None

		# Build Data object from retreived data, and return it
		return "Succes!", data.Data(response=response, data_set=data_set)


# Define APISettings class to hold all API related settings
class APISettings:
	def __init__(self, api_set):
		self.base_url = api_set['base_url']
		self.exchange = api_set['exchange']

		with open(api_set['key_file'], 'r') as key_file:
			self.api_key = key_file.read()
