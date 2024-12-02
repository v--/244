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
# # Problem description
#
# My friend VictORia and I are planning a road trip.
#
# We want to drive from Madrid to Copenhagen and we've seen there are a lot of ways to do it.
#
# Most probably, even if we wanted to go through Budapest, we cannot go that path. We have a limited budget for fuel of 73€, and we want to get the shortest possible way.
#
# Can you help me solve this problem?

# %% [markdown]
# # Problem data

# %% [markdown]
# Here are the first 20 lines of the provided data file:
#     
#     # The first line gives you:
#     # <number of potential cities to visit> <number of connections between them> <max budget in euros for fuel>
#     # The rest of the lines gives you the connections between cities, with the distance between them and the cost to travel from the first to the second one:
#     # <first city> <second city> <distance> <euros wasted in fuel>
#     
#     # In this instance, you have 100 cities with 955 connections between them, and 73 euros to spend on fuel
#     # Connection between cities 1 and 37 has a distance of 60 and a cost of 5 euros of fuel,
#     # connection between cities 1 and 59 has a distance of 9 and a cost of 59 euros of fuel,
#     # and so on and so forth
#     
#     # Madrid is the city 1
#     # Copenhagen is the city 100
#     
#      100 955 73 
#      1 37 60 5 
#      1 59 9 59 
#      1 72 63 1 
#      2 15 61 1 
#      2 20 16 39 
#      2 26 54 6 
#

# %% [markdown]
# # Solution
#
# We enumerate the simple paths from shortest to longest and check which of them fit the budget.

# %%
import itertools
import re
from collections.abc import Sequence
from textwrap import dedent

import IPython
import networkx as nx


graph = nx.DiGraph()


with open('data/02.txt') as file:
    for row in file:
        if match := re.fullmatch(r' (?P<src>\d+) (?P<dest>\d+) (?P<dist>\d+) (?P<cost>\d+) \n', row):        
            graph.add_edge(
                int(match.group('src')),
                int(match.group('dest')),
                dist=int(match.group('dist')),
                cost=int(match.group('cost'))
            )


def sum_along_path(path: Sequence[int], attr: str) -> int:
    return sum(
        graph.edges[src, dest][attr] for src, dest in itertools.pairwise(path)
    )


def find_path(src: int, dest: int, budget: int) -> Sequence[int]:
    for path in nx.shortest_simple_paths(graph, src, dest, 'dist'):
        if sum_along_path(path, 'cost') <= budget:
            return path

    raise LookupError('No such path exists')


path = find_path(src=1, dest=100, budget=73)


IPython.display.display(
    IPython.display.Markdown(
        dedent(
            '''
                Path   | Distance | Cost
                ------ | -------- | ----
                {path} | {dist}   | {cost}
            '''.format(
                path=' -> '.join(map(str, path)),
                dist=sum_along_path(path, 'dist'),
                cost=sum_along_path(path, 'cost')
            )
        )
    )
)
