
import configparser
import pandas as pd
from api_method import AlphaVantageAPI, TickerInterval, TreasuryMaturity
import statsmodels.api as sm

URL = "https://www.alphavantage.co/query"


def fetch_risk_free_data(api: AlphaVantageAPI, maturity: TreasuryMaturity, interval: TickerInterval = TickerInterval.MONTHLY):
    df = api.fetch_function_data(
        function="TREASURY_YIELD",
        json_data_name="data",
        maturity=maturity.value,
        interval=interval.value
    ).T

    df = df.rename(columns={"value": "Treasury Yield"})
    df = df.set_index('date')
    df.index = pd.to_datetime(df.index)
    df = df.sort_index().astype(float)
    df /= 100

    return df


def main():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    API_KEY = config['AlphaVantage']['api_key']

    api = AlphaVantageAPI(API_KEY)

    risk_free_data = fetch_risk_free_data(api, TreasuryMaturity.THREE_MONTH)
    risk_free_data = (1 + risk_free_data)**(1/3) - 1  # Convert to monthly rate
    risk_free_data.index = risk_free_data.index.to_period('M')

    FACTORS_SYMBOLS = {
        "US Market": "SPY",
        "Commodities": "DBC",
        "Emerging Markets": "EEM",

    }

    factors_data = {}
    for factor, symbol in FACTORS_SYMBOLS.items():
        df = api.fetch_ticker_data(ticker=symbol)
        df.index = df.index.to_period('M')
        factors_data[factor] = df

    ASSET_TICKER = "BP"

    asset_data = api.fetch_ticker_data(ticker=ASSET_TICKER)
    asset_data.index = asset_data.index.to_period('M')

    close_prices = asset_data["Close"].rename(ASSET_TICKER).to_frame()
    for factor, df in factors_data.items():
        close = df["Close"].rename(factor)
        close_prices = close_prices.join(close, how='inner')

    returns = close_prices.pct_change().dropna()
    returns = returns.join(risk_free_data["Treasury Yield"], how='inner')

    risk_free_returns = returns['Treasury Yield'].values

    X = returns[factors_data.keys()].subtract(risk_free_returns, axis=0)
    X = sm.add_constant(X)
    y = returns[ASSET_TICKER] - risk_free_returns

    model = sm.OLS(y, X).fit()
    print(model.summary())


if __name__ == "__main__":
    main()
