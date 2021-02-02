import json, sys, numpy, api, data, rnn, graph


# Take API and data settings and retreive necessary data
def get_data(api, json_settings):
    # Print progress while gathering and transforming data

    print("Retreiving history data...", end=" ")
    result, data = api.get_history_data(data_set=json_settings['Data'])

    # If returned result isn't succes, exit with errror
    if result != "Succes!":
        sys.exit(result)
    print("done!")

    print("Cleaning history data...", end=" ")
    data.clean_history()
    print("done!")

    print("Converting JSON data to Pandas DataFrame...", end=" ")
    data.create_data_frame()
    print("done!")

    print("Converting Pandas DataFrame to price matrix...", end=" ")
    data.create_price_matrix()
    print("done!")

    print("Normalizing price matrix...", end=" ")
    data.normalize_matrix()
    print("done!")

    print("Saving data for your viewing pleasure...", end=" ")
    # Write the organised and cleaned history data to a file
    with open(data.settings.save_file, "w") as hist_file:
        json.dump(data.history, hist_file, indent=3)

        grapher = graph.Grapher(json_settings['Graph'])
        grapher.plot(data.data_frame)
    print("done!")

    return data

# Train new model
def train(api, json_settings):
    print("Running in training mode.\n")

    data = get_data(api, json_settings)

    # Split data in train and test sets
    x_train, y_train, x_test, y_test = data.split_test_train()

    print("Building model...", end=" ")
    network = rnn.RNN(rnn_set=json_settings['RNN'],
        data_set=data.settings, trained=False)
    print("done!")
    print(network.model.summary())

    print("\nTraining model...")
    loss = network.train(train_data=(x_train, y_train), test_data=(x_test, y_test))
    print("Done!\n")

    return loss

# Predict prices with already trained model
def predict(api, json_settings):
    print("Running in prediction mode.\n")

    data = get_data(api, json_settings)

    # Load model from disk
    network = rnn.RNN(rnn_set=json_settings['RNN'],
        data_set=data.settings, trained=True)

    # Reshape price matrix so Tensorflow can work with it
    matrix = numpy.array(data.price_matrix[-1])
    matrix = numpy.reshape(matrix, (1, matrix.shape[0], 1))

    print("Predicting price(s)...", end=" ")
    predictions = network.predict(data=matrix)
    print("Done!\n")

    # Get start value of the series we fed to network
    start_value = data.data_frame[-data.settings.series_lenght]
    predictions = numpy.reshape(predictions, (predictions.shape[1]))

    # Serialize predictions by multiplying with start value
    return [(pred + 1) * start_value for pred in predictions]

# Print usage and help message
def print_help():
    print("Usage: python3 main.py [MODE]")
    print("\nAvailable modes:")

    print("-h   --help              Print this help message")
    print("-p   --predict           Predict price with trained model")
    print("-t   --train             Train the model with new data")

    print("\nYou can edit 'settings/settings.json' to change all parameters")
    print("Consult 'README.md' for an explanation of all the available parameters")


if __name__ == "__main__":

    # Read all settings from "settings.json" file for easy access.
    with open('settings/settings.json', 'r') as settings:
        json_settings = json.loads(settings.read())

    # Get command line arguments.
    arguments = sys.argv

    # Initalize API with appropriate settings
    api = api.API(api_set=json_settings['API'])

    # If additional arguments were given, run corresponding mode.
    # If not, print help message
    if len(arguments) == 2:
            mode = arguments[1]

            if mode == "--train" or mode == "-t":
                loss = train(api, json_settings)
                print("Final loss value: ", loss)
            elif mode == "predict" or mode == "-p":
                predictions = predict(api, json_settings)
                print("Future price(s): ", predictions)
            else:
                print_help()

    else:
        print_help()
