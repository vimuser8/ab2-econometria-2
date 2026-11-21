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
    dummy_vars = ["sus_src", "incog", "explt", "rug", "tech", "public", "nontoken"]
    target_var = ["losses"]
    required_vars = target_var + dummy_vars

    X = pd.DataFrame(
        {
            #"rug": defi["rug"],
            #"tech": defi["tech"],
            #"sus_src": defi["sus_src"],
            #"public": defi["public"],
            #"token": defi["token"],
            #"nontoken": defi["nontoken"],
            #"incog": defi["incog"],
            "explt": defi["explt"],
            # some combination?
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
