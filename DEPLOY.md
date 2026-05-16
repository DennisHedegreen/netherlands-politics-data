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

## Streamlit Community Cloud draft

Use Streamlit Community Cloud with the GitHub repo already pushed:

- Repository: `DennisHedegreen/netherlands-politics-data`
- Branch: `main`
- Main file path: `app.py`
- Python version: `3.12`
- Secrets: none
- Suggested app URL: `dutch-politics-data` if available; otherwise leave blank and use the generated URL

Deploy privacy:

- The GitHub repo is private.
- Keep the Streamlit app private for this phase.
- Community Cloud may require GitHub private-repo access before the repo appears in the deploy picker.
- Community Cloud currently allows only one private app at a time, so delete or publicize any old private test app first if the deploy form blocks this one.

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
