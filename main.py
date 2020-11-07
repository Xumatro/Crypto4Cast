import data, json, sys, graph, neural_net, numpy


# Open the keyfile to the read private API key.
with open('key.txt', 'r') as keyfile:
    api_key = keyfile.read()
    keyfile.close()

base_url = "https://min-api.cryptocompare.com/"

if __name__ == "__main__":
    # Get command line arguments.
    arguments = sys.argv

    history_data = data.get_history(base_url, api_key, coin="ETH")

    # If the retrieved data isn't a dictionary, it is our custom error message.
    # Valid data here should always be json which is represented in a dictionary.
    if type(history_data) != dict:
        sys.exit(history_data)

    cleaned_history_data = data.clean_history(history_data, trim=True, convert_date=True)
    history_dataframe = data.to_dataframe(cleaned_history_data)
    history_matrix = data.create_price_matrix(history_dataframe)
    normalized_history_matrix = data.normalize_matrix(history_matrix)
    x_tr, y_tr, x_te, y_te = data.split_test_train(normalized_history_matrix, train_size=0.85)

    # Write our organised and cleaned history data to a file.
    with open("coin_hist.json", "w") as btc_hist:
        json.dump(cleaned_history_data, btc_hist, indent=2)
        btc_hist.close()

    # If supplied argument was "train", train a new model.
    if len(arguments) > 1 and arguments[1] == "train":
        model = neural_net.new_rnn()
        neural_net.train(model, (x_tr, y_tr), (x_te, y_te), epochs=2, batchs=1, save=True)
    else:
        model = neural_net.load('predictor.h5')

        # Get data from last 30 entries in order to make a prediction.
        matrix = normalized_history_matrix[-1]
        matrix = numpy.array(matrix)
        matrix = numpy.reshape(matrix, (1, matrix.shape[0], 1))
        
        prediction = neural_net.predict(model, matrix, batchs=1)
        #final_pred = data.deserializer(prediction, history_dataframe[-30:], train_size=0.85, train_phase=False)

        # Deserialize our prediction.
        print("Tomorrow's marketvalue will be: $" + str((history_dataframe[-30] * (prediction + 1))[0, 0]))
