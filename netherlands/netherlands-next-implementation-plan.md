# Netherlands Next Implementation Plan

Current state:

- candidate scaffold opened
- `Tweede Kamer 2025` CSV package harvested into `../data/politics/netherlands/elections/`
- `Tweede Kamer 2023` CSV package harvested into `../data/politics/netherlands/elections/`
- source-schema notes written at `source-schema/tk2025-csv-schema.md` and `source-schema/tk2023-csv-schema.md`
- party/list availability checked in `source-schema/tk-party-availability.md`
- ordinary `G` municipality codes and names align exactly across inspected `2023` and `2025`
- CBS 2023 and 2025 municipality classifications harvested and reconciled
- internal `TK2023` and `TK2025` municipality-party output written at `tweede-kamer/tweede_kamer_party_share_by_municipality.csv`
- official `L528 / Nederland` national vote-share output written at `tweede-kamer/tweede_kamer_national_vote_share.csv`
- turnout audit output written at `tweede-kamer/tweede_kamer_turnout_audit_by_municipality.csv`, but not promoted to `factors/`
- combined normalization manifest written at `../provenance/netherlands_tk_normalization_manifest.json`
- internal `population` factor output written at `factors/population.csv`
- population manifest written at `../provenance/netherlands_population_manifest.json`
- internal `population_density` factor output written at `factors/population_density.csv`
- population-density manifest written at `../provenance/netherlands_population_density_manifest.json`
- internal `age65` factor output written at `factors/age65_pct.csv`
- age65 manifest written at `../provenance/netherlands_age65_manifest.json`
- internal lagged `education` factor output written at `factors/education.csv`
- education manifest written at `../provenance/netherlands_education_manifest.json`
- internal lagged `income` factor output written at `factors/income.csv`
- income manifest written at `../provenance/netherlands_income_manifest.json`
- internal `one_person_households` factor output written at `factors/one_person_household_share_pct.csv`
- one-person households manifest written at `../provenance/netherlands_one_person_households_manifest.json`
- internal lagged `owner_occupied` factor output written at `factors/owner_occupied_dwelling_share_pct.csv`
- owner-occupied housing manifest written at `../provenance/netherlands_owner_occupied_manifest.json`
- internal private `cars` factor output written at `factors/cars_per_1000.csv`
- cars manifest written at `../provenance/netherlands_cars_manifest.json`
- internal runtime adapter written at `../adapters/netherlands/adapter.py`
- adapter has the same basic country-app shape as the other countries:
  - `Explore`
  - `Compare municipalities`
  - `By Municipality`
  - official land-total `National trends`
  - `About & sources`
- internal registry/profile exposure exists with `public_ready=False`
- rebuild script written at `../fetch_netherlands.py`
- dispatcher entry added in `../fetch_country.py`
- rebuild smoke reproduces the election, crosswalk, and current internal factor CSVs
- runtime smoke covers all five Netherlands views plus `Surprise me`
- Explore, Compare, National trends, and About now show the source-period / method-boundary caveats inside the UI
- National trends now uses the official `L528 / Nederland` source rows; the UI states that this national scope is separate from the European-municipality pattern layer
- Turnout audit confirms the raw fields reconcile, but raw `Opkomst / Kiesgerechtigden` exceeds `100%` in some island municipalities
- public GitHub preview mirror exists as `DennisHedegreen/netherlands-politics-data`
- mirror readback passes locally and is ready for public Streamlit preview deployment

Next useful passes:

1. deploy the public Streamlit preview from `netherlands-politics-data`
2. record the live preview URL in the mirror docs
3. run one live browser readback before any TID/public-homepage decision

First no-go conditions:

- no stable municipality code path
- CSV files only expose stembureau rows without a reliable municipality aggregate
- official source mixes European municipalities and special buckets in a way that cannot be separated cleanly
- CBS factor tables do not align to the election geography without manual guessing

Reference:

- `netherlands-election-scope.md`
- `netherlands-factor-board.md`
- `netherlands-harvest-backlog.md`
- `netherlands-public-vs-internal-boundary.md`
