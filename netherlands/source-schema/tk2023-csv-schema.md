# TK2023 CSV Source Schema

Source:

- dataset: `Verkiezingsuitslag Tweede Kamer 2023`
- publisher: `Kiesraad (Rijk)`
- catalog: `data.overheid.nl`
- resource: `Verkiezingsuitslag Tweede Kamer 2023 (CSV formaat)`
- downloaded: `2026-05-15`
- local raw room: `../../data/politics/netherlands/elections/raw/2023-tweede-kamer/`

Status:

- raw source inspected
- internal normalized candidate output exists
- internal runtime adapter draft exists

## Package Contents

The ZIP contains three files:

| File | Rows excluding header | First use |
|---|---:|---|
| `README_TK2023.txt` | n/a | source description |
| `TK2023_uitslag.csv` | `45,316` | municipality-level source candidate |
| `TK2023_Stemmen_Per_Lijst_Per_Stembureau.csv` | `251,488` | later polling-station source, not first pass |

The README states that this is research data and not the official election result. Preserve that wording in public-facing notes.

## `TK2023_uitslag.csv`

Delimiter:

- semicolon (`;`)

Columns match the inspected `TK2025_uitslag.csv` source:

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
| `AantalBlancoStemmen` | `380` |
| `AantalGeldigeStemmen` | `380` |
| `AantalOngeldigeStemmen` | `380` |
| `Opkomst` | `380` |
| `Kiesgerechtigden` | `380` |
| `KandidaatGekozen` | `150` |
| `LijstAantalZetels` | `15` |
| `KandidaatAantalStemmen` | `33,768` |
| `LijstAantalStemmen` | `9,483` |

## Municipality Target

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

The `342` ordinary `G` codes and names match the inspected `TK2025` ordinary municipality target exactly.

## Vote Reconciliation

For ordinary European municipality rows:

- all `342` target regions have `AantalGeldigeStemmen`
- the sum of `LijstAantalStemmen` equals `AantalGeldigeStemmen` for every target municipality
- `Opkomst` equals `AantalGeldigeStemmen + AantalBlancoStemmen + AantalOngeldigeStemmen` for every target municipality

Note:

- `Opkomst` exceeds `Kiesgerechtigden` in `3` target municipalities: `Ameland`, `Schiermonnikoog`, and `Vlieland`
- do not publish a naive turnout percentage until the denominator wording is explicit

## Party Availability

The file contains `26` unique party/list names overall.

Municipality party/list rows match each municipality's parent kieskring party/list set:

- ordinary municipalities checked: `342`
- parent-kieskring mismatches: `0`

Use `tk-party-availability.md` as the shared rule before writing normalized output.

## National Summary Target

The file also contains an official land-total aggregate:

- `RegioCode`: `L528`
- `Regio`: `Nederland`
- `VeldType == LijstAantalStemmen`: `26` party/list rows
- `AantalGeldigeStemmen`: `10,432,726`

Normalization rule:

- write national trend rows from `L528 / Nederland`
- keep this as `source_scope = official_land_total`
- do not mix this denominator with the European-municipality correlation layer
- the `L528` valid-vote total exceeds the European-municipality target by `73,014` valid votes
- that delta reconciles to `G9010 NBSB` plus `O9001/O9002/O9003`

## `TK2023_Stemmen_Per_Lijst_Per_Stembureau.csv`

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

- rows excluding header: `251,488`
- municipality codes: `344`
- party/list names: `26`
- stembureaus: `10,046`
- special codes present: `9001`, `9010`

This file is useful later for stembureau-level analysis, but it is not the first app source. The first app source should stay municipality-level.

## First Adapter Implication

`fetch_netherlands.py` can be scoped to the shared `TKYYYY_uitslag.csv` layout for `2023` and `2025`.

Do not add `netherlands` to `country_registry.py` until normalized outputs exist and pass coverage checks.
