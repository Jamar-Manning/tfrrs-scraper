from datetime import datetime
import re

def parse_event(event_container, event_name, gender, season_year, season_type):
    # Find the header (for event type detection) and body (for data extraction)
    header = event_container.find("div", class_="performance-list-header")
    body = event_container.find("div", class_="performance-list-body")

    # Extract each column by its data-label attribute
    places = body.find_all("div", {"data-label": "Place"})
    athletes = body.find_all("div", {"data-label": "Athlete"})
    academic_years = body.find_all("div", {"data-label": "Year"})
    teams = body.find_all("div", {"data-label": "Team"})

    # Running events use "Time", field events use "Mark", combined events use "Points"
    if header.find("div", {"data-label": "Time"}):
        results = body.find_all("div", {"data-label": "Time"})
    elif header.find("div", {"data-label": "Mark"}):
        results = body.find_all("div", {"data-label": "Mark"})
    else:
        results = body.find_all("div", {"data-label": "Points"})

    meets = body.find_all("div", {"data-label": "Meet"})
    meet_dates = body.find_all("div", {"data-label": "Meet Date"})

    # Initialize empty lists to store cleaned data for each column
    event_list = []
    gender_list = []
    season_year_list = []
    season_type_list = []
    place_list = []
    athlete_list = []
    academic_year_list = []
    team_list = []
    result_list = []
    converted_list = []
    meet_list = []
    meet_date_list = []

    # Extract and clean text from each column's elements
    for place in places:
        place_list.append(int(place.text.strip()) if place.text.strip().isdigit() else None)

    for athlete in athletes:
        athlete_list.append(athlete.text.strip())
        event_list.append(event_name)
        gender_list.append(gender)
        season_year_list.append(season_year)
        season_type_list.append(season_type)

    for academic_year in academic_years:
        academic_year_list.append(academic_year.text.strip())

    for team in teams:
        team_list.append(team.text.strip())

    for result in results:
        storage = result.text.strip()
        # Flag any result with non-numeric characters as converted
        cleaned = re.sub(r'[^0-9.:]', '', storage)
        converted = cleaned != storage.replace(" ", "")
        converted_list.append(converted)
        try:
            if ":" in cleaned:
                result_list.append(cleaned)
            else:
                result_list.append(round(float(cleaned), 2))
        except ValueError:
            result_list.append(None)

    for meet in meets:
        meet_list.append(meet.text.strip())

    # Parse meet dates into Python date objects
    for meet_date in meet_dates:
        meet_date_list.append(datetime.strptime(meet_date.text.strip(), "%b %d, %Y").date())

    return {
        "season_year": season_year_list,
        "season_type": season_type_list,
        "event": event_list,
        "gender": gender_list,
        "place": place_list,
        "athlete": athlete_list,
        "academic_year": academic_year_list,
        "team": team_list,
        "result": result_list,
        "converted": converted_list,
        "meet": meet_list,
        "meet_date": meet_date_list,
    }