# Deploy

Netherlands public preview deploy checklist.

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

## Live Streamlit Preview

- Live app: [netherlands-politics-data Streamlit app](https://netherlands-politics-data-djf4pmqhx6wa4r6ft5z9xx.streamlit.app/)

## Streamlit Community Cloud settings

Current Streamlit Community Cloud settings:

- Repository: `DennisHedegreen/netherlands-politics-data`
- Branch: `main`
- Main file path: `app.py`
- Python version: `3.12`
- Secrets: none
- Suggested app URL: `dutch-politics-data` if available; otherwise leave blank and use the generated URL

Deploy privacy:

- The GitHub repo is public.
- The Streamlit app may be public for this preview.
- TID/site links may point only to the preview door; keep public homepage and shared profile exposure out until a separate full-launch decision exists.

## Public preview shape

- App title: `Dutch Politics Data`
- Country exposure: `Netherlands` only
- No public country selector
- TID door: public preview only
- Public preview only until an explicit TID-readiness decision exists

## Before pushing live

- confirm the netherlands data pack exists and loads cleanly
- confirm the README and methodology still say `public preview`
- confirm boundary notes still match the Netherlands preview boundary
- confirm the TID-door language stays preview-only
