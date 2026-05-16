# Netherlands Public Vs Internal Boundary

Public now:

- nothing

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
- no public mirror

Not ready for public:

- any public `Dutch Politics Data` app shell
- any TID room
- any public GitHub mirror
- any claim that Netherlands belongs in the public live country switch
- any cross-country comparison involving the Netherlands
- any public municipality-level reading before a factor path and method wording are tested

First internal boundary:

- start with European Netherlands municipalities
- keep Caribbean Netherlands and any special aggregate election rows out of the first factor-aware municipality layer
- keep the official `L528 / Nederland` national vote-share layer separate from the European-municipality correlation layer
- keep turnout out of the factor layer because raw `Opkomst / Kiesgerechtigden` can exceed `100%` in island municipalities
- keep `2023` and `2025` as the first national-election years
- keep older years parked until municipality-boundary drift is understood

Rule:

The Netherlands remains an internal candidate after the first adapter draft. Do not expose the country from public profiles until UI smoke, method wording, source rebuild scripting, and a separate public-readiness decision are complete.
