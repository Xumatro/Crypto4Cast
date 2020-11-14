# CryptoPredix
> ***Predict the future trajectory of cryptocurrencies***
<br/><br/>

### How to use
#### Dependencies:
- json
- requests
- pandas
- keras
- tensorflow
- silence_tensorflow (*optional*)

These can be installed by running:
`$ pip install {dependency}`
<br/><br/>

#### Execution:
This project can be ran in training or prediction mode.

- Prediction mode:
`$ python3 main.py`
- Training mode:
`$ python3 main.py train`
<br/><br/>


### Settings
 All settings can be changed in `settings.json`
 
#### General:
In here all general settings can be changed
<br/><br/>

- `base_url` and `api_key` are api settings
- `base_currency` is the fiat currency, example: `USD`
- `coin` is the coin you want to predict, example: `BTC`
- `timeframe` is the number of entries to return
- `granularity` is the lenght of a single entry, example: `day`
- `conv_date` whether to convert the UNIX timestampt to readable date format
- `trim` cut leading whitespaces from returned data

