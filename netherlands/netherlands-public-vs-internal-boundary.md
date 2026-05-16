# Netherlands Public Vs Internal Boundary

Public now:

- public GitHub preview mirror: `netherlands-politics-data`
- public-preview app shell, once Streamlit is deployed from the mirror
- preview-level README, methodology, provenance, and normalized output files

Still not public-launched:

- no TID room
- no public homepage link
- no cross-country claim
- no public live-country switch exposure from `World-politics-data`

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

- any TID room
- any claim that Netherlands belongs in the public live country switch
- any cross-country comparison involving the Netherlands
- any final public-launch wording before the preview has passed live readback

First internal boundary:

- start with European Netherlands municipalities
- keep Caribbean Netherlands and any special aggregate election rows out of the first factor-aware municipality layer
- keep the official `L528 / Nederland` national vote-share layer separate from the European-municipality correlation layer
- keep turnout out of the factor layer because raw `Opkomst / Kiesgerechtigden` can exceed `100%` in island municipalities
- keep `2023` and `2025` as the first national-election years
- keep older years parked until municipality-boundary drift is understood

Rule:

The Netherlands is now allowed to exist as a public preview mirror. Do not expose the country from the shared public profile, add a TID door, or make cross-country claims until live preview readback, method wording, source rebuild scripting, and a separate TID-readiness decision are complete.
