# Netherlands Election Scope

Current candidate election scope:

- election type: `Tweede Kamer`
- first target years: `2023`, `2025`
- public geography target: European Netherlands `gemeente`
- primary election source layer: `Kiesraad` via `data.overheid.nl`
- first output target: party vote share by municipality
- turnout target: diagnostic audit only; not a live factor while raw `Opkomst / Kiesgerechtigden` can exceed `100%` in island municipalities

Why this scope:

- Tweede Kamer is the cleanest national parliamentary layer
- `2023` and `2025` sit on the current stable municipality count window
- official 2025 data is available in EML and CSV and describes municipality list-level results
- a narrow two-year first pass avoids opening the older municipality-reform problem too early

Known source anchors:

- Kiesraad election-result databank:
  - `https://www.kiesraad.nl/verkiezingen/verkiezingsuitslagen`
- Data.overheid Tweede Kamer 2025 dataset:
  - `https://data.overheid.nl/en/dataset/verkiezingsuitslag-tweede-kamer-2025`
- Kiesraad 2025 per-municipality result overview:
  - `https://www.kiesraad.nl/verkiezingen/tweede-kamer/uitslagen/uitslagen-per-gemeente-tweede-kamer`

Not in scope yet:

- municipal council elections
- provincial elections
- European Parliament elections
- public cross-country comparison
- stembureau-level analysis
- older Tweede Kamer years before a municipality-boundary pass
- Caribbean Netherlands or abroad buckets inside the first European municipality factor layer

First acceptance test:

- `2023` and `2025` official election-year files can be normalized into municipality-level party vote shares
- municipality rows can be reconciled to the corresponding CBS municipality classifications
- non-European or special aggregate buckets are either excluded with a clear note or handled in a separate internal layer
- party labels can be kept readable without inventing English names too early
