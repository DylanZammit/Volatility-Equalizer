import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main(
    tickers: list[str],
    capital: int = 1,
    plot: bool = True,
) -> pd.Series:

    crypto = yf.download(tickers, start='2023-01-01', interval='1d')

    df_crypto = pd.DataFrame(crypto.Close)
    df_crypto_ret = df_crypto.apply(np.log).diff()
    df_crypto_vol = df_crypto_ret.std()

    df_vol_factor = (1 / df_crypto_vol)

    if plot:
        df_crypto_vol_scaled = df_crypto_ret.div(df_crypto_vol)
        df_roi = df_crypto_vol_scaled.mul(capital)
        df_roi['AUM'] = df_roi.sum(axis=1)

        fig, ax = plt.subplots(2, 2)

        df_crypto.plot(title='Raw Price', ax=ax[0, 0])
        df_crypto_ret.cumsum().plot(title='Raw Returns', ax=ax[0, 1])
        df_crypto_vol_scaled.cumsum().plot(title='Vol Scaled Returns', ax=ax[1, 0])

        df_roi.cumsum().plot(title='Vol Scaled ROI', ax=ax[1, 1])

        plt.show()

    position = df_vol_factor.div(df_vol_factor.sum()).mul(capital)
    return position


if __name__ == '__main__':
    """
    example tickers: BTC-USD,SOL-USD,ETH-USD,ADA-USD
    """
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--plot", help="Plot Graphs", action='store_true')
    parser.add_argument("--tickers", help="Comma-separated tickers", type=str, required=True)
    parser.add_argument("--capital", help="capital to invest", type=int, default=1)
    args = parser.parse_args()
    out = main(
        tickers=args.tickers.split(','),
        capital=args.capital,
        plot=args.plot,
    )

    print(out)
