import requests
import pandas as pd
import json
import random
import sys
import time
from pathlib import Path

import requests

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
    # Starts at page 1 (not zero)
    page_idx = 1
    while True:
        print(f"Fetching page #{custom_params['page']}...")
        response = requests.get('https://api.de.fi/v1/rekt/list', params=custom_params, headers=HEADERS)
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
        #if next_page == 3:
        #    break

        custom_params["page"] = str(next_page)
        
        time.sleep(random.uniform(2, 5))

    return master_list

def load_data(src_path: str | Path = DEFI_FILE):
    src_path = Path(src_path)
    if not src_path.exists():
        imported_data = import_data()
        dst_path = src_path
        src_path = export_to_json(imported_data, dst_path)

    with open(src_path, encoding="utf-8") as f:
        data = json.load(f)

    return pd.json_normalize(data, sep=".")
    
if __name__=="__main__":
    df = load_data()
    num_rows = df.shape[0]
    print(num_rows)  # Should 100 times pages

"""
scam_types = df["scam_type.name"].unique()
print(len(scam_types))
for st in scam_types:
    print(st)
"""

