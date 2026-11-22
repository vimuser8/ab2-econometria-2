#!/usr/bin/env python3
import logging
import numpy as np
import pandas as pd
import statsmodels.api as sm

from core import data
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    force=True,
)

logger = logging.getLogger(__name__)

if __name__=="__main__":
    defi = data.load_data()
    year_cols = [c for c in defi.columns if c.startswith("y_")]
    print(year_cols)

    X = pd.DataFrame(
        {
            "exploit": defi["exploit"],
            "sus_src": defi["sus_src"],
            "y_2021": defi["y_2021"],
            "y_2022": defi["y_2022"],
            "y_2023": defi["y_2023"],
            "y_2024": defi["y_2024"],
            "y_2025": defi["y_2025"],
            "y_2026": defi["y_2026"],
            #"is_public_team": defi["is_public_team"],
            #"cefi": defi["cefi"],
            #"tech": defi["tech"],
        },
        index=defi.index,
    )

    X = sm.add_constant(X, has_constant="add")
    y = defi["losses"]

    model = sm.OLS(y, X).fit(cov_type="HC1")
    print(model.summary())
    
    sys.exit(0)

    # Goes to a unittest file
    for col in dummy_vars:
        unique_vals = set(defi[col].unique())
        if not unique_vals.issubset({0, 1}):
            raise ValueError(f"Column '{col}' has non-binary values: {unique_vals}")

    """
    summary = df.groupby("scam_type.type", as_index=False)["funds_lost"].sum()
    for _, rw in summary.iterrows():
        print(rw["scam_type.type"], f"{rw['funds_lost']:,}")

    print(df.shape[0])
    """
