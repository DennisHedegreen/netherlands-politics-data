# Dutch Politics Data

Dutch Politics Data compares Dutch Tweede Kamer election vote shares with municipality-level structural factors. It is built for finding reporting leads and visible patterns, not for proving why people vote as they do.

This repo is a public preview, not a full public launch.

## Public Preview

- GitHub repo: [DennisHedegreen/netherlands-politics-data](https://github.com/DennisHedegreen/netherlands-politics-data)
- Visibility: `public`
- Live app: [netherlands-politics-data Streamlit app](https://netherlands-politics-data-djf4pmqhx6wa4r6ft5z9xx.streamlit.app/)
- Public status: `preview`, not TID-launched

## Declared Scope

- Country: Netherlands
- Election type: Tweede Kamer
- Unit of analysis: municipality
- Municipality election years: `2023`, `2025`
- National trend years: `2023`, `2025`
- Preview geography: `European Netherlands municipality`
- Factors: Population, Population density, Age 65+, Education, Income, One-person households, Owner-occupied housing, Cars

This repo is the Netherlands-only public preview extracted from the internal World-politics-data engine. It keeps the Dutch app shell, Netherlands data pack, source notes, and scope docs without pretending that the country surface has already become a full public launch.

## What You Can Do

- Compare party vote share with one or more municipality-level factors.
- Read whether the relationship is positive, negative, weak, moderate, or strong.
- Inspect high and low municipalities before turning a pattern into a claim.
- Use the result as a lead for reporting, not as the final story.

## What Not To Infer

- Correlation is not causation.
- Municipality-level patterns do not describe individual voters.
- A strong result does not prove why people voted as they did.
- A weak or missing result does not prove that a factor is irrelevant.
- The app is not a prediction model, campaign tool, or causal engine.

## How To Read Results

Positive correlation means higher party vote share tends to appear in municipalities where the selected factor is higher. Negative correlation means higher party vote share tends to appear where the selected factor is lower. The result is ranked by absolute correlation strength, so `-0.62` is treated as stronger than `0.31`.

Example: if a party has `r = 0.58` with population density, a responsible reading is: "The party tended to have higher vote shares in denser municipalities in this election year." It is not: "Density made voters choose this party."

## Quick Case

A journalist could start with a strong party-factor result, open the high and low municipality tables, and ask a concrete reporting question: is this a real geographic pattern, a party-history pattern, or just a one-year artifact? The app gives the lead. The reporting still has to do the verification.

See [METHODOLOGY.md](METHODOLOGY.md) before using results in public claims.

## Boundary

- Not a TID launch
- Not a cross-country Netherlands claim
- Not a second source of truth beside `World-politics-data`
- Not a full Netherlands election archive
- Not a live turnout-factor release

Intentionally missing:

- `TID` public door and public website links
- Full public-launch wording until Netherlands is explicitly declared TID-ready
- `Turnout` as a live factor until the Tweede Kamer audit layer is promoted deliberately
- Older Tweede Kamer years before the source and municipality semantics have been reviewed
- Caribbean/NBSB material in the municipality layer

## Preview Sources

- Election source: `Kiesraad/data.overheid.nl Tweede Kamer municipality results + CBS StatLine municipal indicators`
- Boundary note: `Public preview only; no TID door or cross-country claim`
- Statistics source: `CBS StatLine`
- Provenance notes: [provenance/](provenance/)

## Repo Structure

```text
app.py               Single-country public-preview wrapper
engine_app.py        Shared app shell extracted from the internal engine
correlation_utils.py Compatibility import for correlation helpers
core/                Runtime, presentation, correlation, and failure-state helpers
country_registry.py  Netherlands-only public-preview registry
netherlands/         Country data pack and scope notes
provenance/          Preview-safe manifests
tests/               Country-surface and logic contract tests
```

## Source Of Truth

This repo is a public preview surface. The shared internal source tree still exists separately and remains the source of truth for shell changes and future extraction work. Public claims should cite this repo cautiously and should not treat the preview as a final TID release.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```
