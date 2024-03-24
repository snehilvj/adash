from async_dash import Dash
import dash
from dash import html, dcc
from quart import Quart

server = Quart(__name__)

app = Dash(__name__, server=server, use_pages=True)

app.layout = html.Div(
    [
        html.H1("App Frame"),
        html.Div(
            [
                html.Div(
                    dcc.Link(f"{page['name']} - {page['path']}", href=page["path"])
                )
                for page in dash.page_registry.values()
                if page["module"] != "pages.not_found_404"
            ]
        ),
        dash.page_container,
    ]
)

if __name__ == "__main__":
    server.run()