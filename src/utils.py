import re

import requests
from bs4 import BeautifulSoup


def get_season(url):
    # Parse season from URL. grab last 4-digit year and detect Indoor/Outdoor
    parts = url.split("/")[-1].split("_")
    year = [p for p in parts if p.isdigit() and len(p) == 4][-1]
    season_type = "Indoor" if "Indoor" in parts else "Outdoor"
    return f"{year}_{season_type}"

def get_division(url):
    if "_I_" in url:
        return 1
    elif "_II_" in url:
        return 2
    elif "_III_" in url:
        return 3
    elif "NAIA" in url:
        return 4
    else:
        return None


def fetch_page(url):
    # Spoof as a browser to avoid being blocked
    headers = {"User-Agent": "Mozilla/5.0"}
    page = requests.get(url, headers=headers)
    return BeautifulSoup(page.text, "html.parser")


def scrape_list(url, parse_event):
    # Parse season info from URL
    season = get_season(url)
    season_year, season_type = season.split("_")
    division = get_division(url)

    # Fetch and parse the page
    soup = fetch_page(url)

    # Find all event anchors on the page
    events = soup.find_all("a", id=re.compile("^event"))

    all_results = []

    # Loop through each event, navigate to its container, and extract data
    for event in events:
        event_container = event.find_next_sibling()

        # Skip if no sibling container found
        if event_container is None or event_container.name == "a":
            continue

        h3 = event_container.find("h3")
        if h3 is None:
            continue

        event_name = h3.text.strip()
        event_name = event_name.split("(")[0].strip()
        header = event_container.find("div", class_="performance-list-header")

        # Skip relay events
        if "is-relay" in header.get("class", []):
            continue

        # Detect gender from event container classes
        classes = event_container.get("class", [])
        gender = "m" if "gender_m" in classes else "f"

        # Parse the event and collect results
        result = parse_event(event_container, division, event_name, gender, season_year, season_type)
        all_results.append(result)

    return all_results

def get_division_urls(division):
    soup = fetch_page("https://www.tfrrs.org/archives.html")

    available_seasons = []
    for tag in soup.find_all("a", href=True):
        label = tag.text.strip()
        if label[:4].isnumeric() and int(label[:4]) >= 2012:
            available_seasons.append(label[:4])

    division_urls = []
    for i, season in enumerate(available_seasons):
        outdoor_flag = i % 2
        url = f"https://www.tfrrs.org/college_archives_tab.html?outdoor={outdoor_flag}&year={season}"
        season_soup = fetch_page(url)
        tag = season_soup.find("a", string=re.compile(division))
        if tag:
            division_urls.append(tag["href"])

    return division_urls