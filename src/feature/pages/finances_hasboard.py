import datetime
import streamlit as st
import pandas as pd
from data_access.get_finances_data import GetFinancesData

class FinancesDashboard:
    def __init__(self):
        self.get_initial_data()
    
    def get_initial_data(self):
        self.today = datetime.date.today()
        self.three_months_ago = self.today - datetime.timedelta(days=90)
        self.finances_data = GetFinancesData()
        self.data =  self.finances_data.data_by_financial_dates(self.three_months_ago, self.today, 'BRL')

    def setup_filters(self):
        st.sidebar.title('Filtros')
        self.start_date = st.sidebar.date_input("Data Inicial", value=self.today)
        self.end_date = st.sidebar.date_input("Data Final", value=self.three_months_ago)

    def render_page(self):
        st.title('COTAÇÕES FINANCEIRAS')
        self.setup_filters()