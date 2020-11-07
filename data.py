import requests, json, datetime, pandas, numpy


# Retrieve the history data from our chosen API.
def get_history(base_url, api_key, base_currency, coin, timeframe, granularity):
    
    # Build the correct URL from given parameters.
    url = (base_url + "data/v2/histo" + granularity + "?fsym=" + coin + "&tsym="
        + base_currency + "&limit=" + str(timeframe-1) + "&api_key=" + api_key)

    response = requests.get(url).json()

    # If the data in "Response" field of the retrieved data is "Error", return a helpful error message.
    if response['Response'] == "Error":
        return ("Something went wrong here!\n" + response['Message'])

    return response

# Clean the history data by filtering out unneeded parts.
def clean_history(data, trim, convert_date):
    stop_trim = False
    start_index = 0

    # Loop through the data in the seccond "Data" field.
    for index, entry in enumerate(data["Data"]["Data"]):

        # If convert_date is set, change date info from UNIX timestamp to readable date format.
        if convert_date:
            entry['date'] = (datetime.datetime.fromtimestamp(entry['time'])
                .strftime('%Y-%m-%d'))
            del entry['time']

        # Add an "average" field to every entry of the history data.
        entry['average'] = (entry['high'] + entry['low']) / 2

        # Delete all unnecessary info, we will only need a datestamp and  an average price.
        unnecessary_data = (["conversionSymbol", "conversionType", "volumeto",
            "volumefrom", 'close', 'open'])

        for data_chunk in unnecessary_data:
            del entry[data_chunk]

        # If trim is set, set startindex to the index of the first nonzero value.
        if trim:
            if entry['high'] == 0 and not stop_trim:
                start_index = index + 1
            else:
                stop_trim = True

    if trim:
        # Return the data from the first nonzero point on.
        return data['Data']['Data'][start_index:]
        
    # Only return the usefull history data from the seccond "Data" field.
    return data['Data']['Data']

# Convert our json data into a pandas dataframe.
def to_dataframe(data):

    # Create a new pandas dataframe from the given data.
    data_frame = pandas.DataFrame(data, columns=['average', 'date'])

    # Convert the given date in string format to a pandas datetime.
    data_frame['date'] = pandas.to_datetime(data_frame['date'], format='%Y-%m-%d')

    # Group our data by date.
    return data_frame.groupby('date').mean()['average']

# Convert our data to a series of nested lists where every list contains data from 30 entries.
def create_price_matrix(dataframe, seq_len):
    matrix = []

    # Loop over data in chunks of "seq_len" and add a sublist to the price matrix.
    for index in range(0, len(dataframe) - (seq_len + 1)):
        matrix.append(dataframe[index:(index + seq_len)])

    return matrix

# Normalize the price matrix to reflect percent change from starting point.
def normalize_matrix(matrix):
    normalized_matrix = []

    # Loop over price matrix and get the sublists.
    for sublist in matrix:
        # Calculate the percent change of the entry compared to the first entry in the sublist.
        normalized_matrix.append([((float(price) / float(sublist[0])) - 1.0) for price in sublist])

    return normalized_matrix


# Split the price matrix into test and train datasets.
def split_test_train(matrix, train_size):
    matrix = numpy.array(matrix)

    # Define spliting point base on "train_size".
    split_point = int(round(train_size * len(matrix)))

    # Set train dataset to everything up to "split_point".
    train_set = matrix[:split_point, :]

    # Remove last entry from "x_" lists, and everything but last the last entry from "y_" lists.
    x_train, y_train = train_set[:split_point, :-1], train_set[:split_point, -1]
    x_test, y_test = matrix[split_point:,:-1], matrix[split_point:,-1]

    # Reshape lists into tensorflow format.
    x_train = numpy.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = numpy.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    return x_train, y_train, x_test, y_test
