import data, json, sys


with open('key.txt', 'r') as keyfile:
    api_key = keyfile.read()
    
base_url = "https://min-api.cryptocompare.com/"

if __name__ == "__main__":
    history_data = data.get_history(base_url, api_key)

    if type(history_data) == str:
        sys.exit(history_data)

    history_data = data.clean_data(history_data)

    with open("btc_hist.json", "w") as btc_hist:
        json.dump(history_data['Data']["Data"], btc_hist, indent=2)
