import asyncio
import random

from dash import html, Output, Input, dcc
from dash_extensions import WebSocket
from quart import websocket, json
from async_dash import Dash

app = Dash(__name__)

app.layout = html.Div([WebSocket(id="ws"), dcc.Graph(id="graph")])

app.clientside_callback(
    """
function(msg) {
    if (msg) {
        const data = JSON.parse(msg.data);
        return {data: [{y: data, type: "scatter"}]};
    } else {
        return {};
    }
}""",
    Output("graph", "figure"),
    [Input("ws", "message")],
)


@app.server.websocket("/ws")
async def ws():
    while True:
        output = json.dumps([random.randint(200, 1000) for _ in range(6)])
        await websocket.send(output)
        await asyncio.sleep(1)


if __name__ == "__main__":
    app.run_server()
