import pandas as pd
import json
from pathlib import Path
    
from core import data

# scam_type.name  scam_type.type 

defi_df = data.load_data()
cols = defi_df.columns
#for c in cols:
#    print(c)

scam_names = defi_df["scam_type.name"].unique()
scam_types = defi_df["scam_type.type"].unique()

losses = defi_df["funds_lost"]
desc = losses.describe()

for stat, val in desc.items():
    print(f"{stat:>6}: {val:,.2f}")

#print(type(desc))
#desc = [f"{d:,}" for d in desc]

#print(df.columns)
#years = df["date"].str[:4]
#print(years.value_counts(dropna=False).sort_index())

#for d in sorted(devs):
#    print(d)
#print(len(devs))

#print(df["incident_id"].is_unique)
#print(df["timeline.incident.year"].value_counts(dropna=False).sort_index())
#print(df["timeline.incident.year"].describe())
#print(df["timeline.incident.year"].value_counts().sort_index().tail(10))
