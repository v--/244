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
# # Party mode: randomly selecting which function to run
#
# Have you ever wondered what would happen if, whatever function you call, another function may get called instead? Without even disturbing the type system? Wonder no more.
#
# The party mode decorator does precisely this. It stores a list of functions groupped by signature and decides at runtime which of them to call. See the examples below. It gets bonkers towards the end.

# %%
import functools
import inspect
import random
from collections.abc import Callable


_party_dict = dict[inspect.Signature, list[Callable]]()


def party_mode[**P, T](fun: Callable[P, T]) -> Callable[P, T]:
    sig = inspect.signature(fun)

    if sig not in _party_dict:
        _party_dict[sig] = []

    choices = _party_dict[sig]
    choices.append(fun)

    @functools.wraps(fun)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return random.choice(choices)(*args, **kwargs)

    return wrapper


# %% [markdown]
# The simplest example is just not knowing which of the two strings we would get

# %%
@party_mode
def a() -> str:
    return 'a'


@party_mode
def b() -> str:
    return 'b'


a()  # It can return either 'a' or 'b' depending on the gods of nondeterminism

# %% [markdown]
# A slightly more exciting example is not knowing whether two vectors would get added or subtracted

# %%
from dataclasses import dataclass


@dataclass
class Vec2D:
    x: float
    y: float

    # We add return types in order for the types to be a part of the signature
    @party_mode
    def __add__(self, other: 'Vec2D') -> 'Vec2D':
        return Vec2D(self.x + other.x, self.y + other.y)

    @party_mode
    def __sub__(self, other: 'Vec2D') -> 'Vec2D':
        return Vec2D(self.x - other.x, self.y - other.y)


a = Vec2D(1, 2)
b = Vec2D(3, 4)
a + b  # Would b be added to a or subtracted from it?


# %% [markdown]
# It's fun enough as it is but what if we apply the decorator to classes? Well, classes are callable in Python and they have the signature of their initializer minus the 'self' parameter. So party mode would magically work, albeit in a rather weird way.

# %%
@party_mode
@dataclass
class Worker:
    name: str
    age: int


@party_mode
@dataclass
class Planet:
    name: str
    age: int


Worker('John', 43)  # It may be a Worker instance but it may also be a Planet instance

# %% [markdown]
# That's not what I would expect from party mode on a class, however. It breaks some safety guarantees - Worker and Planet may have completely different fields defined and we would not know in advance whether a method is defined or not. We do not want that type of unsafety in our programs. We can even add a condition on top of the party_mode decorator to return classes as they are.
#
# Instead, we can write the following decorator, which would create new classes by simply replace all methods in a class recursively (hence for nested classes also).

# %%
# These methods (and some more) should not be randomized in order to preserve correctness
magic_method_blacklist = ['__init__', '__weakref__', '__hash__', '__eq__', '__repr__', '__dataclass_fields__', '__dataclass_params__']


def recursive_party_mode[C: type](cls: C) -> C:
    fields = dict[str, Callable]()

    for name, field in vars(cls).items():
        if isinstance(field, Callable) and name not in magic_method_blacklist:
            if isinstance(field, type):
                fields[name] = recursive_party_mode(field)
            else:
                fields[name] = party_mode(field)
        else:
            fields[name] = field

    return type(
        cls.__name__,
        (cls, ),  # Make this a subclass of cls itself
        fields
    )


# %% [markdown]
# Let's see how to use it:

# %%
@recursive_party_mode
@dataclass
class Vec2D:
    x: float
    y: float

    @dataclass
    class Bound:
        start: Vec2D
        end: Vec2D

        def reverse(self) -> 'Vec2D.Bound':
            return Vec2D.Bound(self.end, self.start)

        def reflect_around_origin(self) -> 'Vec2D.Bound':
            return Vec2D.Bound(-self.start, -self.end)

    # We add return types in order for the types to be a part of the signature
    def __add__(self, other: Vec2D) -> Vec2D:
        return Vec2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2D) -> Vec2D:
        return Vec2D(self.x - other.x, self.y - other.y)

    def __neg__(self) -> Vec2D:
        return Vec2D(-self.x, -self.y)


a = Vec2D(1, 2)
b = Vec2D(3, 4)
a + b  # What would it do? Nobody knows in advance.
Vec2D.Bound(a, b).reverse()  # Would this reverse the bound vector or would it reflect it around the origin?

# %% [markdown]
# Up until now, all we had were toy examples. We haven't considered what would happen if we swapped `random.seed` with `exit`. These functions can both be called without arguments and do not have return values. They still have different signatures but the idea is clear.
#
# How about monkey-patching every single class and method from all currently loaded modules? That way even the party_mode decorator call fall victim of itself. Who knows.

# %%
import sys


def enable_full_party_mode() -> None:
    for module in sys.modules.values():
        for name, obj in vars(module).items():
            if isinstance(obj, type):
                setattr(module, name, recursive_party_mode(obj))
            elif isinstance(obj, Callable):
                setattr(module, name, party_mode(obj))

# %% [markdown]
# Would you run it?
