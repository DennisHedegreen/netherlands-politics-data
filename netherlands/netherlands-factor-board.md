# Netherlands Factor Board

Public-preview planning note for the first Netherlands factor passes.

This is not a cross-country comparability claim. It is a working board for deciding what can enter the Netherlands public-preview layer without lowering the honesty bar.

## First Candidate Batch

### `population`

Why:

- core denominator and sanity layer
- needed for per-capita normalization and coverage checks
- CBS municipality source path should be straightforward

Current disposition:

- source path harvested
- normalized preview candidate exists at `factors/population.csv`
- source: CBS StatLine `03759NED`
- field: `BevolkingOp1Januari_1`
- first target years covered: `2023`, `2025`
- coverage: `342/342` municipalities in both years

### `population_density`

Why:

- strong first structural signal
- directly useful for urban/rural settlement reading without forcing a blunt classification
- likely available through CBS regional core or municipality tables

Current disposition:

- source path harvested
- normalized preview candidate exists at `factors/population_density.csv`
- source: CBS StatLine `70072NED`
- field: `Bevolkingsdichtheid_57`
- first target years covered: `2023`, `2025`
- coverage: `342/342` municipalities in both years
- denominator: CBS residents on January 1 per km2 land

### `age65`

Why:

- clean demographic structure signal
- usually easier to defend than labour-market or welfare semantics

Current disposition:

- source path harvested
- normalized preview candidate exists at `factors/age65_pct.csv`
- source: CBS StatLine `03759NED`
- field: `BevolkingOp1Januari_1`
- rule: sum ages 65-94 plus CBS `95 jaar of ouder`, divide by total population on January 1
- first target years covered: `2023`, `2025`
- coverage: `342/342` municipalities in both years

### `education`

Why:

- part of the Denmark, Sweden, and Norway factor family
- analytically useful for a first national-election reading

Current disposition:

- source path harvested
- normalized preview candidate exists at `factors/education.csv`
- source: CBS StatLine `85525NED`
- field: `k_3HboWo_4`
- definition: `hbo/wo` highest completed education share for ages 15-75
- target app years covered: `2023`, `2025`
- source periods: `2023JJ00` for 2023, `2024JJ00` as latest available lagged source for 2025
- coverage: `341/342` municipalities in both app years
- known gap: `GM0088` Schiermonnikoog is null in CBS, not backfilled
- disposition: preview live candidate only; this is not a full-coverage factor

### `income`

Why:

- useful structural complement to education
- likely available in CBS income / regional core material

Current disposition:

- source path harvested
- normalized preview candidate exists at `factors/income.csv`
- source: CBS StatLine `70072NED`
- field: `ParticuliereHuishoudensExclStudenten_136`
- definition: average standardized income for private households excluding student households
- unit: `1 000 euro`
- target app years covered: `2023`, `2025`
- source periods: `2023JJ00` for 2023, `2024JJ00` as latest available lagged source for 2025
- coverage: `342/342` municipalities in 2023 and `336/342` municipalities in 2025 app view
- known gap: CBS nulls for Ameland, Schiermonnikoog, Terschelling, Vlieland, Rozendaal, and Renswoude in the 2024 source period
- disposition: preview live candidate only; this is not a TID-launch factor by itself

## Safe Second Batch

### `one_person_households`

Why:

- clean household-structure signal
- full municipality coverage in the already-harvested CBS `70072NED` current-period rowset
- useful alongside education and income without adding sensitive wording

Current disposition:

- normalized preview candidate exists at `factors/one_person_household_share_pct.csv`
- source: CBS StatLine `70072NED`
- field: `Eenpersoonshuishoudens_86`
- definition: one-person private households as a share of all private households
- coverage: `342/342` municipalities in both `2023` and `2025`
- disposition: preview live candidate only

### `owner_occupied`

Why:

- stable housing-tenure signal
- easy to explain in public language if it later earns promotion
- aligns with the broader housing-factor family already used in the system

Current disposition:

- normalized preview candidate exists at `factors/owner_occupied_dwelling_share_pct.csv`
- source: CBS StatLine `70072NED`
- field: `Koopwoningen_94`
- definition: owner-occupied dwellings as a share of dwellings
- coverage: `342/342` municipalities in both app years
- source periods: `2023JJ00` for 2023, `2024JJ00` as latest usable source for 2025
- disposition: preview live candidate only; lagged 2025 wording must remain visible

### `cars`

Why:

- readable mobility/rurality proxy
- full municipality coverage in the already-harvested CBS `70072NED` current-period rowset
- the private-car field avoids the lease-company distortion in total registered cars

Current disposition:

- normalized preview candidate exists at `factors/cars_per_1000.csv`
- source: CBS StatLine `70072NED`
- field: `PersonenautoSParticulierenRelatief_204`
- definition: private passenger cars per 1,000 residents, excluding company-registered cars
- coverage: `342/342` municipalities in both `2023` and `2025`
- disposition: preview live candidate only

## Investigate After First Batch

### `turnout`

Why:

- election-context signal, not a socioeconomic factor
- may be derivable from official election totals

Current disposition:

- audit output exists at `tweede-kamer/tweede_kamer_turnout_audit_by_municipality.csv`
- all rows reconcile `Opkomst = valid + blank + invalid`
- raw `Opkomst / Kiesgerechtigden` exceeds `100%` in `Ameland`, `Schiermonnikoog`, `Vlieland`, and in 2025 also `Terschelling`
- do not promote to `factors/` or the live picker unless a defensible denominator rule is written

### `housing`

Why:

- Netherlands may have strong housing-tenure and dwelling-type signals
- potentially useful after the first structural batch

Current disposition:

- first safe housing-tenure slice is now live as `owner_occupied`
- keep broader housing fields out until the basic Netherlands method wording is tested

### `employment` / `unemployment`

Why:

- analytically useful but semantically more fragile
- likely more source-definition work than the first pass should carry

Current disposition:

- later
- investigate only after population, density, age, education, and income are stable

## Blocked For Now

### `immigration_share`

Why:

- politically and semantically risky
- high chance of weak public wording if added too early
- should only be considered after the Netherlands adapter has a tested method layer

### `crime`

Why:

- public wording and source comparability are not locked
- not needed for the first public-preview country proof

## Working Order

1. lock current municipality list and codes
2. normalize `2023` and `2025` Tweede Kamer election years
3. choose and harvest one core CBS StatLine factor source
4. run municipality coverage checks
5. only then draft adapter and registry work

Current working-order status:

- steps 1-4 are complete for `population` and `population_density`
- steps 1-4 are complete with caveats for `education`
- step 5 now has a public-preview adapter with `population`, `population_density`, `age65`, lagged `education`, and lagged `income`
- safe second batch now adds `one_person_households`, lagged `owner_occupied`, and private-car `cars`
- next useful pass is local UI/browser interaction and method wording, not broad factor harvesting
