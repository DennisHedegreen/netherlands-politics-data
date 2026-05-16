# TK2025 CSV Source Schema

Source:

- dataset: `Verkiezingsuitslag Tweede Kamer 2025`
- publisher: `Kiesraad (Rijk)`
- catalog: `data.overheid.nl`
- resource: `Verkiezingsuitslag Tweede Kamer 2025 (CSV Formaat)`
- downloaded: `2026-05-15`
- local raw room: `../../data/politics/netherlands/elections/raw/2025-tweede-kamer/`

Status:

- raw source inspected
- internal normalized candidate output exists
- internal runtime adapter draft exists

## Package Contents

The ZIP contains three files:

| File | Rows excluding header | First use |
|---|---:|---|
| `README_TK2025.txt` | n/a | source description |
| `TK2025_uitslag.csv` | `47,609` | first municipality-level source candidate |
| `TK2025_Stemmen_Per_Lijst_Per_Stembureau.csv` | `240,562` | later polling-station source, not first pass |

The README states that this is research data and not the official election result. Preserve that wording in public-facing notes.

## `TK2025_uitslag.csv`

Delimiter:

- semicolon (`;`)

Columns:

- `Regio`
- `RegioCode`
- `OuderRegioCode`
- `GrootOuderRegioCode`
- `Partij`
- `LijstNummer`
- `LijstNaam`
- `KandidaatNummer`
- `KandidaatInitialen`
- `KandidaatVoornaam`
- `KandidaatTussenvoegsel`
- `KandidaatAchternaam`
- `KandidaatWoonplaats`
- `KandidaatGeslacht`
- `VeldType`
- `Waarde`

Observed `RegioCode` prefix counts:

| Prefix | Meaning from README | Count |
|---|---|---:|
| `G` | Gemeente | `343` |
| `O` | Openbaar lichaam | `3` |
| `K` | Kieskring | `20` |
| `P` | Provincie | `13` |
| `L` | Land | `1` |

Observed `VeldType` counts:

| VeldType | Rows |
|---|---:|
| `LijstAantalZetels` | `15` |
| `KandidaatGekozen` | `150` |
| `LijstAantalStemmen` | `9,011` |
| `KandidaatAantalStemmen` | `36,533` |
| `AantalBlancoStemmen` | `380` |
| `AantalGeldigeStemmen` | `380` |
| `AantalOngeldigeStemmen` | `380` |
| `Kiesgerechtigden` | `380` |
| `Opkomst` | `380` |

## First Municipality Target

The first app candidate should not treat all `G` rows as ordinary municipalities.

Working inclusion rule:

- include `RegioCode` prefix `G`
- include `VeldType == LijstAantalStemmen`
- exclude `G9010 NBSB`

Working exclusion rule:

- exclude `O9001 Bonaire`
- exclude `O9002 Sint Eustatius`
- exclude `O9003 Saba`
- exclude `K*`, `P*`, and `L*` aggregate rows
- exclude stembureau rows from first normalized output

Expected first target:

- `342` European Netherlands municipalities

## Vote Reconciliation

For `G` rows in `TK2025_uitslag.csv`:

- all `343` `G` regions have `AantalGeldigeStemmen`
- the sum of `LijstAantalStemmen` equals `AantalGeldigeStemmen` for every `G` region

After excluding `G9010 NBSB`, the same check must be repeated for the `342` European municipality target before writing normalized output.

## Party Availability

The file contains `27` unique party/list names overall.

Municipality-level `LijstAantalStemmen` rows do not contain every party in every municipality:

- minimum list rows per `G` region: `21`
- maximum list rows per `G` region: `26`

Availability check:

- ordinary municipalities checked: `342`
- parent-kieskring mismatches: `0`
- `G9010 NBSB` has parent `K12` and `26` party/list rows

Conclusion:

- missing party/list rows are explained by parent-kieskring ballot availability
- do not backfill every national party/list into every municipality
- preserve rows only for party/lists available in the municipality's parent kieskring

Use `tk-party-availability.md` as the shared rule before writing normalized output.

## National Summary Target

The file also contains an official land-total aggregate:

- `RegioCode`: `L528`
- `Regio`: `Nederland`
- `VeldType == LijstAantalStemmen`: `27` party/list rows
- `AantalGeldigeStemmen`: `10,571,990`

Normalization rule:

- write national trend rows from `L528 / Nederland`
- keep this as `source_scope = official_land_total`
- do not mix this denominator with the European-municipality correlation layer
- the `L528` valid-vote total exceeds the European-municipality target by `90,186` valid votes
- that delta reconciles to `G9010 NBSB` plus `O9001/O9002/O9003`

## Turnout Reconciliation

For ordinary European municipality rows:

- all `342` target regions have the turnout-related fields
- `Opkomst` equals `AantalGeldigeStemmen + AantalBlancoStemmen + AantalOngeldigeStemmen` for every target municipality

Note:

- `Opkomst` exceeds `Kiesgerechtigden` in `4` target municipalities: `Ameland`, `Schiermonnikoog`, `Terschelling`, and `Vlieland`
- do not publish a naive turnout percentage until the denominator wording is explicit

## `TK2025_Stemmen_Per_Lijst_Per_Stembureau.csv`

Delimiter:

- semicolon (`;`)

Columns:

- `GemeenteCode`
- `GemeenteNaam`
- `Postcode`
- `StembureauNaam`
- `StembureauCode`
- `PartijNaam`
- `AantalStemmen`

Observed:

- rows excluding header: `240,562`
- municipality codes: `346`
- party/list names: `27`
- stembureaus: `10,085`
- special codes present: `9001`, `9002`, `9003`, `9010`

This file is useful later for stembureau-level analysis, but it is not the first app source. The first app source should stay municipality-level.

## First Adapter Implication

`fetch_netherlands.py` should not be written as a broad parser yet.

First implementation should:

1. read `TK2025_uitslag.csv`
2. filter to ordinary European municipality target
3. normalize list votes to municipality-party rows
4. compute vote share from municipality valid votes
5. preserve party availability instead of backfilling absent rows
6. write a provenance manifest before any registry exposure

Do not add `netherlands` to `country_registry.py` until normalized outputs exist and pass coverage checks.
