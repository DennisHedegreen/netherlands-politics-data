# Netherlands Tweede Kamer Party Availability

Status:

- checked for `Tweede Kamer 2025`
- checked for `Tweede Kamer 2023`
- internal normalized candidate output exists for both years

## Method

For each election year:

1. read `TKYYYY_uitslag.csv`
2. build each kieskring's party/list set from `RegioCode` prefix `K` and `VeldType == LijstAantalStemmen`
3. build each municipality's party/list set from `RegioCode` prefix `G` and `VeldType == LijstAantalStemmen`
4. map each municipality to its parent kieskring through `OuderRegioCode`
5. exclude `G9010 NBSB` from the ordinary European municipality check
6. compare every ordinary municipality's party/list set with its parent kieskring party/list set

## Findings

| Election | Unique party/lists overall | Ordinary municipalities checked | Municipality to parent-kieskring mismatches |
|---|---:|---:|---:|
| `2025` | `27` | `342` | `0` |
| `2023` | `26` | `342` | `0` |

Kieskring party/list counts:

| Election | Count distribution |
|---|---|
| `2025` | `19:1`, `21:1`, `22:2`, `23:3`, `24:8`, `25:4`, `26:1` |
| `2023` | `20:1`, `23:2`, `24:3`, `25:9`, `26:5` |

Ordinary municipality party/list row counts:

| Election | Count distribution |
|---|---|
| `2025` | `21:12`, `22:23`, `23:87`, `24:136`, `25:83`, `26:1` |
| `2023` | `23:25`, `24:48`, `25:161`, `26:108` |

Special bucket:

| Election | Code | Name | Parent kieskring | Party/list rows |
|---|---|---|---|---:|
| `2025` | `G9010` | `NBSB` | `K12` | `26` |
| `2023` | `G9010` | `NBSB` | `K12` | `25` |

## Normalization Rule

Missing party/list rows across municipalities are explained by kieskring-level ballot availability, not by random source omission.

First adapter rule:

- do not backfill every national party/list into every municipality
- preserve rows only for party/lists available in the municipality's parent kieskring
- treat a municipality missing a parent-kieskring party/list as a source error
- keep `election_year`, `lijst_nummer`, and `lijst_naam` together as the first internal party/list key

Do not use `lijst_nummer` alone as a cross-year party identifier.
