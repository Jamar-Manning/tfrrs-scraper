# TFRRS Scraper

A Python scraper that pulls NCAA Division I track and field performance lists from TFRRS going back to 2012. Outputs a clean CSV per season covering all individual events for both men and women.

## What it does

Scrapes TFRRS performance lists and extracts athlete, team, event, result, and meet data into CSVs ready for analysis. Handles running events, field events, and combined events, and flags altitude and track-size converted marks.

## Setup

Install dependencies:

```
pip install -r requirements.txt
```

Add URLs to `config/urls.txt` (one per line) and set your result limit in `config/settings.py`, then run:

```
python src/scraper.py
```

CSVs will be exported to `data/processed/`.

## Output

Each CSV contains the following columns:

| Column | Description |
|--------|-------------|
| event | Event name (e.g. 60 Meters, Long Jump) |
| gender | m or f |
| place | Finishing place |
| athlete | Athlete name |
| year | Academic year (e.g. JR-3) |
| team | School name |
| result | Performance mark or time |
| converted | True if mark was altitude or track-size converted |
| meet | Meet name |
| meet_date | Date of performance |

## Structure

```
tfrrs-scraper/
├── config/
│   ├── settings.py       # result limit and other constants
│   └── urls.txt          # list of TFRRS performance list URLs
├── data/
│   └── processed/        # output CSVs, one per season
└── src/
    ├── scraper.py        # entry point
    ├── utils.py          # fetching and orchestration
    └── parsers/
        └── parser.py     # event parsing logic
```

## Notes

Relay events are intentionally excluded. This scraper focuses on individual performances only. Results flagged with `@` (altitude) or `#` (track size conversion) are marked in the `converted` column. Marks with no comma-separated name format are stored as a full name string in the athlete column.