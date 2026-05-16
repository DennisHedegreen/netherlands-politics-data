# Deploy

Netherlands private mirror deploy checklist.

## Local smoke

```bash
pip install -r requirements.txt
streamlit run app.py
```

Check:

- `Explore`
- `Compare municipalities`
- `By Municipality`
- `National trends`
- `About & Sources`

## Private mirror shape

- App title: `Dutch Politics Data`
- Country exposure: `Netherlands` only
- No public country selector
- No TID door or public homepage updates in this phase
- Internal-only until an explicit public-readiness decision exists

## Before pushing live

- confirm the netherlands data pack exists and loads cleanly
- confirm the README and methodology still say `private mirror`
- confirm internal-only notes still match the Netherlands boundary
- confirm no public-door language slipped into the repo
