# ADash

`adash` is an async port of [Plotly Dash](https://github.com/plotly/dash) library, created by replacing its flask backend
with its async counterpart: [quart](https://pgjones.gitlab.io/quart/index.html).

It started with my need to be able to create realtime dashboards with `dash`, specifically with event-driven architecture.
Using `adash` with components from [dash-extensions](https://github.com/thedirtyfew/dash-extensions) such as WebSocket, 
EventSource, etc. you can create truly events based dashboards.

### Motivation

In addition to all the advantages of writing async code, `adash` enables you to:
1. run truly asynchronous callbacks
2. use websockets, server sent events, etc. without needing to monkey patch the Python standard library
3. use `quart` / [`fastapi`](https://fastapi.tiangolo.com) / [`starlette`](https://www.starlette.io) frameworks with your dash apps side by side
4. use HTTP/2 (especially server push) if you use it HTTP/2 enabled server such as [`hypercorn`](https://pgjones.gitlab.io/hypercorn/).

### Cons

I'm maintaining this library as a proof of concept for now. It should not be used for production. You can see the deviation from `dash` [here](https://github.com/snehilvj/adash/compare/dev...snehilvj:async-dash).

If you do decide to use it, I'd love to hear your feedback.

### Alternatives

#### [dash-devices](https://github.com/richlegrand/dash_devices)

`dash-devices` is another async port based on `quart`. Its capable os using websockets even for callbacks, which makes
it way faster than either of `dash` or `adash`. However, the library stands outdated at the time this document was last updated.

**PS:** `adash` is highly inspired by the `dash-devices`. Difference being that `adash` tries to follow `dash` as close as possible.

### Known Issues

1. Exception handling in callbacks is broken.

### TODO
1. Write examples/articles showcasing the use cases for asynchronous `dash`.
2. Gather reviews and feedback from the Dash Community.
