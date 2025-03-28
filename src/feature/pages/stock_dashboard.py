import streamlit as st
from data_access.get_stock_data import GetStockData

class StockDashboard:
    def __init__(self):
        self.get_initial_data()
    
    def get_initial_data(self):
        self.data = GetStockData().get_stock()
    
    def render_layout(self):
        st.dataframe(self.data)

    def render_page(self):
        st.title('DADOS DE ESTOQUE')
        self.render_layout()
