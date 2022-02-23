## Async Dash

`async-dash` is an async port of [Plotly Dash](https://github.com/plotly/dash) library, created by replacing its flask
backend with its async counterpart [quart](https://pgjones.gitlab.io/quart/index.html).

It started with my need to be able to create realtime dashboards with `dash`, specifically with event-driven
architecture. Using `async-dash` with components from [dash-extensions](https://github.com/thedirtyfew/dash-extensions)
such as WebSocket, EventSource, etc. you can create truly events based or realtime dashboards.

#### Table Of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Motivation](#motivation)
- [Caveats](#caveats)
- [Alternatives](#alternatives)
- [Known Issues](#known-issues)
- [TODO](#todo)

### Installation

```bash
pip install async-dash
```

### Usage

```python
from async_dash import Dash
from dash import html, dcc
```

Simple Example

```python
import asyncio
import random

from async_dash import Dash
from dash import html, Output, Input, dcc
from dash_extensions import WebSocket
from quart import websocket, json

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
```

### Motivation

In addition to all the advantages of writing async code, `async-dash` enables you to:

1. run truly asynchronous callbacks
2. use websockets, server sent events, etc. without needing to monkey patch the Python standard library
3. use `quart` / [`fastapi`](https://fastapi.tiangolo.com) / [`starlette`](https://www.starlette.io) frameworks with
   your dash apps side by side
4. use HTTP/2 (especially server push) if you use it HTTP/2 enabled server such
   as [`hypercorn`](https://pgjones.gitlab.io/hypercorn/).

### Caveats

I'm maintaining this library as a proof of concept for now. It should not be used for production. You can see the
deviation from `dash` [here](https://github.com/snehilvj/async-dash/compare/dev...snehilvj:async-dash).

If you do decide to use it, I'd love to hear your feedback.

### Alternatives

#### [dash-devices](https://github.com/richlegrand/dash_devices)

`dash-devices` is another async port based on `quart`. It's capable of using websockets even for callbacks, which makes
it way faster than either of `dash` or `async-dash`. However, the library stands outdated at the time this document was
last updated.

**PS:** `async-dash` is highly inspired by the `dash-devices`. Difference being that `async-dash` tries to follow `dash`
as close as possible.

### Known Issues

1. Exception handling in callbacks in **debug mode** is broken. So its disabled internally.

### TODO

1. Write examples/articles showcasing the use cases for asynchronous `dash`.
2. Gather reviews and feedback from the Dash Community.
