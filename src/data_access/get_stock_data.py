from dotenv import load_dotenv
import pandas as pd
import requests
import os
from io import StringIO

class GetStockData:
    def __init__(self):
        load_dotenv(dotenv_path=".env")
        self.stock_base_url = os.getenv("URL_STOCK_API")
    
    def get_stock(self):
        response = requests.get(f'{self.stock_base_url}')
        data = response.text
        df = pd.read_csv(StringIO(data), sep=";")
        df['nom_municipio'] = df['nom_municipio'].str.strip()
        df['nom_municipio'] = df['nom_municipio'].str.split('-', expand=True)[0]
        return df

