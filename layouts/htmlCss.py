from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.io as pio

pio.templates.default = "simple_white"

df = pd.read_csv('data/world-data-2023.csv')

# app = Dash()

# Initialize the app - incorporate css
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(external_stylesheets=external_stylesheets)

app.layout = [
    html.Div(className='row', children='My layout with HTML and CSS', style={'textAlign': 'center', 'fontSize': 24}),

    html.Div(className='row', children=[
        dcc.RadioItems(options=['Infant mortality', 'Birth Rate', 'Life expectancy'], 
                       value='Birth Rate', id='main-selector', inline=True, style={'margin': '10px'}),
    ]),

    html.Div(className='row', children=[
    html.Div(className='six columns', children=[
        dash_table.DataTable(data=df.to_dict('records'), 
                             page_size=11, style_table={'overflowX': 'auto'})
        ]),

        html.Div(className='six columns', children=[
        dcc.Graph(figure={}, id='bar-chart-final')

        ])
    ])
]

@callback(
    Output(component_id='bar-chart-final', component_property='figure'),
    Input(component_id='main-selector', component_property='value')
)

def update_graph(col_chosen):
    fig = px.bar(df, x='Country', y=col_chosen)
    # rotate x-axis labels
    fig.update_xaxes(tickangle=45)
    # rotate axis of the graph
    return fig



if __name__ == '__main__':
    app.run(debug=True)