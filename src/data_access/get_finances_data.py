import os
from dotenv import load_dotenv
import requests
import pandas as pd
from datetime import date

class GetFinancesData:
    def __init__(self):
        load_dotenv(dotenv_path=".env")
        self.finance_base_url = os.getenv("URL_FINANCE_API")
    
    def today_data_finance(self, base):
        response = requests.get(f'{self.finance_base_url}/{date.today()}', params=base)
        data = pd.DataFrame.from_dict(response.json())
        return data
    
    def data_by_financial_dates(self, startDate, endDate, base):
        response = requests.get(f'{self.finance_base_url}/{startDate}..{endDate}', params=base)
        data = pd.DataFrame.from_dict(response.json())
        return data
