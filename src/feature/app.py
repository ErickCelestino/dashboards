import streamlit as st
from feature.pages.finances_dashboard import FinancesDashboard

class App:
    def __init__(self):
        st.set_page_config(page_title="Portifólio de Dados", layout="wide")
        self.pages = {
            "Página Principal": self.render_main_page,
            "Dados Financeiros": FinancesDashboard().render_page
        }

    def render_main_page(self):
        st.title('DASHBOARDS PORTIFÓLIO DE DADOS:rocket:')
        st.write("Escolha uma página no menu lateral.")
    
    def run(self):
        page = st.sidebar.selectbox("Escolha a página", list(self.pages.keys()))
        self.pages[page]()
