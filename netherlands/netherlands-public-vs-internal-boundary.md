# Netherlands Public Vs Internal Boundary

Public now:

- public GitHub preview mirror: `netherlands-politics-data`
- public-preview Streamlit app shell: `https://netherlands-politics-data-djf4pmqhx6wa4r6ft5z9xx.streamlit.app/`
- TID public-preview door: `https://hedegreenresearch.com/tid/netherlands-politics-data/`
- preview-level README, methodology, provenance, and normalized output files

Still not public-launched:

- no public homepage link
- no cross-country claim
- no public live-country switch exposure from `World-politics-data`
- TID wording must stay preview-only

Internal now:

- candidate planning notes
- raw election and geography source rooms
- raw factor source room
- internal normalized `TK2023`/`TK2025` municipality-party output
- internal normalized `L528 / Nederland` national vote-share output
- internal turnout audit output, held out of the live picker
- internal normalized `population` factor output
- internal normalized `population_density` factor output
- internal adapter draft
- internal registry/profile exposure

Not ready for public:

- any claim that Netherlands belongs in the public live country switch
- any cross-country comparison involving the Netherlands
- any final public-launch wording beyond the current public-preview door

First internal boundary:

- start with European Netherlands municipalities
- keep Caribbean Netherlands and any special aggregate election rows out of the first factor-aware municipality layer
- keep the official `L528 / Nederland` national vote-share layer separate from the European-municipality correlation layer
- keep turnout out of the factor layer because raw `Opkomst / Kiesgerechtigden` can exceed `100%` in island municipalities
- keep `2023` and `2025` as the first national-election years
- keep older years parked until municipality-boundary drift is understood

Rule:

The Netherlands is now allowed to exist as a public preview mirror, public Streamlit preview, and TID public-preview door. Do not expose the country from the shared public profile, public homepage, or cross-country surfaces until method wording, source rebuild scripting, and a separate full-launch decision are complete.
