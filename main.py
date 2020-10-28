import data, json, sys, graph


# Open the keyfile to the read private API key.
with open('key.txt', 'r') as keyfile:
    api_key = keyfile.read()
    keyfile.close()
    
base_url = "https://min-api.cryptocompare.com/"

if __name__ == "__main__":
    history_data = data.get_history(base_url, api_key, coin="ETH")

    # If the retrieved data isn't a dictionary, it is our custom error message.
    # Valid data here should always be json which is represented in a dictionary.
    if type(history_data) != dict:
        sys.exit(history_data)

    history_data = data.clean_history(history_data, trim=True)

    graph.draw_from_json(history_data)

    # Write our organised and cleaned history data to a file.
    with open("coin_hist.json", "w") as btc_hist:
        json.dump(history_data, btc_hist, indent=2)
        btc_hist.close()
