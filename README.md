# ***Crypto4Cast*** [![](https://tokei.rs/b1/github/Xumatro/Crypto4Cast)](https://github.com/Aaronepower/tokei) [![](https://img.shields.io/badge/license-MIT-brightgreen)](https://github.com/Xumatro/Crypto4Cast/blob/main/LICENSE)
> ***Predict the future trajectory of cryptocurrencies***
<br/><br/>

---

## **How to use:**
### Dependencies
- json
- requests
- pandas
- keras
- tensorflow
- silence_tensorflow (*optional*)

These can be installed by running: `$ pip install {dependency}`
<br/><br/>

### Execution
This project can be ran in training or prediction mode.

- Prediction mode: `$ python3 main.py`
- Training mode: `$ python3 main.py train`
<br/><br/>

---

## **Settings**
 All settings can be changed in `settings.json`
<br/><br/>
 
## `General`
In this field, all general settings can be changed

- `base_url` and `api_key` are api settings
- `base_currency` is the fiat currency, example: `USD`
- `coin` is the coin you want to predict, example: `BTC`
- `timeframe` is the number of entries to return
- `granularity` is the lenght of a single entry, example: `day`
- `conv_date` whether to convert the UNIX timestampt to readable date format
- `trim` cut leading whitespaces from returned data
<br/><br/>

## `Data`
In this field, all data specific settings can be changed

- `sequential_len` is the number of entries to group the data in
- `train_size` is the ration between the train and test dataset
- `hist_file` is the filename of the file to save the data to
<br/><br/>

## `Graph`
In this field, all graphing specific settings can be changed

- `graph_file` is the filename to save the graph to
- `show_grid` whether to draw gridlines in the grapbh
- `dpi` the dpi setting for the image file
<br/><br/>

## `neural_net`
In this field, all the neural net specific settings can be changed

- `rnn_file` is the filename to save the trained model to
- `batch_size` is the number of chunks to split the data between for the network
- `epochs` is the number of training cycles
- `save` whether to save the model after training or not
- `optimizer` the optimizer algorithm to use while training
- `loss_function` the function to estimate the loss while training
- `layers` array of layers to build the network from
	- `type` the type of neurons layer consists of
	- `units` the number of neurons in this layer
	- `activation` the activation function to use in the neurons
	- `alpha` negative slope coefficient, only usefull when `activation` is `leaky_relu`
	- `return_seq` whether the layer should return a sequence of not
