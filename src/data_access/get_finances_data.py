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
        df = pd.DataFrame.from_dict(data['rates'], orient="index").reset_index()
        #df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
        #df.index =  df.index.strftime('%d/%m/%Y')
        df['DiaMes'] = pd.to_datetime(df.index).strftime('%d/%m')
        id_vars = ['DiaMes', 'index']
        value_vars = [col for col in df.columns if col not in id_vars]
        df = pd.melt(
            df,
            id_vars= id_vars,
            value_vars= value_vars,
            var_name='Moeda',
            value_name="Valor"
        )
        return df

    def data_currency_names(self):
        response = requests.get(f'{self.finance_base_url}/currencies')
        data = response.json()
        df = pd.DataFrame.from_dict(data, orient="index")
        return df.index
