from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.io as pio
import json

# default theme for Plotly
pio.templates.default = "simple_white"

try:
    geogson = json.load(open('maps/brasil_estados.json', encoding='utf-8'))
except FileNotFoundError:
    print("Erro: O arquivo 'brasil_estados.json' não foi encontrado. Verifique o caminho.")
    geogson = {"type": "FeatureCollection", "features": []}


# Load the data for the map
try:
    df = pd.read_csv('data/test_BR_states.csv')
    df.columns = ['state', 'Nvalue'] # Garante que as colunas se chamem 'state' e 'Nvalue'
except FileNotFoundError:
    print("Erro: O arquivo 'test_BR_states.csv' não foi encontrado. Verifique o caminho.")
    # Crie um DataFrame de exemplo se o arquivo não for encontrado
    df = pd.DataFrame({'state': ['SP', 'RJ', 'MG'], 'Nvalue': [0.5, 0.7, 0.3]})


# Load the CSS data
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets) # Adicione __name__ aqui

app.layout = html.Div([
    html.H1("Dashboard de Estados do Brasil", style={'textAlign': 'center', 'fontSize': 36, 'margin-top': '20px'}),
    html.Div([
        dcc.Graph(figure={}, id='Map-final')
    ], style={'width': '80%', 'margin': 'auto', 'padding': '20px'}), # Centraliza o gráfico

    # Componente invisível para disparar o callback na carga inicial
    dcc.Store(id='initial-load-trigger', data='loaded')
])

@callback(
    Output(component_id='Map-final', component_property='figure'),
    Input(component_id='initial-load-trigger', component_property='data')
)
def update_graph(data):
    if geogson["features"]: 
        fig = px.choropleth(df, geojson=geogson,
                            locations='state', # Coluna no DataFrame com as abreviações dos estados
                            #featureidkey='Feature.id', # Caminho para o ID correspondente no GeoJSON.
                            color='Nvalue',
                            hover_name='state',
                            range_color=[0, 100], # Ajuste a faixa de cor se seus valores não são de 0 a 1
                            hover_data={'state': True, 'Nvalue': True}, # Mostra essas colunas no hover
                            scope='south america',
                            fitbounds="locations" # Ajusta o zoom para os locais fornecidos
                            )

        fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0} # Remove margens desnecessárias
        )
        return fig
    else:
        # Retorna um gráfico vazio ou uma mensagem de erro se o GeoJSON não foi carregado
        return px.scatter(title="Erro ao carregar o mapa. Verifique o arquivo GeoJSON.")


if __name__ == '__main__':
    app.run(debug=True) # Use run_server em vez de run