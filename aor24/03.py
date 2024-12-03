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
# Hey, ORville here 👋
#
# I'm a logistics manager overseeing the allocation of tasks to employees in our company, FurnitORe.
#
# Right now we have 100 tasks that need to be completed, and we also have 100 employees available to handle them.
#
# The catch is that assigning a task to an employee has a cost 💸.
#
# These costs vary depending on the difficulty of the task, the expertise of the employee, and other factors.
#
# I need your help to figure out the most cost-effective way to assign these tasks to employees.
#
# You can assume that each task is done by just one employee, and one employee is assigned to just one task.
#
# Can you help me solve this problem?

# %% [markdown]
# # Problem data

# %% [markdown]
# Here are the first 15 lines of the provided data file:
#
#     # The first line gives you the number of tasks (and employees)
#     # The rest of the lines give you the cost to assign each task to an employee, such that
#     # they're grouped in sets of the number of tasks.
#
#     # In this instance, you have 100 tasks and employees
#     # For the assignment of task 1, the cost for assigning it to employee 1 is 52, to employee 2 is 89, to employee 3 is 40... and to employee 100 is 69
#     # Similarly, for the assignment of task 2, the cost for assigning it to employee 1 is 20, to employee 2 is 17... and to employee 100 is 92
#     # And so on and so forth
#
#      100
#      52 89 40 77 89 14 9 77 92 77 52 53 96
#      96 92 76 33 81 92 84 36 81 47 55 87 35
#      31 71 6 20 8 10 75 54 50 12 38 5 20
#      93 70 63 95 96 61 53 35 25 60 64 42 46
#      68 20 61 53 61 28 86 16 51 32 39 19 28

# %% [markdown]
# # Solution
#
# We build a bipartite graph, with tasks in one part and employees in the other. The edges of the graph have the cost of work assigned to them. We then build a full matching of minimal cost, assigning each employee to a task.

# %%
from collections.abc import Iterable

import networkx as nx


def iter_data_file_numbers(path: str) -> Iterable[int]:
    with open(path) as file:
        for row in file:
            if row.startswith('#'):
                continue

            for num_str in row.split():
                yield int(num_str)


def read_data(path: str) -> nx.Graph:
    it = iter(iter_data_file_numbers(path))
    size = next(it)
    graph = nx.Graph()

    for i in range(1, size + 1):
        for j in range(1, size + 1):
            graph.add_edge(('task', i), ('employee', j), cost=next(it))

    return graph


graph = read_data('data/03.txt')
matching = nx.algorithms.bipartite.minimum_weight_full_matching(graph, weight='cost')
sum(graph.edges[task, employee]['cost'] for task, employee in matching.items())
