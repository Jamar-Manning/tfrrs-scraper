from datetime import datetime

def parse_event(event_container, event_name, gender):
    # Find the header (for event type detection) and body (for data extraction)
    header = event_container.find("div", class_="performance-list-header")
    body = event_container.find("div", class_="performance-list-body")

    # Extract each column by its data-label attribute
    places = body.find_all("div", {"data-label": "Place"})
    athletes = body.find_all("div", {"data-label": "Athlete"})
    years = body.find_all("div", {"data-label": "Year"})
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
    place_list = []
    athlete_list = []
    year_list = []
    team_list = []
    result_list = []
    converted_list = []
    meet_list = []
    meet_date_list = []

    # Extract and clean text from each column's elements
    for place in places:
        place_list.append(place.text.strip())

    for athlete in athletes:
        athlete_list.append(athlete.text.strip())
        event_list.append(event_name)
        gender_list.append(gender)

    for year in years:
        year_list.append(year.text.strip())

    for team in teams:
        team_list.append(team.text.strip())

    for result in results:
        storage = result.text
        # Strip conversion indicators (@ = altitude, # = track size)
        if "@" in storage or "#" in storage:
            storage = storage.replace("@", "").replace("#", "")
            converted_list.append(True)
        else:
            converted_list.append(False)
        result_list.append(storage.strip())

    for meet in meets:
        meet_list.append(meet.text.strip())

    # Parse meet dates into Python date objects
    for meet_date in meet_dates:
        meet_date_list.append(datetime.strptime(meet_date.text.strip(), "%b %d, %Y").date())

    return {
        "event": event_list,
        "gender": gender_list,
        "place": place_list,
        "athlete": athlete_list,
        "year": year_list,
        "team": team_list,
        "result": result_list,
        "converted": converted_list,
        "meet": meet_list,
        "meet_date": meet_date_list,
    }