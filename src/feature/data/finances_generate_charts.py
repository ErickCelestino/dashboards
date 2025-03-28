import plotly.express as px
import math

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
            
        max_idx = filtered['Data'].idxmax()
        return filtered.loc[max_idx]['Valor']
    
    def generate_data(self):
        moedas=['BRL', 'EUR', 'USD', 'GBP']
        last_month = self.filtered_data['Data'].max().month
        
        self.filtered_data = self.filtered_data.sort_values('Data')
        self.df_sample = self.filtered_data[self.filtered_data['Moeda'].isin(moedas)]
        df_last_month = self.filtered_data[self.filtered_data['Mes'] == last_month]

        valued_currency = self.filtered_data.groupby('Moeda')['Valor'].agg(['last']).reset_index()
        self.top_five_undervalued_currency = valued_currency.nlargest(5, "last")
        self.top_five_valued_currency = valued_currency.nsmallest(5, "last")

        self.week_average_currency = df_last_month.groupby(['Moeda', 'Mes', 'Semana'])['Valor'].mean().reset_index()
        self.top_five_average_valued_currency = (
            self.week_average_currency.groupby('Semana')
            .apply(lambda x: x.nsmallest(5, 'Valor'))
            .reset_index(drop=True)
        )
        self.top_five_average_undervalued_currency = (
            self.week_average_currency.groupby('Semana')
            .apply(lambda x: x.nlargest(5, 'Valor'))
            .reset_index(drop=True)
        )

    def generate_charts(self):
        self.generate_data()
        def create_line_chart(data, x, y, color, title, labels):
            return px.line(data, 
                           x=x, 
                           y=y, 
                           markers=True, 
                           range_y=[0, data[y].max()], 
                           color=color, line_dash=color, 
                           title=title, 
                           labels=labels)
        
        def create_bar_chart(data, x, y, title, yaxis_title, color=None, labels=None, orientation = 'v'):
            return px.bar(data, 
                          x=x, 
                          y=y, 
                          orientation=orientation, 
                          labels=labels, 
                          color=color, 
                          text_auto=True, 
                          title=title, 
                          range_y=[0, math.ceil(data[y].mean())], 
                          barmode='group').update_layout(yaxis_title=yaxis_title)


        return {
            "dolar_value": self.convert_currency(self.ajust_metric('USD'), 'USD'),
            "euro_value": self.convert_currency(self.ajust_metric('EUR'), 'EUR'),
            "last_date": f"""
                <div style="
                    padding: 8px;
                    border-radius: 5px;
                    text-align: center;
                    margin: 10px 0;
                ">
                    📅 <strong>Última atualização:</strong> {self.filtered_data['Data'].dt.strftime('%d/%m/%Y').iloc[-1]}
                </div>
                """,
            "fig_evolution_price_day": create_line_chart(
                self.df_sample, 
                x='DiaMes', 
                y='Valor', 
                color='Moeda',
                title='Evolução das Cotações por Dia/Mês', 
                labels={'Valor': 'Valor da Moeda', 'DiaMes': 'Dia/Mês'}
                ),
            "fig_top_five_undervalued_currency": create_bar_chart(
                self.top_five_undervalued_currency,
                x='Moeda',
                y='last',
                title='Top 5 Moedas mais desvalorizadas',
                yaxis_title='Preço'
            ),
            "fig_top_five_valued_currency": create_bar_chart(
                self.top_five_valued_currency,
                x='Moeda',
                y='last',
                title='Top 5 Moedas mais valorizadas',
                yaxis_title='Preço'
            ),
            "fig_top_five_average_valued_currency": create_bar_chart(
                self.top_five_average_valued_currency,
                x='Valor',
                y='Semana',
                color='Moeda',
                title='Top 5 Média das moedas mais valorizadas Mês Atual',
                labels={'Valor': 'Média do Valor', 'Semana': 'Semana'},
                orientation='h',
                yaxis_title='Semana'
            ),
            "fig_top_five_average_undervalued_currency": create_bar_chart(
                self.top_five_average_undervalued_currency,
                x='Valor',
                y='Semana',
                color='Moeda',
                title='Top 5 Média das moedas mais desvalorizadas Mês Atual',
                labels={'Valor': 'Média do Valor', 'Semana': 'Semana'},
                orientation='h',
                yaxis_title='Semana'
            )
        }