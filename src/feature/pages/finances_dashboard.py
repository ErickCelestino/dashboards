import datetime
import streamlit as st
import plotly.express as px
from data_access.get_finances_data import GetFinancesData
from feature.data.finances_generate_charts import FinancesGenerateCharts

class FinancesDashboard:
    def __init__(self):
        self.get_initial_data()
    
    def get_initial_data(self):
        self.today = datetime.date.today()
        self.three_months_ago = self.today - datetime.timedelta(days=90)
        self.finances_data = GetFinancesData()
        self.currency = 'BRL' 

        self.last_fetched_start = self.three_months_ago
        self.last_fetched_end = self.today
        self.last_fetched_currency = self.currency
        self.currency_data = self.finances_data.data_currency_names().to_list()

        self.data = None  
        self.fetch_data()

    def ajust_metric_title(self, value, currency):
        if self.currency == 'BRL' or self.currency != currency:
            return value
        else:
            return 'Cotação Real'

    def fetch_data(self):
        """Fetches new data from the API with the selected dates and currency."""
        self.data = self.finances_data.data_by_financial_dates(
            self.last_fetched_start, self.last_fetched_end, { "base": self.last_fetched_currency }
        )

    def setup_filters(self):
        """Configure filters in the Streamlit sidebar."""
        st.sidebar.title('Filtros')
        self.start_date = st.sidebar.date_input("Data Inicial", value=self.last_fetched_start)
        self.end_date = st.sidebar.date_input("Data Final", value=self.last_fetched_end)
        default_index = self.currency_data.index('BRL') 
        self.currency = st.sidebar.selectbox("Moeda", self.currency_data, index=default_index)

    def apply_filters(self):
        """Check whether you need to fetch new data or just apply local filters."""
        if (self.start_date != self.last_fetched_start or 
            self.end_date != self.last_fetched_end or 
            self.currency != self.last_fetched_currency):

            self.last_fetched_start = self.start_date
            self.last_fetched_end = self.end_date
            self.last_fetched_currency = self.currency

            self.fetch_data()
        self.filtered_data = self.data.copy()
    
    def render_layout(self):
        """Renders the filtered data on the screen."""
        charts = FinancesGenerateCharts(self.filtered_data, self.currency).generate_charts()
        
        tabHistory = st.tabs(['Histórico'])[0]
        with tabHistory:
            col_metric1, col_metric2, col_metric3 = st.columns(3)
            with col_metric1:
                st.metric(self.ajust_metric_title('Dólar (USD)', 'USD'), charts['dolar_value'])
            with col_metric2:
                st.metric(self.ajust_metric_title('Euro (EUR)', 'EUR'), charts['euro_value'])
            with col_metric3:
                st.markdown(charts['last_date'], unsafe_allow_html=True)

            st.plotly_chart(charts['fig_evolution_price_day'], use_container_width=True)

            #columnLeft, columnRight = st.columns(2) .update_layout(autosize=True)

        st.dataframe(self.filtered_data, use_container_width=True)

    def render_page(self):
        """Executes the dashboard page logic."""
        st.title('COTAÇÕES FINANCEIRAS')
        self.setup_filters()
        self.apply_filters()
        self.render_layout()
