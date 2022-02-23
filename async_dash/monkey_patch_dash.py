import asyncio
import inspect
import mimetypes
import pkgutil
import sys

import dash
import flask
import quart
from dash import _validate
from dash._grouping import map_grouping, grouping_len
from dash._utils import inputs_to_dict, split_callback_id, inputs_to_vals
from dash.fingerprint import check_fingerprint
from quart.utils import run_sync


# borrowed from dash-devices
def exception_handler(loop, context):
    if "future" in context:
        task = context["future"]
        exception = context["exception"]
        # Route the exception through sys.excepthook
        sys.excepthook(exception.__class__, exception, exception.__traceback__)


# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments, too-many-locals
class Dash(dash.Dash):
    server: quart.Quart

    async def serve_component_suites(self, package_name, fingerprinted_path):
        path_in_pkg, has_fingerprint = check_fingerprint(fingerprinted_path)

        _validate.validate_js_path(self.registered_paths, package_name, path_in_pkg)

        extension = "." + path_in_pkg.split(".")[-1]
        mimetype = mimetypes.types_map.get(extension, "application/octet-stream")

        package = sys.modules[package_name]
        self.logger.debug(
            "serving -- package: %s[%s] resource: %s => location: %s",
            package_name,
            package.__version__,
            path_in_pkg,
            package.__path__,
        )

        response = quart.Response(
            pkgutil.get_data(package_name, path_in_pkg), mimetype=mimetype
        )

        if has_fingerprint:
            # Fingerprinted resources are good forever (1 year)
            # No need for ETag as the fingerprint changes with each build
            response.cache_control.max_age = 31536000  # 1 year
        else:
            # Non-fingerprinted resources are given an ETag that
            # will be used / check on future requests
            await response.add_etag()
            tag = response.get_etag()[0]

            request_etag = quart.request.headers.get("If-None-Match")

            if '"{}"'.format(tag) == request_etag:
                response = quart.Response("", status=304)

        return response

    async def dispatch(self):
        body = await quart.request.get_json()
        quart.g.inputs_list = inputs = body.get(  # pylint: disable=assigning-non-slot
            "inputs", []
        )
        quart.g.states_list = state = body.get(  # pylint: disable=assigning-non-slot
            "state", []
        )
        output = body["output"]
        outputs_list = body.get("outputs") or split_callback_id(output)
        quart.g.outputs_list = outputs_list  # pylint: disable=assigning-non-slot

        quart.g.input_values = (  # pylint: disable=assigning-non-slot
            input_values
        ) = inputs_to_dict(inputs)
        quart.g.state_values = inputs_to_dict(  # pylint: disable=assigning-non-slot
            state
        )
        changed_props = body.get("changedPropIds", [])
        quart.g.triggered_inputs = [  # pylint: disable=assigning-non-slot
            {"prop_id": x, "value": input_values.get(x)} for x in changed_props
        ]

        response = (
            quart.g.dash_response  # pylint: disable=assigning-non-slot
        ) = quart.Response("", mimetype="application/json")

        args = inputs_to_vals(inputs + state)

        try:
            cb = self.callback_map[output]
            func = cb["callback"]

            # Add args_grouping
            inputs_state_indices = cb["inputs_state_indices"]
            inputs_state = inputs + state
            args_grouping = map_grouping(
                lambda ind: inputs_state[ind], inputs_state_indices
            )
            quart.g.args_grouping = args_grouping  # pylint: disable=assigning-non-slot
            quart.g.using_args_grouping = (  # pylint: disable=assigning-non-slot
                not isinstance(inputs_state_indices, int)
                and (
                    inputs_state_indices
                    != list(range(grouping_len(inputs_state_indices)))
                )
            )

            # Add outputs_grouping
            outputs_indices = cb["outputs_indices"]
            if not isinstance(outputs_list, list):
                flat_outputs = [outputs_list]
            else:
                flat_outputs = outputs_list

            outputs_grouping = map_grouping(
                lambda ind: flat_outputs[ind], outputs_indices
            )
            quart.g.outputs_grouping = (  # pylint: disable=assigning-non-slot
                outputs_grouping
            )
            quart.g.using_outputs_grouping = (  # pylint: disable=assigning-non-slot
                not isinstance(outputs_indices, int)
                and outputs_indices != list(range(grouping_len(outputs_indices)))
            )

        except KeyError as missing_callback_function:
            msg = "Callback function not found for output '{}', perhaps you forgot to prepend the '@'?"
            raise KeyError(msg.format(output)) from missing_callback_function
        if inspect.iscoroutinefunction(func):
            output = await func(*args, outputs_list=outputs_list)
        else:
            output = run_sync(func)(*args, outputs_list=outputs_list)
        response.set_data(output)
        return response

    def run_server(self, *args, **kwargs):
        loop = asyncio.get_event_loop()
        loop.set_exception_handler(exception_handler)
        if kwargs.get("debug", False):
            self.logger.warning(
                "Currently, `debug` mode in not supported in async-dash."
            )
            kwargs["debug"] = False
        return super().run_server(*args, **kwargs, loop=loop)

    async def serve_layout(self):
        return super().serve_layout()

    async def serve_reload_hash(self):
        return super().serve_reload_hash()

    async def index(self, *args, **kwargs):
        return super().index(*args, **kwargs)

    async def dependencies(self):
        return super().dependencies()

    async def _serve_default_favicon(self):
        return super()._serve_default_favicon()


def apply():
    flask.Flask = quart.Quart
    flask.Blueprint = quart.Blueprint
    flask.jsonify = quart.jsonify
    flask.Response = quart.Response
