# Netherlands Harvest Backlog

Working backlog for future source intake.

First source pass status:

- `Tweede Kamer 2025` CSV package harvested on `2026-05-15`
- `Tweede Kamer 2023` CSV package harvested on `2026-05-15`
- CBS 2023 and 2025 municipality classifications harvested on `2026-05-15`
- schema notes written at `source-schema/tk2025-csv-schema.md` and `source-schema/tk2023-csv-schema.md`
- party/list availability note written at `source-schema/tk-party-availability.md`
- geography reconciliation note written at `geography/cbs-election-geography-reconciliation.md`
- internal normalized `TK2023` and `TK2025` municipality-party output written at `tweede-kamer/tweede_kamer_party_share_by_municipality.csv`
- internal normalized `population` factor written at `factors/population.csv`
- internal normalized `population_density` factor written at `factors/population_density.csv`
- internal normalized `age65` factor written at `factors/age65_pct.csv`
- internal normalized `education` factor written at `factors/education.csv`
- internal normalized `income` factor written at `factors/income.csv`
- internal normalized `one_person_households` factor written at `factors/one_person_household_share_pct.csv`
- internal normalized `owner_occupied` factor written at `factors/owner_occupied_dwelling_share_pct.csv`
- internal normalized private `cars` factor written at `factors/cars_per_1000.csv`
- raw/source room created at `../data/politics/netherlands/elections/`
- raw geography room created at `../data/politics/netherlands/geography/`
- raw factor room created at `../data/politics/netherlands/factors/`
- internal runtime app adapter draft exists
- rebuild script exists at `../fetch_netherlands.py`

## Election Sources

### Tweede Kamer 2025

Target:

- official result by municipality and party list
- possible turnout fields if available in the same official CSV/EML pack

Known source:

- `https://data.overheid.nl/en/dataset/verkiezingsuitslag-tweede-kamer-2025`

Notes:

- dataset is published by Kiesraad
- license is listed as `CC-0 (1.0)`
- source page says CSV exists and includes municipality-level list results
- download package also includes a file with votes per list per polling station
- first pass should use municipality list-level results, not stembureau-level results

Observed:

- package contains `README_TK2025.txt`, `TK2025_uitslag.csv`, and `TK2025_Stemmen_Per_Lijst_Per_Stembureau.csv`
- `TK2025_uitslag.csv` is the first municipality-level source candidate
- `G` prefix has `343` rows because `G9010 NBSB` is present
- the first European municipality target should therefore be `342` rows after excluding `G9010`
- `O9001`, `O9002`, and `O9003` identify Bonaire, Sint Eustatius, and Saba and stay outside the first target geography
- `G`-level list-vote sums match valid-vote rows in the inspected file

Remaining checks:

- decide whether turnout can be promoted from the official `Kiesgerechtigden` / `Opkomst` / vote-validity rows
- keep turnout out of the live picker until denominator wording is explicit

### Tweede Kamer 2023

Target:

- same shape as 2025 if available
- use as the second first-pass year only after 2025 is normalized

Known source:

- `https://data.overheid.nl/en/dataset/verkiezingsuitslag-tweede-kamer-2023`

Observed:

- package contains `README_TK2023.txt`, `TK2023_uitslag.csv`, and `TK2023_Stemmen_Per_Lijst_Per_Stembureau.csv`
- `TK2023_uitslag.csv` matches the `TK2025` column layout
- ordinary `G` municipality codes and names align exactly with inspected `2025`
- ordinary municipality party/list sets match parent kieskring party/list sets
- `G`-level list-vote sums match valid-vote rows in the inspected file

Remaining checks:

- keep the rebuild script aligned with future source harvests
- keep turnout out of the public layer until denominator wording is explicit

## Factor Sources

### CBS StatLine Open Data

Known source:

- `https://www.cbs.nl/nl-nl/onze-diensten/open-data/StatLine-als-open-data`

Population source:

- CBS StatLine OData table `03759NED`
- field `BevolkingOp1Januari_1`
- `2023` and `2025` covered with `342/342` municipalities

Population-density source:

- CBS StatLine OData table `70072NED`
- field `Bevolkingsdichtheid_57`
- definition: residents on January 1 per km2 land
- `2023` and `2025` covered with `342/342` municipalities

Age 65+ source:

- CBS StatLine OData table `03759NED`
- derived from `BevolkingOp1Januari_1`
- rule: sum ages 65-94 plus CBS `95 jaar of ouder`, divide by total population on January 1
- `2023` and `2025` covered with `342/342` municipalities

Education source:

- CBS StatLine OData table `85525NED`
- field `k_3HboWo_4`
- definition: `hbo/wo` highest completed education share for ages 15-75
- `2023` covered with `341/342` municipalities
- `2025` app view uses lagged `2024` source period and covers `341/342` municipalities
- known gap: `GM0088` Schiermonnikoog is CBS-null, not backfilled

Income source:

- CBS StatLine OData table `70072NED`
- field `ParticuliereHuishoudensExclStudenten_136`
- definition: average standardized income for private households excluding student households
- unit: `1 000 euro`
- `2023` covered with `342/342` municipalities
- `2025` app view uses lagged `2024` source period and covers `336/342` municipalities
- known gaps: `GM0060`, `GM0088`, `GM0093`, `GM0096`, `GM0277`, and `GM0339` are CBS-null, not backfilled

### CBS Municipality Classification

Known source:

- `https://www.cbs.nl/nl-nl/onze-diensten/methoden/classificaties/overig/gemeentelijke-indelingen-per-jaar/indeling%20per%20jaar/gemeentelijke-indeling-op-1-januari-2025`

Observed:

- CBS 2023 and 2025 municipality classification sources each contain `342` municipality rows
- inspected `TK2023` and `TK2025` ordinary election municipality codes both match their corresponding CBS classification with `0` missing/extra codes
- raw name differences are suffix-format differences only after province-suffix normalization
- first crosswalk written at `geography/election_cbs_municipality_crosswalk.csv`

## First Local Output Targets

First harvest internal outputs:

- `netherlands/tweede-kamer/tweede_kamer_party_share_by_municipality.csv`
- `netherlands/tweede-kamer/tweede_kamer_turnout_by_municipality.csv` if defensible
- `netherlands/factors/population.csv`
- `netherlands/factors/population_density.csv`
- `netherlands/factors/age65_pct.csv`
- `netherlands/factors/education.csv`
- `netherlands/factors/income.csv`
- `netherlands/factors/one_person_household_share_pct.csv`
- `netherlands/factors/owner_occupied_dwelling_share_pct.csv`
- `netherlands/factors/cars_per_1000.csv`
- `provenance/netherlands_first_harvest_manifest.json`

Turnout and `provenance/netherlands_first_harvest_manifest.json` are still not written.

Current output exception:

- `netherlands/tweede-kamer/tweede_kamer_party_share_by_municipality.csv` now exists as an internal `2023`/`2025` candidate
- `netherlands/factors/population.csv`, `netherlands/factors/population_density.csv`, `netherlands/factors/age65_pct.csv`, `netherlands/factors/education.csv`, `netherlands/factors/income.csv`, `netherlands/factors/one_person_household_share_pct.csv`, `netherlands/factors/owner_occupied_dwelling_share_pct.csv`, and `netherlands/factors/cars_per_1000.csv` now exist as internal `2023`/`2025` factor candidates
- the first internal adapter draft can read these files behind internal profiles
- the output files must not be used for public registry exposure by themselves
