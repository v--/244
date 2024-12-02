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
# ## Retrieve startup count data

# %%
import json

import pandas as pd
import pycountry
import requests
from bs4 import BeautifulSoup


# Manually downloaded from https://www.startupranking.com/countries because of CloudFlare protection
with open('https __www.startupranking.com_countries.html') as file:
    sr_bs = BeautifulSoup(file.read())


sr_countries_tag = sr_bs.find_all(type='text/javascript')[17]
sr_countries = json.loads(sr_countries_tag.text[25:-6])
sr_df = pd.DataFrame(sr_countries['data'])[['code', 'name', 'value']] \
    .rename(columns=dict(code='iso2', value='startup_count'))


sr_df.head()

# %% [markdown]
# ### Retrieve population data

# %%
import requests


pop_res = requests.get('https://countriesnow.space/api/v0.1/countries/population')
pop_json = pop_res.json()['data']
pop_df = pd.DataFrame([
    dict(
        iso2=pycountry.countries.get(alpha_3=row['iso3']).alpha_2,
        population=row['populationCounts'][-1]['value']
    )
    for row in pop_json
    if pycountry.countries.get(alpha_3=row['iso3'])
])

pop_df.head()

# %% [markdown]
# ### Show countries by the number of startups per capita (only countries with >=1 million population)

# %%
df_full = sr_df.set_index('iso2').join(pop_df.set_index('iso2'), how='inner').reset_index()
df_full['startups_per_capita'] = df_full['startup_count'] / df_full['population']

large_countries = df_full[df_full['population'] >= 1e6]
per_capita = large_countries.sort_values('startups_per_capita', ascending=False, ignore_index=True).head(60)
per_capita.index += 1
per_capita

# %% [markdown]
# ### Show countries by the number of startups per capita (all countries)

# %%
per_capita_all = df_full.sort_values('startups_per_capita', ascending=False, ignore_index=True).head(60)
per_capita_all.index += 1
per_capita_all

# %% [markdown]
# ### Show countries by the number of startups overall (all countries)

# %%
overall = df_full.sort_values('startup_count', ascending=False, ignore_index=True).head(60)
overall.index += 1
overall
