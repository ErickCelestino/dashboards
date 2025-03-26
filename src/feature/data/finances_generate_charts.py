import streamlit as st

class FinancesGenerateCharts:
    def __init__(self, data, currency):
        self.filtered_data = data 
        self.currency = currency
    
    def convert_currency(self, data, value):
        if value == 'USD' and self.currency != 'USD':
            return f"$ {data:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".")
        elif value == 'EUR' and self.currency != 'EUR':
            return f"€ {data:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            return f"R$ {data:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    def ajust_metric(self, value):
        if self.currency == value:
            return self.filtered_data['BRL'].loc[self.filtered_data.index.max()]
        else:
            return self.filtered_data[value].loc[self.filtered_data.index.max()]

    def generate_charts(self):

        
        return {
            "dolar_value": self.convert_currency(self.ajust_metric('USD'), 'USD'),
            "euro_value": self.convert_currency(self.ajust_metric('EUR'), 'EUR'),
        }