from dash import Dash, html, dash_table
import pandas as pd

df  = pd.read_csv('data/world-data-2023.csv')

app = Dash()

app.layout = [
    html.H1("World Data 2023"),
    dash_table.DataTable(data=df.to_dict('records'), page_size=15)
]

if __name__ == '__main__':
    app.run(debug=True)