from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

df = pd.read_csv('data/world-data-2023.csv')

app = Dash()

app.layout = [
    html.H1("World Data with Controls and Callbacks"),
    html.Hr(),
    dcc.RadioItems(options=['Infant mortality', 'Birth Rate', 'Life expectancy'], value='Birth Rate', id='main-selector'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=6),
    dcc.Graph(figure={}, id='main-graph')
]

@callback(
    Output(component_id='main-graph', component_property='figure'),
    Input(component_id='main-selector', component_property='value')
)

def update_graph(col_chosen):
    fig = px.bar(df, x='Country', y=col_chosen)
    return fig

if __name__ == '__main__':
    app.run(debug=True)