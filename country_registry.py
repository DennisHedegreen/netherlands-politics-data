from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent


BASE_FACTOR_CATALOG = {'population': {'label': 'Population',
                'metric_label': 'Population (reference count)',
                'question': 'Do larger municipalities vote differently?',
                'filename': 'population.csv',
                'comparability_status': 'country_local'},
 'density': {'label': 'Population density',
             'metric_label': 'Residents per km²',
             'question': 'Does dense settlement correlate with voting '
                         'behaviour?',
             'filename': 'population_density.csv',
             'comparability_status': 'country_local'},
 'age65': {'label': 'Age 65+',
           'metric_label': 'Share aged 65+ (%)',
           'question': 'Do older municipalities vote differently?',
           'filename': 'age65_pct.csv',
           'comparability_status': 'family_mapped'},
 'education': {'label': 'Education',
               'metric_label': 'Higher education share (%)',
               'question': 'Do more educated municipalities vote differently?',
               'filename': 'education.csv',
               'comparability_status': 'family_mapped'},
 'income': {'label': 'Income',
            'metric_label': 'Avg. disposable income',
            'question': 'Do wealthier municipalities vote differently?',
            'filename': 'income.csv',
            'comparability_status': 'family_mapped'},
 'one_person_households': {'label': 'One-person households',
                           'metric_label': 'Occupied dwellings with 1 person '
                                           '(%)',
                           'question': 'Do municipalities with more one-person '
                                       'households vote differently?',
                           'filename': 'one_person_household_share_pct.csv',
                           'comparability_status': 'country_local'},
 'owner_occupied': {'label': 'Owner-occupied housing',
                    'metric_label': 'Owner-occupied occupied dwellings (%)',
                    'question': 'Do municipalities with more owner-occupied '
                                'housing vote differently?',
                    'filename': 'owner_occupied_dwelling_share_pct.csv',
                    'comparability_status': 'country_local'},
 'cars': {'label': 'Cars',
          'metric_label': 'Passenger cars per 1,000 residents',
          'question': 'Do car-heavy (rural) areas vote differently from urban '
                      'ones?',
          'filename': 'cars_per_1000.csv',
          'comparability_status': 'country_local'}}

PARTY_METADATA = {}


@dataclass(frozen=True)
class CountryConfig:
    country_id: str
    display_name: str
    adjective: str
    language: str
    statistics_source_name: str
    default_election_type: str
    election_label: str
    public_geography_type: str
    public_geography_label: str
    public_geography_label_plural: str
    public_geography_count: int
    supported_factors: tuple[str, ...]
    supported_elections: tuple[str, ...]
    internal_ready: bool
    public_ready: bool
    municipal_vote_path: Path
    national_vote_path: Path | None
    factor_dir: Path
    party_metadata: dict[str, dict[str, str]]
    source_note: str
    secondary_source_note: str | None = None

    def factor_catalog(self) -> list[dict[str, str]]:
        return [{**BASE_FACTOR_CATALOG[key], "key": key} for key in self.supported_factors]


COUNTRY = CountryConfig(
    country_id='netherlands',
    display_name='Netherlands',
    adjective='Dutch',
    language='English',
    statistics_source_name='CBS StatLine',
    default_election_type='tweede_kamer',
    election_label='Tweede Kamer election',
    public_geography_type='municipality',
    public_geography_label='municipality',
    public_geography_label_plural='municipalities',
    public_geography_count=342,
    supported_factors=('population', 'density', 'age65', 'education', 'income', 'one_person_households', 'owner_occupied', 'cars'),
    supported_elections=('tweede_kamer',),
    internal_ready=True,
    public_ready=True,
    municipal_vote_path=ROOT / "netherlands/tweede-kamer/tweede_kamer_party_share_by_municipality.csv",
    national_vote_path=ROOT / "netherlands/tweede-kamer/tweede_kamer_national_vote_share.csv",
    factor_dir=ROOT / "netherlands/factors",
    party_metadata=PARTY_METADATA,
    source_note='Kiesraad/data.overheid.nl Tweede Kamer municipality results + CBS StatLine municipal indicators',
    secondary_source_note='Public preview only; TID door is preview-labelled and there is no cross-country claim',
)


def get_country_config(country_id: str) -> CountryConfig:
    if country_id != COUNTRY.country_id:
        raise KeyError(f"Unknown country_id: {country_id}")
    return COUNTRY


def list_public_countries() -> list[CountryConfig]:
    return [COUNTRY] if COUNTRY.public_ready else []


def list_internal_countries() -> list[CountryConfig]:
    return [COUNTRY] if COUNTRY.internal_ready else []


def country_data_pack_exists(config: CountryConfig) -> bool:
    if not config.municipal_vote_path.exists():
        return False
    if not config.factor_dir.exists():
        return False
    return True


def _normalize_allowed_country_ids(allowed_country_ids: Iterable[str] | None) -> list[str] | None:
    if allowed_country_ids is None:
        return None
    return [country_id.strip().lower() for country_id in allowed_country_ids if country_id.strip()]


def list_exposed_countries(
    allowed_country_ids: Iterable[str] | None = None,
    *,
    allow_internal: bool = False,
    require_data_pack: bool = True,
) -> list[CountryConfig]:
    allowed = _normalize_allowed_country_ids(allowed_country_ids)
    if allow_internal:
        if not COUNTRY.internal_ready:
            return []
    elif not COUNTRY.public_ready:
        return []
    if allowed is None:
        if require_data_pack and not country_data_pack_exists(COUNTRY):
            return []
        return [COUNTRY]
    if COUNTRY.country_id not in allowed:
        return []
    if require_data_pack and not country_data_pack_exists(COUNTRY):
        return []
    return [COUNTRY]


def list_exposed_public_countries(
    allowed_country_ids: Iterable[str] | None = None,
    require_data_pack: bool = True,
) -> list[CountryConfig]:
    return list_exposed_countries(
        allowed_country_ids,
        allow_internal=False,
        require_data_pack=require_data_pack,
    )
