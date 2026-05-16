# Netherlands Factors

Public-preview factor layer for Netherlands.

Status:

- public preview only
- TID public-preview door exists, but not a full public launch
- public-preview runtime adapter exists
- public-preview mirror exposure exists

Current factors:

| Factor | Years | Rows | Source |
|---|---:|---:|---|
| `population` | `2023`, `2025` | `684` | CBS StatLine `03759NED` |
| `population_density` | `2023`, `2025` | `684` | CBS StatLine `70072NED` |
| `age65` | `2023`, `2025` | `684` | CBS StatLine `03759NED` |
| `education` | `2023`, `2025` | `682` | CBS StatLine `85525NED` |
| `income` | `2023`, `2025` | `678` | CBS StatLine `70072NED` |
| `one_person_households` | `2023`, `2025` | `684` | CBS StatLine `70072NED` |
| `owner_occupied` | `2023`, `2025` | `684` | CBS StatLine `70072NED` |
| `cars` | `2023`, `2025` | `684` | CBS StatLine `70072NED` |

## Population

File:

- `population.csv`

Rule:

- source field: `BevolkingOp1Januari_1`
- definition: population on January 1
- source table: CBS StatLine `03759NED`
- dimensions:
  - `Geslacht = T001038` total men and women
  - `Leeftijd = 10000` total age
  - `BurgerlijkeStaat = T001019` total marital status
- geography: matching CBS annual municipality classification
- `public_geography_id`: four-digit CBS municipality code
- `municipality`: CBS municipality name

Coverage:

- `2023`: `342/342` municipalities
- `2025`: `342/342` municipalities

Provenance:

- `../../provenance/netherlands_population_manifest.json`

## Population Density

File:

- `population_density.csv`

Rule:

- source field: `Bevolkingsdichtheid_57`
- definition: residents on January 1 per km2 land
- source table: CBS StatLine `70072NED`
- geography: matching CBS annual municipality classification
- `public_geography_id`: four-digit CBS municipality code
- `municipality`: CBS municipality name

Coverage:

- `2023`: `342/342` municipalities
- `2025`: `342/342` municipalities

Provenance:

- `../../provenance/netherlands_population_density_manifest.json`

## Age 65+

File:

- `age65_pct.csv`

Rule:

- source field: `BevolkingOp1Januari_1`
- definition: share of total population aged 65+
- source table: CBS StatLine `03759NED`
- dimensions:
  - `Geslacht = T001038` total men and women
  - `BurgerlijkeStaat = T001019` total marital status
  - `Leeftijd = 16500-19400` single-year ages 65-94 plus `22000` 95 years or older
- geography: matching CBS annual municipality classification
- denominator: existing `population.csv` total population on January 1
- `public_geography_id`: four-digit CBS municipality code
- `municipality`: CBS municipality name

Coverage:

- `2023`: `342/342` municipalities
- `2025`: `342/342` municipalities

Provenance:

- `../../provenance/netherlands_age65_manifest.json`

## Education

File:

- `education.csv`

Rule:

- source field: `k_3HboWo_4`
- definition: share of residents aged 15-75 whose highest completed education level is `hbo/wo`
- source table: CBS StatLine `85525NED`
- dimensions:
  - `Geslacht = T001038` total men and women
  - `Leeftijd = 52052` ages 15 to 75
- geography: matching CBS annual municipality classification
- `public_geography_id`: four-digit CBS municipality code
- `municipality`: CBS municipality name

Coverage:

- `2023`: `341/342` municipalities, source period `2023JJ00`, reference period `2023-10-01`
- `2025`: `341/342` municipalities, source period `2024JJ00`, reference period `2024-10-01`
- known gap: CBS publishes a null value for `GM0088` Schiermonnikoog in both source periods

Provenance:

- `../../provenance/netherlands_education_manifest.json`

## Income

File:

- `income.csv`

Rule:

- source field: `ParticuliereHuishoudensExclStudenten_136`
- definition: average standardized income for private households excluding student households
- source table: CBS StatLine `70072NED`
- unit: `1 000 euro`
- geography: matching CBS annual municipality classification
- `public_geography_id`: four-digit CBS municipality code
- `municipality`: CBS municipality name

Coverage:

- `2023`: `342/342` municipalities, source period `2023JJ00`
- `2025`: `336/342` municipalities, source period `2024JJ00`
- known 2025-view gap: CBS publishes null 2024 values for `GM0060` Ameland, `GM0088` Schiermonnikoog, `GM0093` Terschelling, `GM0096` Vlieland, `GM0277` Rozendaal, and `GM0339` Renswoude

Provenance:

- `../../provenance/netherlands_income_manifest.json`

## One-person Households

File:

- `one_person_household_share_pct.csv`

Rule:

- source field: `Eenpersoonshuishoudens_86`
- definition: private households consisting of one person as a share of all private households
- source table: CBS StatLine `70072NED`
- unit: `%`
- geography: matching CBS annual municipality classification
- `public_geography_id`: four-digit CBS municipality code
- `municipality`: CBS municipality name

Coverage:

- `2023`: `342/342` municipalities, source period `2023JJ00`
- `2025`: `342/342` municipalities, source period `2025JJ00`

Provenance:

- `../../provenance/netherlands_one_person_households_manifest.json`

## Owner-occupied Housing

File:

- `owner_occupied_dwelling_share_pct.csv`

Rule:

- source field: `Koopwoningen_94`
- definition: dwellings owned by the current or future resident, or used as second homes
- source table: CBS StatLine `70072NED`
- unit: `%`
- geography: matching CBS annual municipality classification
- `public_geography_id`: four-digit CBS municipality code
- `municipality`: CBS municipality name

Coverage:

- `2023`: `342/342` municipalities, source period `2023JJ00`
- `2025`: `342/342` municipalities, source period `2024JJ00`
- note: the 2025 election-year view uses 2024 as the latest usable source period for this field

Provenance:

- `../../provenance/netherlands_owner_occupied_manifest.json`

## Cars

File:

- `cars_per_1000.csv`

Rule:

- source field: `PersonenautoSParticulierenRelatief_204`
- definition: private passenger cars per 1,000 residents
- source table: CBS StatLine `70072NED`
- unit: `cars-per-1000-residents`
- note: this excludes company-registered cars, avoiding the distortion CBS notes around lease-company concentrations
- geography: matching CBS annual municipality classification
- `public_geography_id`: four-digit CBS municipality code
- `municipality`: CBS municipality name

Coverage:

- `2023`: `342/342` municipalities, source period `2023JJ00`
- `2025`: `342/342` municipalities, source period `2025JJ00`

Provenance:

- `../../provenance/netherlands_cars_manifest.json`

Do not promote Netherlands beyond the public-preview gate from these files alone. They are preview factor candidates for the current app surface, not a public-homepage, shared-profile, cross-country, or full-launch signal.
