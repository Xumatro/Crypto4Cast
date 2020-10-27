import requests, json, datetime


# Retrieve the history data from our chosen API.
def get_history(base_url, api_key, coin="BTC", base_currency="USD", granularity="day", timescale="1825"):

    # Build the correct URL from given parameters.
    url = (base_url + "data/v2/histo" + granularity + "?fsym=" + coin + "&tsym="
        + base_currency + "&limit=" + timescale + "&api_key=" + api_key)

    response = requests.get(url).json()

    # If the "Response" key in the retrieved data is "Error", return a helpful error message.
    if response['Response'] == "Error":
        return ("Something went wrong here!\n" + response['Message'])

    return response

# Clean the history data by filtering out unneeded parts.
def clean_data(history_data):

    # Loop through the data in the seccond "Data" field.
    for day in history_data["Data"]["Data"]:

        # Change date info from UNIX timestamp to readable date format.
        day['date'] = (datetime.datetime.fromtimestamp(day['time'])
            .strftime('%Y-%m-%d'))

        # Add an "average" field to every day of the history data.
        day['average'] = (day['high'] + day['low']) / 2

        # Delete unnecessary info including "time" field, we replaced it with "date".
        del day['time']
        del day["volumefrom"]
        del day["volumeto"]
        del day["conversionType"]
        del day["conversionSymbol"]

    # Only return the usefull data from the seccond "Data" field.
    return history_data['Data']['Data']