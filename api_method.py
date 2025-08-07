import requests
import pandas as pd
from enum import Enum


class TickerInterval(Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"


class TreasuryMaturity(Enum):
    THREE_MONTH = "3month"
    TWO_YEAR = "2year"
    FIVE_YEAR = "5year"
    SEVEN_YEAR = "7year"
    TEN_YEAR = "10year"
    THIRTY_YEAR = "30year"


class DataInterval(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class AlphaVantageAPI:
    URL = "https://www.alphavantage.co/query"
    RENAMES = {
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume",
    }

    def __init__(self, api_key: str):
        self.api_key = api_key

    def fetch_function_data(self, function: str, json_data_name: str, **kwargs):
        params = {
            "function": function,
            **kwargs,
            "apikey": self.api_key
        }
        response = requests.get(self.URL, params=params)
        data = response.json()
        print(data['Error Message']) if 'Error Message' in data else None
        print(data['Information']) if 'Information' in data else None

        if json_data_name in data:
            df = pd.DataFrame(data[json_data_name]).T
            return df
        else:
            raise ValueError(
                f"Data for {json_data_name} not found in the response.")

    def fetch_ticker_data(self, ticker: str, interval: TickerInterval = TickerInterval.MONTHLY):
        df = self.fetch_function_data(
            function=f"TIME_SERIES_{interval.value.upper()}",
            json_data_name=f"{interval.value.capitalize()} Time Series",
            symbol=ticker,
            outputsize="full"
        )
        df = df.rename(columns=self.RENAMES)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index().astype(float)
        return df
