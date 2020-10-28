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
def clean_history(data, trim=False):
    stop_trim = False
    start_index = 0

    # Loop through the data in the seccond "Data" field.
    for index, entry in enumerate(data["Data"]["Data"]):

        # Change date info from UNIX timestamp to readable date format.
        entry['date'] = (datetime.datetime.fromtimestamp(entry['time'])
            .strftime('%Y-%m-%d'))

        # Add an "average" field to every entry of the history data.
        entry['average'] = (entry['high'] + entry['low']) / 2

        # Delete unnecessary info including "time" field, we replaced it with "date".
        del entry['time']
        del entry["volumefrom"]
        del entry["volumeto"]
        del entry["conversionType"]
        del entry["conversionSymbol"]

        # If trimming is turned on, set startindex to the index of the first nonzero value.
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

    