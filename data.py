import requests, json, datetime


def get_history(base_url, api_key, coin="BTT", base_currency="EUR", granularity="day", timebase="1825"):
    url = (base_url + "data/v2/histo" + granularity + "?fsym=" + coin + "&tsym="
        + base_currency + "&limit=" + timebase + "&api_key=" + api_key)

    response = requests.get(url).json()
    if response['Response'] == "Error":
        return ("Something went wrong here!\n" + response['Message'])

    return response

def clean_data(history_data):
    for day in history_data["Data"]["Data"]:
        day['date'] = (datetime.datetime.fromtimestamp(day['time'])
            .strftime('%Y-%m-%d'))

        del day['time']
        del day["volumefrom"]
        del day["volumeto"]
        del day["conversionType"]
        del day["conversionSymbol"]

    return history_data