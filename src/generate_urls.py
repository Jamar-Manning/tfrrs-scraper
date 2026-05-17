import re

from src.utils import fetch_page
from utils import get_division_urls

# All four college divisions
divisions = ["NCAA Div. I", "NCAA Div. II", "NCAA Div. III", "NAIA"]

# Fetch and write qualifying list URLs for each division to its own txt file
for division in divisions:
    urls = get_division_urls(division)
    filename = f"../config/urls_{division.replace(' ', '_').replace('.', '')}.txt"
    with open(filename, "w") as f:
        f.write("\n".join(urls))
    print(f"Wrote {len(urls)} URLs to {filename}")