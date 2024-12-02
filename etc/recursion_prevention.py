# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Recursion prevention
#
# Here are two utilities for preventing accidential recursive calls where they should be forbidden. They grew out of a very peculiar problem we had at work. The solutions are not themselves elegant, but are useful for debugging and usable for safe-proofing code that can do nasty things when called recursively.

# %% [markdown]
# ## Recursive functions
#
# The following is a decorator that wraps a function and "poisons" the call stack so that it cannot be called again on deeper levels.

# %%
import functools
import inspect
from collections.abc import Callable
from typing import Never


def prevent_recursion[**P, R](fun: Callable[P, R]) -> Callable[P, R]:
    # We simply need a sentinel object with a unique id
    sentinel = set[Never]()

    @functools.wraps(fun)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        call_stack = inspect.stack()

        for frame_info in call_stack[1:]:
            if frame_info.frame.f_locals.get('sentinel') is sentinel:
                raise RecursionError(f'Did not expect a recursive function call for {fun!r}.')

        return fun(*args, **kwargs)

    return wrapper


# %%
@prevent_recursion
def fibonacci(n: int) -> int:
    assert n >= 0

    if n < 2:
        return n

    return fibonacci(n - 1) + fibonacci(n - 2)


# %%
fibonacci(1)

# %%
fibonacci(3)


# %% [markdown]
# ## Call stack singletons
#
# The following mixin disallows a class to be instantiated if the call stack already has a living instance **assigned to a variable**.

# %%
import inspect
from typing import Any, Self, override


class CallStackSingletonMixin:
    @override
    def __new__(cls, *args: Any, **kwargs: Any) -> Self:
        call_stack = inspect.stack()

        for frame_info in call_stack[1:]:
            for value in frame_info.frame.f_locals.values():
                if isinstance(value, cls):
                    raise RecursionError(f'Only one instance of {cls!r} allowed in the call stack.')

        return super().__new__(cls)


# %%
class Test(CallStackSingletonMixin):
    def __init__(self) -> None:
        pass


# %% [markdown]
# The following is fine because the first instance is not accessible (directly). The capture magic ensures that no instance is assigned to a variable by Jupyter.

# %%
# %%capture

Test()
Test()

# %% [markdown]
# The following is fine because there is an instance that is not assigned directly (although ideally it should not be fine).

# %%
# %%capture

test_set = {Test()}
Test()

# %% [markdown]
# The following is not fine because "t" is a living instance.

# %%
# %%capture

t = Test()
Test()
