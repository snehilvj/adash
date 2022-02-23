from async_dash import (
    monkey_patch_callback,
    monkey_patch_callback_context,
    monkey_patch_dash,
)

monkey_patch_callback.apply()
monkey_patch_callback_context.apply()
monkey_patch_dash.apply()

Dash = monkey_patch_dash.Dash

__all__ = ["Dash"]
