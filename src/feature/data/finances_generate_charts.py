import pandas as pd

class FinancesGenerateCharts:
    def __init__(self, data, currency):
        self.filtered_data = data 
        self.currency = currency
    
    def convert_currency(self, data, value):
        if not isinstance(data, (int, float)):
            return ""
            
        if value == 'USD' and self.currency != 'USD':
            return f"$ {data:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".")
        elif value == 'EUR' and self.currency != 'EUR':
            return f"€ {data:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            return f"R$ {data:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    def ajust_metric(self, value):
        if self.currency == value:
            filtered = self.filtered_data[self.filtered_data['Moeda'] == 'BRL']
        else:
            filtered = self.filtered_data[self.filtered_data['Moeda'] == value]
        
        if filtered.empty:
            return 0
            
        max_idx = filtered['index'].idxmax()
        return filtered.loc[max_idx]['Valor']

    def generate_charts(self):
        return {
            "dolar_value": self.convert_currency(self.ajust_metric('USD'), 'USD'),
            "euro_value": self.convert_currency(self.ajust_metric('EUR'), 'EUR')
        }