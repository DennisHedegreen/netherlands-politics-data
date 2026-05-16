# Netherlands CBS / Election Geography Reconciliation

Status:

- CBS 2023 municipality classification harvested
- CBS 2025 municipality classification harvested
- `Tweede Kamer 2023` election municipalities reconciled to CBS 2023
- `Tweede Kamer 2025` election municipalities reconciled to CBS 2025
- first crosswalk written to `election_cbs_municipality_crosswalk.csv`

## Sources

CBS source family:

- `Gemeentelijke indeling op 1 januari 2023`
- `Gemeentelijke indeling op 1 januari 2025`

Election source family:

- Kiesraad/data.overheid.nl `TK2023_uitslag.csv`
- Kiesraad/data.overheid.nl `TK2025_uitslag.csv`

## Reconciliation Result

| Election year | CBS municipality rows | Election ordinary `G` rows | Code-only mismatches | Normalized-name mismatches |
|---|---:|---:|---:|---:|
| `2023` | `342` | `342` | `0` | `0` |
| `2025` | `342` | `342` | `0` | `0` |

The election files and CBS files match by municipality code after excluding:

- `G9010 NBSB`
- `O9001 Bonaire`
- `O9002 Sint Eustatius`
- `O9003 Saba`

## Name Differences

Raw names differ only because CBS and the election files do not always use identical province-suffix spelling.

Examples:

- CBS `Bergen (NH.)` vs election `Bergen (NH)`
- CBS `Bergen (L.)` vs election `Bergen (L)`
- CBS `Beek (L.)` vs election `Beek`
- CBS `Hengelo (O.)` vs election `Hengelo (O)`

Normalization rule:

- compare municipality identity by CBS/election code
- use CBS municipality name as canonical public geography label
- accept name differences only when they collapse under province-suffix normalization

## First Output Rule

For internal normalized election outputs:

- `public_geography_id` is the four-digit CBS municipality code
- `municipality` is the CBS municipality name
- `source_municipality` preserves the election source name
- `geography_version` names the matching CBS annual classification

No public runtime adapter should expose Netherlands until this rule is used consistently by both election and factor outputs and the internal adapter has passed smoke testing.
