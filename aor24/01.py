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
# Hi, I'm ÉléonORe, and I'm struggling to organize a series of events...
#
# Each event requires a dedicated room.
#
# Some events have overlapping participants, so I can't schedule them in the same room at the same time.
#
# How many rooms do I need? How can I assign each event to a room so that no two overlapping events are scheduled in the same one?
#
# Ideally, I want to minimize the total number of rooms used.
#
# Can you help me solve this problem?

# %% [markdown]
# # Problem data

# %% [markdown]
# Here are the first 15 lines of the provided data file:
#     
#     # The first line gives you the number of events and the number of conflicts among them.
#     # The rest of the lines are the events in conflict.
#     
#     # In this instance, you have 100 events with 2487.
#     # The first conflict is event 1 with event 5,
#     # the second conflict is event 1 with event 7,
#     # and so on and so forth.
#     
#     100 2487
#     e 1 5
#     e 1 7
#     e 1 9
#     e 1 10
#     e 1 11
#     e 1 12

# %% [markdown]
# # Solution
#
# We can regard the events as vertices of a simple undirected graph, with an edge in case there is a conflict. The problem then reduces to finding a proper coloring of the graph.

# %%
import re

import networkx as nx


graph = nx.Graph()


with open('data/01.txt') as file:
    for row in file:
        if match := re.fullmatch(r'e (?P<eid>\d+) (?P<cid>\d+)\n', row):
            graph.add_edge(
                match.group('eid'),
                match.group('cid')
            )


coloring = nx.coloring.greedy_color(graph)
n_rooms = len(set(coloring.values()))
n_rooms
