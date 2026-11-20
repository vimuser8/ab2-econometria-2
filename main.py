#!/usr/bin/env python3
import pandas as pd
import json
from pathlib import Path
    
from core import data

# scam_type.name  scam_type.type 

defi_df = data.load_data()
cols = defi_df.columns
for i, c in enumerate(cols):
    print(f"{i:>2}: {c}")


def get_unique(df, col):
    out  = df[col].unique()
    return out


cols = [
    "technical_issue",
    "funds_lost",
    "funds_returned",
    "funds_recovered",
    "is_verified_source_code",
    "is_public_team",
    "scam_type.name",
    "scam_type.type"
]
for c in cols:
    out = get_unique(defi_df, c)
    print(f"{c:>2}: {out}")
    print("")


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
