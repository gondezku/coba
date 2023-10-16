import random
import string
from dataclasses import dataclass, field
from typing import List
import pandas as pd
import numpy as np

def objects_to_df(model, fields=None, exclude=None, date_cols=None, col_replace=None, **kwargs):
    # if not fields:
    #     fields = [field.name for field in model._meta.get_fields()]

    # if exclude:
    #     fields = [field for field in fields if field not in exclude]

    # records = model.objects.filter(**kwargs).values_list(*fields)

    # df = pd.DataFrame(list(records), columns=fields)

    strftime = date_cols.pop(0)
    date_col = date_cols.pop(0)
    
    df = pd.DataFrame(list(model), columns=fields)
    if col_replace:
        in_col = col_replace.pop(0)
        out_col = col_replace.pop(0)
        df.rename(columns = {in_col:out_col}, inplace = True)
    df.rename(columns = {date_col:'date'}, inplace = True)
    df['date'] = df['date'].dt.strftime(strftime)

    dta_csv = pd.read_csv('test.csv')
    dta_csv['date'] = pd.to_datetime(dta_csv['date'], format='%d-%m-%Y').dt.strftime(strftime)
    # dta_csv['date'] = dta_csv['date'].dt.strftime(strftime)
    dta_csv = pd.concat([df, dta_csv], ignore_index = True, sort=True)

    return dta_csv

def from_df(df, values, labels, stacks=None, aggfunc=np.sum, round_values=0, fill_value=0):
       
    pivot = pd.pivot_table(
        df,
        values=values,
        index=stacks,
        columns=labels,
        aggfunc=aggfunc,
        fill_value=0
    )

    pivot = pivot.round(round_values)

    

    # values=[]
    # for mylist in pivot.values:
    #         for el in mylist:
    #              values.append(int(el))
    # # values = (pivot.values)[0].tolist()
    # labels = pivot.index.tolist()
    values = ((pivot.values)).tolist()
    labels = pivot.index.tolist()

    dictionary = dict(zip(labels, values))

    Chart_Label = pivot.columns.tolist()

    return (dictionary), Chart_Label
