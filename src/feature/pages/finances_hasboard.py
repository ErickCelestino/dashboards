import datetime
import streamlit as st
from data_access.get_finances_data import GetFinancesData

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

        self.data = None  
        self.fetch_data()

    def fetch_data(self):
        """Busca novos dados da API com as datas e moeda selecionadas."""
        self.data = self.finances_data.data_by_financial_dates(
            self.last_fetched_start, self.last_fetched_end, self.last_fetched_currency
        )

    def setup_filters(self):
        """Configura os filtros na sidebar do Streamlit."""
        st.sidebar.title('Filtros')
        self.start_date = st.sidebar.date_input("Data Inicial", value=self.last_fetched_start)
        self.end_date = st.sidebar.date_input("Data Final", value=self.last_fetched_end)
        self.currency = st.sidebar.selectbox("Moeda", ['BRL', 'USD', 'EUR'], index=0)

    def apply_filters(self):
        """Verifica se precisa buscar novos dados ou apenas aplicar filtros locais."""
        if (self.start_date != self.last_fetched_start or 
            self.end_date != self.last_fetched_end or 
            self.currency != self.last_fetched_currency):

            self.last_fetched_start = self.start_date
            self.last_fetched_end = self.end_date
            self.last_fetched_currency = self.currency

            self.fetch_data()

        self.filtered_data = self.data.copy()
    
    def render_layout(self):
        """Renderiza os dados filtrados na tela."""
        st.dataframe(self.filtered_data, use_container_width=True)

    def render_page(self):
        """Executa a lógica da página do dashboard."""
        st.title('COTAÇÕES FINANCEIRAS')
        self.setup_filters()
        self.apply_filters()
        self.render_layout()
