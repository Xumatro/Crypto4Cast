import data, json, sys, graph, neural_net, numpy

# Read all settings from "settings.json" file for easy acces.
with open('settings/settings.json', 'r') as settings:
    settings = json.loads(settings.read())
    general_set = settings['general']
    rnn_set = settings['neural_net']
    data_set = settings['data']
    graph_set = settings['graph']

# Open the keyfile to the read private API key.
with open(general_set['keyfile'], 'r') as keyfile:
    api_key = keyfile.read()

if __name__ == "__main__":
    # Get command line arguments.
    arguments = sys.argv

    history_data = data.get_history(base_url=general_set['base_url'], api_key=api_key, 
        base_currency=general_set['base_currency'], coin=general_set['coin'],
        timeframe=general_set['timeframe'], granularity=general_set['granularity'])

    # If the retrieved data isn't a dictionary, it is our custom error message.
    # Valid data here should always be json which is represented in a dictionary.
    if type(history_data) != dict:
        sys.exit(history_data)

    cleaned_history_data = data.clean_history(data=history_data,
        convert_date=general_set['conv_date'], trim=general_set['trim'])

    history_dataframe = data.to_dataframe(data=cleaned_history_data)

    history_matrix = data.create_price_matrix(dataframe=history_dataframe,
        seq_len=data_set['sequential_len'])

    normalized_history_matrix = data.normalize_matrix(matrix=history_matrix)

    x_tr, y_tr, x_te, y_te = data.split_test_train(matrix=normalized_history_matrix,
        train_size=data_set['train_size'])

    # Write our organised and cleaned history data to a file.
    with open(data_set['hist_file'], "w") as hist_file:
        json.dump(cleaned_history_data, hist_file, indent=2)

    # If supplied argument was "train", train a new model.
    if len(arguments) > 1 and arguments[1] == "train":
        model = neural_net.new_rnn(layers=rnn_set['layers'], seq_len=data_set['sequential_len'],
            optimizer=rnn_set['optimizer'], loss_function=rnn_set['loss_function'])

        # Print a description of the model.
        print(model.summary())

        model, loss = neural_net.train(model, (x_tr, y_tr), (x_te, y_te), epochs=rnn_set['epochs'],
            batchs=rnn_set['batch_size'])
        
        # If "save" is set, save the trained model for later use, also save a json file with the model architecture.
        if rnn_set['save']:
            model.save(rnn_set['rnn_trained_file'])
            with open(rnn_set['rnn_arch_file'], 'w') as model_file:
                json_model = json.loads(model.to_json())
                json.dump(json_model, model_file, indent=2)

        print("\nModels final loss was: " + str(loss))

    else:
        model = neural_net.load(filename=rnn_set['rnn_trained_file'], optimizer=rnn_set['optimizer'],
            loss_function=rnn_set['loss_function'])

        # Get data from last "seqential_len" entries in order to make a prediction.
        matrix = normalized_history_matrix[-1]
        matrix = numpy.array(matrix)
        matrix = numpy.reshape(matrix, (1, matrix.shape[0], 1))
        
        prediction = neural_net.predict(model=model, data=matrix, batchs=rnn_set['batch_size'])

        # Deserialize our prediction.
        print("Tomorrow's marketvalue will be: $" + str((history_dataframe[-data_set['sequential_len']]
            * (prediction + 1))[0, 0]))

        graph.plot_from_json(data=cleaned_history_data, show_grid=graph_set['show_grid'],
            filename=graph_set['graph_file'], dpi=graph_set['dpi'])
