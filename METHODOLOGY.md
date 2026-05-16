# Methodology — Dutch Politics Data

## What this tool is

A public preview reading surface for Dutch politics data. It pairs Tweede Kamer election results with the current municipality-safe factor layer while keeping the TID/public-launch boundary explicit.

## What this tool is not

- It is not a prediction model.
- It is not a political recommendation engine.
- Correlation is not causation.
- Municipal-level patterns do not describe individual voters.

## Preview scope

- Country: `Netherlands`
- Election type: `Tweede Kamer`
- Public geography: `municipality`
- Public geography count: `342`
- Current public factors: `Population, Population density, Age 65+, Education, Income, One-person households, Owner-occupied housing, Cars`

## Data handling rules

- Missing data is shown honestly rather than backfilled.
- Public factors only enter the surface when municipality coverage and semantics are good enough.
- Party label mode only changes displayed labels. Data values and party IDs remain the same.
- The public layer stays narrower than the internal engine on purpose.

## Sources

- Election source: `Kiesraad/data.overheid.nl Tweede Kamer municipality results + CBS StatLine municipal indicators`
- Boundary note: `Public preview only; TID door is preview-labelled and there is no cross-country claim`
- Statistics source: `CBS StatLine`

## Known limitations

- This surface intentionally keeps a narrower public scope than the internal engine.
- If a factor or year combination does not hold up, it should disappear rather than survive as a lie.
- Some future country-specific factors may exist internally before they earn public release here.
