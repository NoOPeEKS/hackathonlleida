# %%
import pandas as pd
import json
from itertools import chain
from collections import ChainMap

with open('./Data/response.json') as f:
    data_dict = json.load(f)

# %%
data_list = data_dict['response']['comparables']


# %%
grouped_dict = {}
[grouped_dict.setdefault(key, []).append(value)
 for d in data_list for key, value in d.items()]

# %%
ordered_dict = {}
for key, value in grouped_dict.items():
    for i, inner_dict in enumerate(value):
        if key == 'media':
            continue
        ordered_dict.setdefault(i, []).append(inner_dict)
# %%
final_dict = {}
for key, value in ordered_dict.items():
    final_dict[key] = dict(ChainMap(*value))
# %%
df = pd.DataFrame.from_dict(final_dict).T
# %%
