# AUTOGENERATED! DO NOT EDIT! File to edit: ../03b_ipyautoui.ipynb.

# %% auto 0
__all__ = ['controls', 'make_enforcer']

# %% ../03b_ipyautoui.ipynb 9
from ipyautoui import AutoUi

# %% ../03b_ipyautoui.ipynb 43
from .pydantic_model import DataSelectorModel

# %% ../03b_ipyautoui.ipynb 45
controls = AutoUi(DataSelectorModel)

# %% ../03b_ipyautoui.ipynb 61
from pydantic import ValidationError

# %% ../03b_ipyautoui.ipynb 62
def make_enforcer(ui):
    """
    Make a function that can be used to observe changes on a 
    user interface element.

    Parameters
    ----------

    ui: an AutoUi widget

    Returns
    -------

    callable
        A function that can be used as the observer of a traitlets event.
    """
    def constraint_enforcer(change):
        """
        Reset widget to the most recent valid value if the new
        value results in an invalid value.
        """
        try:
            # Every AutoUi widget has a copy of the model class
            # We'll try validating the value in change["new"] and see if it works
            ui.model.model_validate(change["new"])
        except ValidationError:
            # That failed, so reset the ui to the old value
            ui.value = change["old"]

    return constraint_enforcer

# %% ../03b_ipyautoui.ipynb 64
controls.observe(make_enforcer(controls), "_value")
