# Volatility Equalizer
Pick a set of instruments based on their `tickers` and provide the `capital` to be invested in this pool of instruments.
The script will then suggest how to apportion this amount of capital based
The aim is to aim equal units of volatility across all stocks. Otherwise, the most volatile of the bunch will dictate the whole portfolio.

## Installation
Before running the script, the necessary packages must be installed by first going to the root directory and running 
```bash
python -m pip install . -r reqiurements.txt
```
## Running
Then the following code can be used to run the script.
```bash
python vol_equalizer.py \
    --tickers BTC-USD,SOL-USD,ETH-USD,ADA-USD \
    --capital 1000 \
    --plot
```
## Implementation
Below, a brief explanation of how the code works is given.
```python

    # Get historical daily crypto prices using yahoo finance
    crypto = yf.download(tickers, start='2023-01-01', interval='1d')
    df_crypto = pd.DataFrame(crypto.Close)
    
    # Convert to log-space. Typically done in finance due to nice properties
    df_crypto_ret = df_crypto.apply(np.log).diff()
    
    # Take standard deviation (volatility) of the daily prices
    df_crypto_vol = df_crypto_ret.std()
    
    # The reciprocal of the volatility will give the ratio of the stake to be invested
    df_vol_factor = (1 / df_crypto_vol)
    
    # Normalise the ratios and scale by the capital
    position = df_vol_factor.div(df_vol_factor.sum()).mul(capital)

```
