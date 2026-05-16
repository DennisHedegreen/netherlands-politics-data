# Netherlands Tweede Kamer Outputs

Public-preview output room for Netherlands `Tweede Kamer` election data.

Current file:

- `tweede_kamer_party_share_by_municipality.csv`
- `tweede_kamer_national_vote_share.csv`
- `tweede_kamer_turnout_audit_by_municipality.csv`

Status:

- normalized preview candidate
- `2023` and `2025`
- public-preview runtime adapter exists
- public-preview mirror exposure exists
- TID public-preview door exists, but not a full public launch

Current output:

- `342` European Netherlands municipalities per year
- `16,684` municipality-party rows total
- `8,560` municipality-party rows for `2023`
- `8,124` municipality-party rows for `2025`
- `53` official national land-total party rows from `L528 / Nederland`
  - `26` rows for `2023`
  - `27` rows for `2025`
- `684` turnout audit rows
  - `342` rows for `2023`
  - `342` rows for `2025`
- `0` vote-sum mismatches against `AantalGeldigeStemmen` in both years
- `0` party-availability mismatches against parent kieskring party/list sets in both years
- `G9010 NBSB` excluded
- `O9001/O9002/O9003` excluded

Output rule:

- `public_geography_id` uses CBS municipality code
- `municipality` uses CBS municipality name
- `source_municipality` preserves the election source name
- `share` is party votes divided by `AantalGeldigeStemmen`, in percentage points
- `party_id` is a year-local list/name slug, not a cross-year party bridge

National output rule:

- `tweede_kamer_national_vote_share.csv` is built from `RegioCode == L528`, `Regio == Nederland`
- the national output keeps the source's land-total scope
- this is not the same scope as the European-municipality pattern layer
- the manifest records the valid-vote delta between `L528` and the European municipality layer:
  - `73,014` valid votes in `2023`
  - `90,186` valid votes in `2025`
- those deltas reconcile to `G9010 NBSB` plus `O9001/O9002/O9003`

Turnout audit rule:

- `tweede_kamer_turnout_audit_by_municipality.csv` is a diagnostic output, not a factor file
- all audit rows reconcile `Opkomst` to valid + blank + invalid votes
- raw `Opkomst / Kiesgerechtigden` exceeds `100%` in:
  - `2023`: `Ameland`, `Schiermonnikoog`, `Vlieland`
  - `2025`: `Ameland`, `Schiermonnikoog`, `Terschelling`, `Vlieland`
- keep turnout out of the live picker unless a defensible denominator rule is written

Provenance:

- `../../provenance/netherlands_tk_normalization_manifest.json`

Do not promote Netherlands beyond the public-preview gate from this file alone. The national output is source-backed, but public-homepage exposure, shared-profile exposure, cross-country claims, and full-launch wording still need a separate release decision.
