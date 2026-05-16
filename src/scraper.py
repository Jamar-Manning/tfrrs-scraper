import pandas as pd

from config.settings import RESULT_LIMIT
from parsers.parser import parse_event
from utils import get_season, scrape_list

# Read all URLs from config file
with open("../config/urls.txt", "r") as f:
    base_urls = [line.strip() for line in f if line.strip()]

# Process each URL as a separate season
for base_url in base_urls:
    url = f"{base_url}?limit={RESULT_LIMIT}"
    season = get_season(url)
    all_results = scrape_list(url, parse_event)

    # Combine all events into a single DataFrame and export to CSV
    df = pd.concat([pd.DataFrame(result) for result in all_results])
    df.to_csv(f"../data/processed/{season}_results.csv", index=False)
    print(f"Exported {season}_results.csv")