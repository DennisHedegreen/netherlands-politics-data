# Dutch Politics Data

A private Netherlands-only deploy mirror for the current Tweede Kamer municipality layer, kept internal until the Netherlands surface is honest enough for public release.

This repo is the Netherlands-only private mirror extracted from the internal World-politics-data engine. It keeps the Dutch app shell, Netherlands data pack, source notes, and internal-only scope docs without pretending that the country surface is already public-ready.

## Internal status

- Mirror visibility: `private`
- Public launch status: `not public-ready`
- GitHub repo: `https://github.com/DennisHedegreen/netherlands-politics-data`

## Current scope

- Election type: `Tweede Kamer`
- Municipality election years: `2023`, `2025`
- National trend years: `2023`, `2025`
- Mirror geography: `European Netherlands municipality`
- Current live factors in the private shell: `population`, `population density`, `age65`, `education`, `income`, `one-person households`, `owner-occupied housing`, `cars`

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## What this repo is not

- Not a public launch
- Not a cross-country Netherlands claim
- Not a second source of truth beside `World-politics-data`
- Not a full Netherlands election archive
- Not a live turnout-factor release

## Intentionally missing

- `TID` public door and public website links
- Public Streamlit deployment until Netherlands is explicitly declared public-ready
- `Turnout` as a live factor until the Tweede Kamer audit layer is promoted deliberately
- Older Tweede Kamer years before the source and municipality semantics have been reviewed
- Caribbean/NBSB material in the municipality layer

## Data sources

- Election source: `Kiesraad/data.overheid.nl Tweede Kamer municipality results + CBS StatLine municipal indicators`
- Secondary source: `Internal candidate only; no public mirror or cross-country claim`
- Statistics source: `CBS StatLine`

## Repo structure

```text
app.py               Single-country private wrapper
engine_app.py        Shared app shell extracted from the internal engine
correlation_utils.py Shared correlation helpers
country_registry.py  Single-country registry for this private mirror
netherlands/               Country data pack and scope notes
provenance/          Mirror manifests copied from the internal engine
tests/               Country-surface smoke tests
```

## Source of truth

This repo is a private country mirror. It exists to stage and verify Netherlands as a separate deploy surface while the shared internal engine still remains the only source of truth.
