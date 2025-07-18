from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.io as pio

# default theme for Plotly
pio.templates.default = "simple_white"

df = pd.read_csv('data/world-data-2023.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(external_stylesheets=external_stylesheets)

app.layout = html.Div(className='container', children=[ # Adiciona um container para o layout geral
    # header
    html.Div(className='row', children=[
        html.Div(className='twelve columns', children=[ # Ocupa a largura total para o cabeçalho
            html.H1("Dashboard de Dados Mundiais", style={'textAlign': 'center'}) # Usando H1 para o título
        ])
    ]),

    # Dropdown para selecionar país
    html.Div(className='row', children=[
        html.Div(className='six columns offset-by-three', children=[ # Centraliza o dropdown usando offset
            dcc.Dropdown(
                id='Country-dropdown',
                options=[{'label': country, 'value': country} for country in df.Country.unique()],
                value='Afghanistan', # Valor inicial
                placeholder="Selecione um País...", # Texto de placeholder
                # style={'width': '100%', 'margin': '10px 0'} # Ajuste de estilo se necessário
            )
        ])
    ]),

    # Gráfico
    html.Div(className='row', children=[
        html.Div(className='twelve columns', children=[ # Gráfico ocupa a largura total
            dcc.Graph(figure={}, id='chart-life-expectancy')
        ])
    ])
])


@callback(
    Output(component_id='chart-life-expectancy', component_property='figure'),
    Input(component_id='Country-dropdown', component_property='value')
)
def update_life_expectancy_chart(selected_country):
    # Filtra o DataFrame pelo país selecionado
    filtered_df = df[df['Country'] == selected_country]

    life_expectancy_value = filtered_df['Life expectancy'].iloc[0] if not filtered_df.empty else 0

    # Cria um DataFrame para o gráfico com um único ponto
    plot_df = pd.DataFrame({
        'Métrica': ['Expectativa de Vida'],
        'Valor': [life_expectancy_value]
    })

    fig = px.bar(plot_df, x='Métrica', y='Valor',
                 title=f'Expectativa de Vida em {selected_country}',
                 text='Valor') # Adiciona o valor como texto na barra

    fig.update_yaxes(range=[0, 100]) # Ajusta o range do eixo Y para Expectativa de Vida
    return fig


if __name__ == '__main__':
    app.run(debug=True)
