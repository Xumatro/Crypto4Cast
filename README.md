# ***Crypto4Cast***<br/>[![](https://tokei.rs/b1/github/Xumatro/Crypto4Cast)](https://github.com/Aaronepower/tokei) [![](https://img.shields.io/badge/license-MIT-brightgreen)](https://github.com/Xumatro/Crypto4Cast/blob/main/LICENSE)
> ***Predict the future trajectory of cryptocurrencies***
<br/><br/>

---

## **How to use:**
### Dependencies
- matplotlib
- requests
- pandas
- keras
- tensorflow
- silence_tensorflow (*optional*)*

These can be installed by running: `$ pip install {dependency}`.

Tensorflow does not yet support python 3.9 so it is reccomended to create a python virtual environment with python 3.8.

This can be done by running `$ python3.8 -m venv {environment name}` on Linux or Mac.
This will create a folder called `{environment name}`, you will need to actvate this environment by running `$ source env/bin/activate` on Linux or Mac.
Once activated you can install dependencies and run the program.

**If you choose not to install silence_tensorflow, you will need to edit 'rnn.py' and remove the first line.*
<br/><br/>

### Execution
This project can be ran either in training or prediction mode.

- Prediction mode: `$ python3 main.py -p`
- Training mode: `$ python3 main.py -t`
<br/><br/>

---

## **Settings**
 All settings can be changed in `settings/settings.json`
<br/><br/>
 
## `API`
In this field, all API specific settings can be changed

- `base_url` the base url of your API
- `key_file` the file where your API key is saved
<br/><br/>

## `Data`
In this field, all data specific settings can be changed

- `res_sym` is the symbol wou want to recieve the price in, example: `EUR`
- `req_sym` is the coin you want to predict, example: `BTC`
- `timeframe` is the number of entries to return
- `granularity` is the lenght of a single entry, example: `day`
- `trim_leading_blank` whether or not to cut leading whitespaces from returned data
- `series_lenght` is the number of entries to group the data in
- `train_test_ratio` is the ratio between the train and test dataset
- `prediction_len` the lenght of the series to predict, 1 would predict today's average
- `save_file` is the filename of the file to save the data to
<br/><br/>

## `Graph`
In this field, all graphing specific settings can be changed

- `DPI` is the PI of the image to be generated
- `save_file` is the filename to save the graph to
- `darm_mode` whether or not to use a dark theme
- `data_lenght` the lenght of the data series to use, use `all` to use the whole series
- `show_grid` whether to draw gridlines in the grapbh
<br/><br/>

## `RNN`
In this field, all the neural net specific settings can be changed

- `trained_file` is the filename to save the trained model to
- `arch_file` is the filename to save the architecture of the model to
- `loss_function` the function to estimate the loss while training
- `optimizer` the optimizer algorithm to use while training
- `batch_size` is the number of chunks to split the data between for the network
- `epochs` is the number of training cycles

- `layers` array of layers to build the network from
	- `type` the type of neurons layer consists of
	- `units` the number of neurons in this layer
	- `activation` the activation function to use in the neurons
	- `alpha` negative slope coefficient, only usefull when `activation` is `leaky_relu`
	- `return_seq` whether the layer should return a sequence of not
