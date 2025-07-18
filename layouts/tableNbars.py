from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px

df  = pd.read_csv('data/world-data-2023.csv')

app = Dash()

app.layout = [
    html.H1("World Data"),
    dash_table.DataTable(data=df.to_dict('records'), page_size=15),
    dcc.Graph(figure=px.bar(df, x='Country', y='Birth Rate'))
]

if __name__ == '__main__':
    app.run(debug=True)