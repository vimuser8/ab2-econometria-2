import logging
import requests
import numpy as np
import pandas as pd
import json
import random
import sys
import time
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    force=True,
)

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:159.0) Gecko/20100101 Firefox/159.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://de.fi/',
    'Origin': 'https://de.fi',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

PARAMS = {
    'sortField': 'fundsLost',
    'sort': 'desc',
    'sortDirection': 'desc',
    'limit': '100',
    'page': '1',
}

DEFI_FILE = Path(__file__).parent.parent / "data/defi.json"

def export_to_json(data: list[dict], filename: str | Path = DEFI_FILE) -> Path:
    dst_path = Path(filename)
    with open(filename, "w", encoding="utf-8") as f:
        try:
            json.dump(data, f, ensure_ascii=False, indent=2)
            print("JSON-dumped successfully!")
        except Exception as exc:
            raise RuntimeError(f"Error exporting to json: {exc}")
    
    return dst_path

def import_data(limit: int=100) -> list[dict]:
    custom_params = PARAMS 
    master_list = []
    while True:
        print(f"Fetching page #{custom_params['page']}...")
        response = requests.get('https://api.de.fi/v1/rekt/list', params=custom_params, headers=HEADERS)  # TODO Turn this into an env variable
        if response.status_code==200:
            data = response.json() 
            records = data.get("items", [])
            if not records:
                break

            master_list.extend(records)

        else:
            raise RuntimeError("Giving up after wrong response for fear of data corruption") 

        curr_page = custom_params["page"]
        next_page = int(curr_page) + 1
        custom_params["page"] = str(next_page)
        
        time.sleep(random.uniform(2, 5))

    return master_list

def load_data(src_path: str | Path = DEFI_FILE):

    src_path = Path(src_path)
    if not src_path.exists():
        logger.info(f"{src_path} not found. Importing data...")
        imported_data = import_data()
        dst_path = src_path
        src_path = export_to_json(imported_data, dst_path)

    logger.info("Loading JSON data...")
    with open(src_path, encoding="utf-8") as f:
        data = json.load(f)

    defi = pd.json_normalize(data, sep=".")

    # Handling the data
    variables = ["funds_lost", "explt", "rug"]
    #variables = ["exit", "incog", "sus_src"]

    # Data-type conversion  Becomes process_data()
    defi = defi[~defi["name_categories"].str.startswith("CeFi")]

    defi["funds_lost"] = defi["funds_lost"].astype(float)
    defi["is_verified_source_code"] = defi["is_verified_source_code"].astype(float)
    defi["is_public_team"] = defi["is_public_team"].astype(float)
    defi["explt"] = defi["scam_type.name"].str.startswith("Exploit").astype(float)
    defi["rug"] = defi["scam_type.type"].str.endswith("Rugpull").astype(float)

    defi["token"] = (defi["name_categories"].str.lower()=="token").astype(float)
    defi["nontoken"] = 1 - defi["token"]

    # NEW
    CONTRACT = ("rugpull", "honeypot")
    TECHNICAL = ("access control", "flash loan attack", "oracle issue", "reentrancy")
    IMITATION = ("phishing",)
    MARKET = ("abandoned",)

    sub = defi["scam_type.type"].str.lower().str.strip()

    mapping = {
        **dict.fromkeys(CONTRACT, "contract"),
        **dict.fromkeys(TECHNICAL, "technical"),
        **dict.fromkeys(IMITATION, "imitation"),
        **dict.fromkeys(MARKET, "market")
    }

    defi["strategy"] = sub.map(mapping)
    defi["tech"] = (defi["strategy"]=="technical").astype(float)

    before_rows = defi.shape[0]
    defi = defi.dropna(subset=variables)

    # Custom variables

    # TODO check if all bool variables are actually reliable
    # Made post formatting (what is a better way?)
    defi["losses"] = np.log(defi["funds_lost"].astype(float))

    logger.info("Usable rows after dropping NAs: %d (from %d)", len(defi), before_rows)
   
    return defi
    
if __name__=="__main__":
    df = load_data()
    num_rows = df.shape[0]
    logger.info(num_rows)  # Should 100 times pages

    logger.info(df["strategy"].value_counts(dropna=False))
    logger.info(df["tech"].value_counts(dropna=False))
    logger.info(df["token"].value_counts(dropna=False))

