# ESTRUTURA DO DASHBOARD
# --- mapa do Brasil com estados (parte esquerda completa);
# --- gráfico de linhas com dados de COVID-19 por estado (parte direita superior);
# --- gráfico de barras com dados de COVID-19 acumulados por estado (parte direita inferior);

from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.io as pio
import json

pio.templates.default = "simple_white"

# Import GeoJSON data
try:
    geogson = json.load(open('maps/brasil_estados.json', encoding='utf-8'))
except FileNotFoundError:
    print("Erro: O arquivo 'brasil_estados.json' não foi encontrado. Verifique o caminho.")
    geogson = {"type": "FeatureCollection", "features": []}

# Load the data for the dashboard
try:
    df = pd.read_csv('data/COVID19_BRAZIL_2020.csv')
    # Convert date column to datetime
    df['data'] = pd.to_datetime(df['data'])
except FileNotFoundError:
    print("Erro: file doesn't found.")
    # Create sample data if file not found
    df = pd.DataFrame({
        'regiao': ['Norte', 'Sudeste', 'Sul'],
        'estado': ['RO', 'SP', 'RS'],
        'data': pd.to_datetime(['2020-03-01', '2020-03-01', '2020-03-01']),
        'casosNovos': [10, 50, 20],
        'casosAcumulados': [100, 500, 200],
        'obitosNovos': [1, 5, 2],
        'obitosAcumulados': [10, 50, 20]
    })

# Load the CSS data
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(external_stylesheets=external_stylesheets)

# Prepare data for the map (latest data for each state)
latest_data = df.groupby('estado').agg({
    'data': 'max',
    'obitosAcumulados': 'last',
    'casosAcumulados': 'last'
}).reset_index()

# Get unique states for dropdown
states_list = ['Todos os Estados'] + sorted(df['estado'].unique().tolist())

app.layout = html.Div([
    html.H1("Dashboard COVID-19 Brasil", 
            style={'textAlign': 'center', 'fontSize': 36, 'margin-top': '20px', 'marginBottom': '30px'}),
    
    html.Div([
        # Left side - Map
        html.Div(className ='twelve columns', children=[
            #html.H3("Óbitos Acumulados por Estado", style={'textAlign': 'center', 'marginBottom': '20px'}),
            dcc.Graph(id='brazil-map', style={'height': '600px'})
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),
        
        # Right side - Charts
        html.Div([
            # Top right - Line chart
            html.Div(className ='twelve columns', children=[
                #html.H3("Casos Novos por Data", style={'textAlign': 'center', 'marginBottom': '10px'}),
                html.Div([
                    html.Label("Selecione o Estado:", style={'marginRight': '10px'}),
                    dcc.Dropdown(
                        id='state-dropdown',
                        options=[{'label': state, 'value': state} for state in states_list],
                        value='Todos os Estados',
                        style={'width': '200px'}
                    )
                ], style={'marginBottom': '20px'}),
                dcc.Graph(id='line-chart', style={'height': '300px'})
            ], style={'marginBottom': '40px'}),
            
            # Bottom right - Bar chart
            html.Div(className ='twelve columns', children=[
                #html.H3("Dados Acumulados por Estado", style={'textAlign': 'center', 'marginBottom': '10px'}),
                html.Div([
                    html.Label("Selecione o Tipo de Dado:", style={'marginRight': '10px'}),
                    dcc.RadioItems(
                        id='data-type-selector',
                        options=[
                            {'label': 'Casos Acumulados', 'value': 'casosAcumulados'},
                            {'label': 'Óbitos Acumulados', 'value': 'obitosAcumulados'}
                        ],
                        value='casosAcumulados',
                        inline=True,
                        style={'marginBottom': '20px'}
                    )
                ]),
                dcc.Graph(id='bar-chart', style={'height': '300px'})
            ])
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'})
    ], style={'width': '100%'}),
    
    # Hidden div to trigger initial load
    dcc.Store(id='initial-load-trigger', data='loaded')
])

@callback(
    Output('brazil-map', 'figure'),
    Input('initial-load-trigger', 'data')
)
def update_map(data):
    if geogson["features"]:
        fig = px.choropleth(
            latest_data, 
            geojson=geogson,
            locations='estado',
            color='obitosAcumulados',
            hover_name='estado',
            hover_data={'estado': True, 'obitosAcumulados': True},
            color_continuous_scale='Reds',
            scope='south america',
            fitbounds="locations",
            title="Óbitos Acumulados por Estado"
        )
        
        fig.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            font=dict(size=12)
        )
        return fig
    else:
        return px.scatter(title="Erro ao carregar o mapa. Verifique o arquivo GeoJSON.")

@callback(
    Output('line-chart', 'figure'),
    Input('state-dropdown', 'value')
)
def update_line_chart(selected_state):
    if selected_state == 'Todos os Estados':
        # Group by date and sum all states
        line_data = df.groupby('data')['casosNovos'].sum().reset_index()
        title = "Casos Novos - Todos os Estados"
    else:
        # Filter for selected state
        line_data = df[df['estado'] == selected_state][['data', 'casosNovos']]
        title = f"Casos Novos - {selected_state}"
    
    fig = px.line(
        line_data, 
        x='data', 
        y='casosNovos',
        title=title,
        labels={'data': 'Data', 'casosNovos': 'Casos Novos'}
    )
    
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        font=dict(size=11)
    )
    
    return fig

@callback(
    Output('bar-chart', 'figure'),
    Input('data-type-selector', 'value')
)
def update_bar_chart(selected_data_type):
    # Get the sum for each state
    bar_data = latest_data.groupby('estado')[selected_data_type].sum().reset_index()
    bar_data = bar_data.sort_values(selected_data_type, ascending=False)
    
    # Set title and color based on selection
    if selected_data_type == 'casosAcumulados':
        title = "Casos Acumulados por Estado"
        color = 'lightblue'
    else:
        title = "Óbitos Acumulados por Estado"
        color = 'lightcoral'
    
    fig = px.bar(
        bar_data, 
        x='estado', 
        y=selected_data_type,
        title=title,
        labels={'estado': 'Estado', selected_data_type: selected_data_type.replace('Acumulados', ' Acumulados')},
        color_discrete_sequence=[color]
    )
    
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        font=dict(size=11),
        xaxis_tickangle=-45
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)




