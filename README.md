# TFRRS Scraper

Scrapes NCAA track and field performance lists from TFRRS going back to 2012.
One CSV per season per division, all individual events, both men and women.

Data feeds into the [tfrrs-dbt](https://github.com/Jamar-Manning/tfrrs-dbt) project for transformation and analysis in Snowflake.

## Setup

```
pip install -r requirements.txt
```

Configure `config/settings.py`, then generate URLs for each division:

```
python src/generate_urls.py
```

Then run the scraper:

```
python src/scraper.py
```

CSVs land in `data/processed/<division>/`.

## Configuration

All settings live in `config/settings.py`.

| Setting | Description |
|---------|-------------|
| `DIVISION_KEY` | Division to scrape: `1`=NCAA Div I, `2`=NCAA Div II, `3`=NCAA Div III, `4`=NAIA, `5`=All |
| `RESULT_LIMIT` | Top N results to return per event (1–500) |

## Output

One CSV per season per division, named `{season}_{division}_results.csv`.

| Column | Description |
|--------|-------------|
| division | Division (1–4) |
| season_year | Season year (e.g. 2026) |
| season_type | Indoor or Outdoor |
| event | Event name (e.g. 60 Meters, Long Jump) |
| gender | m or f |
| place | Finishing place |
| athlete | Athlete name |
| academic_year | Academic year (e.g. JR-3) |
| team | School name |
| result | Performance mark or time |
| meet | Meet name |
| meet_date | Date of performance |

## Structure

```
tfrrs-scraper/
├── config/
│   ├── settings.py           # division, result limit, and other constants
│   ├── urls_NCAA_Div_I.txt
│   ├── urls_NCAA_Div_II.txt
│   ├── urls_NCAA_Div_III.txt
│   └── urls_NAIA.txt
├── data/
│   └── processed/
│       ├── NCAA_Div_I/       # output CSVs, one per season
│       ├── NCAA_Div_II/
│       ├── NCAA_Div_III/
│       └── NAIA/
└── src/
    ├── generate_urls.py      # generates config URL txt files per division
    ├── scraper.py            # entry point
    ├── utils.py
    └── parsers/
        └── parser.py        # event parsing logic
```

## Notes

The result limit in `config/settings.py` controls how many results are fetched per event per page. At `500` (max), scraping all years and divisions takes roughly 20–40 minutes. At `5`, it runs in roughly a minute. Adjust based on your needs.

Data goes back to 2012 as earlier seasons are excluded due to inconsistent formatting.

Relay events are excluded therefore, individual performances only. Names not stored in Last, First format are kept as a full string in the athlete column.