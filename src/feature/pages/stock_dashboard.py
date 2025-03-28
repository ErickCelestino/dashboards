import streamlit as st
from data_access.get_stock_data import GetStockData

class StockDashboard:
    def __init__(self):
        self.get_initial_data()
    
    def get_initial_data(self):
        self.data = GetStockData().get_stock()
    
    def setup_filters(self):
        st.sidebar.title('Filtros')
        def generate_list(value):
            return ['TODOS'] + self.data[value].unique().tolist()

        def generate_sidebar(title, list):
            return st.sidebar.selectbox(title, list)

        species_warehouse_list = generate_list('dsc_especie_armazem')
        types_warehouse_list = generate_list('dsc_tipo_armazem')
        types_entities_list = generate_list('dsc_tipo_entidade')
        types_person_list = generate_list('dsc_tipo_pessoa')
        uf_list = generate_list('uf')

        self.species_warehouse = generate_sidebar('Especie de Armazem', species_warehouse_list)
        self.types_warehouse = generate_sidebar('Tipo de Armazem', types_warehouse_list)
        self.types_entities = generate_sidebar('Tipo de Entidade' ,types_entities_list)
        self.types_person = generate_sidebar('Tipo Pessoa' , types_person_list)
        self.uf = generate_sidebar('Estados', uf_list)
 
        if self.uf == 'TODOS':
            filtered_cities = generate_list('nom_municipio')
        else:
            filtered_cities = ['TODOS'] + self.data.loc[self.data['uf'] == self.uf, 'nom_municipio'].unique().tolist()

        self.cities = generate_sidebar('Municípios', filtered_cities)

    def render_layout(self):
        st.dataframe(self.data)

    def render_page(self):
        st.title('DADOS DE ESTOQUE')
        self.render_layout()
        self.setup_filters()
