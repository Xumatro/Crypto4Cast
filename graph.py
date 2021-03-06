from matplotlib import pyplot

# Define grapher class to hold grapher and methods
class Grapher:
	def __init__(self, graph_set):
		self.settings = GraphSettings(graph_set)

	# Plot and save graph from data
	def plot(self, data):

		# Is lenght isn't 'all', use the last 'lenght' of data
		if self.settings.data_lenght != "all":
			data = data[-self.settings.data_lenght:]
		
		# Generate x axis (time) values, counting down from len(data)
		data_x = [*range(-len(data)+1, 1)]
		data_y = [value for value in data]

		# Set dark theme
		if self.settings.dark_mode:
			pyplot.style.use('dark_background')

		# Set title, labels and grid
		pyplot.title("Value of BTC", color="#999999")
		pyplot.xlabel("Time (Days)", color="#999999")
		pyplot.ylabel("Value (USD)", color="#999999")
		pyplot.grid(self.settings.grid, color="#999999")

		# Plot and save figure
		pyplot.plot(data_x, data_y, color="#02dd3c")
		pyplot.savefig(self.settings.save_file, dpi=self.settings.dpi)


# Define GraphSettings class to hold all graph related settings
class GraphSettings:
	def __init__(self, graph_set):
		self.data_lenght = graph_set['data_lenght']
		self.save_file = graph_set['save_file']
		self.dark_mode = graph_set['dark_mode']
		self.grid = graph_set['show_grid']
		self.dpi = graph_set['DPI']