import os
from dotenv import load_dotenv
import requests
import pandas as pd
from datetime import date

class GetFinancesData:
    def __init__(self):
        load_dotenv(dotenv_path=".env")
        self.finance_base_url = os.getenv("URL_FINANCE_API")

    def data_by_financial_dates(self, startDate, endDate, params):
        response = requests.get(f'{self.finance_base_url}/{startDate}..{endDate}', params=params)
        data = response.json()
        df = pd.DataFrame.from_dict(data['rates'], orient="index")
        df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
        df.index =  df.index.strftime('%d/%m/%Y')
        return df
