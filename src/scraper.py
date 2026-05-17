import os
import pandas as pd

from config.settings import RESULT_LIMIT, DIVISION, DIVISION_MAP
from parsers.parser import parse_event
from utils import get_season, scrape_list

# If All, scrape every division, otherwise just the selected one
divisions = list(DIVISION_MAP.values())[:-1] if DIVISION == "All" else [DIVISION]

for division in divisions:
    # Read all URLs from config file
    with open(f"../config/urls_{division}.txt", "r") as f:
        base_urls = [line.strip() for line in f if line.strip()]

    # Process each URL as a separate season
    for base_url in base_urls:
        url = f"{base_url}?limit={RESULT_LIMIT}"
        season = get_season(url)
        all_results = scrape_list(url, parse_event)

        # Combine all events into a single DataFrame and export to CSV
        output_path = f"../data/processed/{division}/{season}_{division}_results.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df = pd.concat([pd.DataFrame(result) for result in all_results])
        df.to_csv(output_path, index=False)
        print(f"Exported {season}_{division}_results.csv")