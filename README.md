# TFRRS Scraper

Scrapes NCAA Division I track and field performance lists from TFRRS going back to 2012. One CSV per season, all individual events, both men and women.

## Setup

```
pip install -r requirements.txt
```

Add URLs to `config/urls.txt` and adjust the result limit in `config/settings.py`, then run:

```
python src/scraper.py
```

CSVs land in `data/processed/`.

## Output

| Column | Description |
|--------|-------------|
| event | Event name (e.g. 60 Meters, Long Jump) |
| gender | m or f |
| place | Finishing place |
| athlete | Athlete name |
| year | Academic year (e.g. JR-3) |
| team | School name |
| result | Performance mark or time |
| converted | True if altitude or track-size adjusted |
| meet | Meet name |
| meet_date | Date of performance |

## Structure

```
tfrrs-scraper/
├── config/
│   ├── settings.py       # result limit and other constants
│   └── urls.txt          # TFRRS performance list URLs
├── data/
│   └── processed/        # output CSVs, one per season
└── src/
    ├── scraper.py        # entry point
    ├── utils.py          # fetching and orchestration
    └── parsers/
        └── parser.py     # event parsing logic
```

## Notes

The result limit in `config/settings.py` controls how many results are fetched per event per page. At `500` (max), scraping all years takes roughly 5–10 minutes. At `5`, it runs in seconds. Adjust based on your needs.

Relay events are excluded therefore, individual performances only. Marks flagged with `@` (altitude) or `#` (track size) are noted in the `converted` column. Names not stored in Last, First format are kept as a full string in the athlete column.
