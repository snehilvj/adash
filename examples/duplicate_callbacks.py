from async_dash import Dash
from dash import html, dcc, Output, Input
from quart import Quart

import plotly.express as px
import plotly.graph_objects as go

server = Quart(__name__)
app = Dash(
    server=server,
    prevent_initial_callbacks=True
)

app.layout = html.Div([
    html.Button('Draw Graph', id='draw-2'),
    html.Button('Reset Graph', id='reset-2'),
    dcc.Graph(id='duplicate-output-graph')
])

@app.callback(
    Output('duplicate-output-graph', 'figure', allow_duplicate=True),
    Input('draw-2', 'n_clicks'),
    prevent_initial_call=True
)
def draw_graph(n_clicks):
    df = px.data.iris()
    return px.scatter(df, x=df.columns[0], y=df.columns[1], color="species")

@app.callback(
    Output('duplicate-output-graph', 'figure'),
    Input('reset-2', 'n_clicks'),
)
def reset_graph(input):
    return go.Figure()

if __name__ == '__main__':
    app.run(debug=True)