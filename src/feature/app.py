import streamlit as st
from feature.pages.finances_hasboard import FinancesDashboard

class App:
    def __init__(self):
        st.set_page_config(page_title="Analises Portifólio", layout="wide")
        self.pages = {
            "Página Principal": self.render_main_page,
            "Dados Financeiros": FinancesDashboard().render_page
        }

    def render_main_page(self):
        st.title('DASHBOARDS PORTIFÓLIO :rocket:')
        st.write("Escolha uma página no menu lateral.")
    
    def run(self):
        page = st.sidebar.selectbox("Escolha a página", list(self.pages.keys()))
        self.pages[page]()
