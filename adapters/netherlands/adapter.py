from __future__ import annotations

import random
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from core.correlation import compute_correlation_result, corr_strength_label
from core.presentation import (
    METRIC_SHORT_LABELS,
    PARTY_NAME_MODES,
    build_country_finding,
    format_display_table,
    format_party_name,
    render_bar_chart,
    render_compact_dataframe,
    render_country_sidebar_footer,
    render_national_trend_chart,
    render_profile_cards,
)


NETHERLANDS_LIVE_YEARS = (2023, 2025)
NETHERLANDS_DEFAULT_PARTY_MIN_MUNICIPALITIES = 25
NETHERLANDS_DEFAULT_PARTY_MIN_MEAN_SHARE = 0.5
NETHERLANDS_METRIC_OPTIONS = [
    ("population", "Population", "Population (reference count)"),
    ("density", "Population density", "Residents per km2 land"),
    ("age65", "Age 65+", "Share aged 65+ (%)"),
    ("education", "Education", "Hbo/wo highest completed education, aged 15-75 (%)"),
    ("income", "Income", "Avg. standardized household income (1,000 euro)"),
    ("one_person_households", "One-person households", "One-person households (%)"),
    ("owner_occupied", "Owner-occupied housing", "Owner-occupied dwellings (%)"),
    ("cars", "Cars", "Private passenger cars per 1,000 residents"),
]
NETHERLANDS_FACTOR_FILES = {
    "population": "population.csv",
    "density": "population_density.csv",
    "age65": "age65_pct.csv",
    "education": "education.csv",
    "income": "income.csv",
    "one_person_households": "one_person_household_share_pct.csv",
    "owner_occupied": "owner_occupied_dwelling_share_pct.csv",
    "cars": "cars_per_1000.csv",
}
NETHERLANDS_FACTOR_METHOD_NOTES = {
    "population": "CBS population on January 1.",
    "density": "CBS residents on January 1 per km2 land.",
    "age65": "Derived from CBS population by age: 65-94 plus 95+, divided by total population.",
    "education": "Hbo/wo highest completed education share for ages 15-75; CBS-null Schiermonnikoog is omitted.",
    "income": "Average standardized income for private households excluding student households; CBS-null municipalities are omitted.",
    "one_person_households": "One-person private households as a share of all private households.",
    "owner_occupied": "Owner-occupied dwellings as a share of dwellings; includes second homes in the CBS definition.",
    "cars": "Private passenger cars per 1,000 residents; company-registered cars are excluded to avoid lease-company concentration distortion.",
}
NETHERLANDS_LAGGED_FACTOR_NOTES = {
    "education": "2025 view uses 2024 source data.",
    "income": "2025 view uses 2024 source data.",
    "owner_occupied": "2025 view uses 2024 source data.",
}


def _factor_file(country_config, filename: str) -> Path:
    return country_config.factor_dir / filename


def is_available(country_config, runtime_context) -> bool:
    return country_config.municipal_vote_path.exists() and country_config.factor_dir.exists()


def build_netherlands_national(municipal: pd.DataFrame) -> pd.DataFrame:
    if municipal.empty:
        return pd.DataFrame(columns=["party", "election_year", "votes", "valid_votes", "share"])

    required = {"election_year", "public_geography_id", "party", "votes", "valid_votes"}
    if not required.issubset(municipal.columns):
        return pd.DataFrame(columns=["party", "election_year", "votes", "valid_votes", "share"])

    unique_municipality_totals = municipal.drop_duplicates(["election_year", "public_geography_id"])
    valid_by_year = unique_municipality_totals.groupby("election_year")["valid_votes"].sum()
    national = municipal.groupby(["election_year", "party"], as_index=False)["votes"].sum()
    national["valid_votes"] = national["election_year"].map(valid_by_year)
    national["share"] = (national["votes"] / national["valid_votes"] * 100).round(4)
    return national[["party", "election_year", "votes", "valid_votes", "share"]].sort_values(
        ["election_year", "share", "votes"],
        ascending=[True, False, False],
    ).reset_index(drop=True)


def load_netherlands_national(country_config, municipal: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    if country_config.national_vote_path and country_config.national_vote_path.exists():
        national = pd.read_csv(country_config.national_vote_path)
        national["election_year"] = national["election_year"].astype(int)
        national["share"] = pd.to_numeric(national["share"], errors="coerce")
        national["votes"] = pd.to_numeric(national["votes"], errors="coerce")
        national["valid_votes"] = pd.to_numeric(national["valid_votes"], errors="coerce")
        return national, "official_land_total"
    return build_netherlands_national(municipal), "derived_european_municipality_sum"


@st.cache_data
def load_bundle(country_config):
    municipal = pd.read_csv(country_config.municipal_vote_path)
    municipal["election_year"] = municipal["election_year"].astype(int)
    municipal["share"] = pd.to_numeric(municipal["share"], errors="coerce")
    municipal["votes"] = pd.to_numeric(municipal["votes"], errors="coerce")
    municipal["valid_votes"] = pd.to_numeric(municipal["valid_votes"], errors="coerce")

    factor_frames = {}
    for metric_key in country_config.supported_factors:
        filename = NETHERLANDS_FACTOR_FILES.get(metric_key)
        if filename is None:
            continue
        path = _factor_file(country_config, filename)
        frame = pd.read_csv(path) if path.exists() else pd.DataFrame(columns=["municipality", "public_geography_id", "year", "value"])
        if not frame.empty:
            frame["year"] = frame["year"].astype(int)
            frame["value"] = pd.to_numeric(frame["value"], errors="coerce")
        factor_frames[metric_key] = frame

    national, national_source_scope = load_netherlands_national(country_config, municipal)
    return {
        "municipal": municipal,
        "national": national,
        "national_source_scope": national_source_scope,
        "factor_frames": factor_frames,
    }


def _get_metric_series(metric_key, year, factor_frames):
    frame = factor_frames.get(metric_key, pd.DataFrame())
    if frame.empty:
        return pd.DataFrame(columns=["public_geography_id", "metric"])
    current = frame[frame["year"] == year][["public_geography_id", "value"]].copy()
    if current.empty:
        return pd.DataFrame(columns=["public_geography_id", "metric"])
    current["metric"] = pd.to_numeric(current["value"], errors="coerce")
    return current[["public_geography_id", "metric"]].dropna(subset=["metric"])


def _metric_label(metric_key: str) -> str:
    for key, _label, metric_label in NETHERLANDS_METRIC_OPTIONS:
        if key == metric_key:
            return metric_label
    return metric_key


def _factor_reference_period(metric_key: str, year: int, factor_frames) -> str:
    frame = factor_frames.get(metric_key, pd.DataFrame())
    if frame.empty or "reference_period" not in frame.columns:
        return str(year)
    current = frame[frame["year"] == year]
    if current.empty:
        return str(year)
    refs = current["reference_period"].dropna().astype(str).unique().tolist()
    return refs[0] if refs else str(year)


def _append_factor_source_pointer(note: str) -> str:
    return f"{note} · Factor source notes are documented in About & sources."


def _metric_items_for_year(year, factor_frames):
    return [
        (key, label, metric_label)
        for key, label, metric_label in NETHERLANDS_METRIC_OPTIONS
        if not _get_metric_series(key, year, factor_frames).empty
    ]


def _municipality_sort_key(name: str) -> str:
    return str(name).lower().replace("'", "").replace("-", " ")


def _preferred_index(options: list[str], preferred: str, fallback: int = 0) -> int:
    if preferred in options:
        return options.index(preferred)
    if not options:
        return 0
    return min(fallback, len(options) - 1)


def _party_options(municipal_df, year):
    year_frame = municipal_df[municipal_df["election_year"] == year].copy()
    if year_frame.empty:
        return []
    profiles = get_netherlands_party_profiles(year_frame)
    return profiles["party"].tolist()


def get_netherlands_party_profiles(municipal_df):
    if municipal_df.empty:
        return pd.DataFrame(columns=["party", "municipality_count", "mean_share", "default_public"])
    stats = (
        municipal_df[municipal_df["share"] > 0]
        .groupby("party", as_index=False)
        .agg(
            municipality_count=("municipality", "nunique"),
            mean_share=("share", "mean"),
        )
    )
    stats["default_public"] = (
        (stats["municipality_count"] >= NETHERLANDS_DEFAULT_PARTY_MIN_MUNICIPALITIES)
        & (stats["mean_share"] >= NETHERLANDS_DEFAULT_PARTY_MIN_MEAN_SHARE)
    )
    return stats.sort_values(
        ["default_public", "mean_share", "municipality_count"],
        ascending=[False, False, False],
    ).reset_index(drop=True)


def ordered_netherlands_national_parties(national_df):
    if national_df.empty:
        return []
    latest_year = int(national_df["election_year"].max())
    latest = national_df[national_df["election_year"] == latest_year].copy()
    latest["share"] = pd.to_numeric(latest["share"], errors="coerce")
    latest = latest.dropna(subset=["share"]).sort_values("share", ascending=False)
    ordered = latest["party"].tolist()
    remainder = sorted([party for party in national_df["party"].dropna().unique().tolist() if party not in ordered])
    return ordered + remainder


def top_netherlands_national_parties(national_df, top_n=5):
    if national_df.empty:
        return []
    latest_year = int(national_df["election_year"].max())
    latest = national_df[national_df["election_year"] == latest_year].copy()
    latest["share"] = pd.to_numeric(latest["share"], errors="coerce")
    latest = latest.dropna(subset=["share"]).sort_values("share", ascending=False)
    return latest["party"].head(top_n).tolist()


def _factor_rows(factor_frames):
    rows = []
    for key, label, _metric_text in NETHERLANDS_METRIC_OPTIONS:
        frame = factor_frames.get(key, pd.DataFrame())
        years = sorted(frame["year"].dropna().astype(int).unique().tolist()) if not frame.empty else []
        references = sorted(frame["reference_period"].dropna().astype(str).unique().tolist()) if not frame.empty and "reference_period" in frame else []
        status = "Internal candidate" if years else "Missing"
        rows.append(
            {
                "Factor": label,
                "Visible in live picker": "Yes" if years else "No",
                "Years": ", ".join(str(year) for year in years) or "-",
                "Source periods": ", ".join(references) or "-",
                "Rows": len(frame),
                "Status": status,
                "Method boundary": NETHERLANDS_FACTOR_METHOD_NOTES.get(key, ""),
            }
        )
    return rows


def _result_divider():
    st.markdown(
        "<div style='margin:2rem 0 0.5rem;border-top:2px solid #0d0d14;'>"
        "<span style='font-size:0.58rem;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;"
        "color:#0d0d14;background:#f5f5f7;padding:0 0.6rem;position:relative;top:-0.7rem;'>RESULT</span>"
        "</div>",
        unsafe_allow_html=True,
    )


def _finding_html(strength_cls, strength_tag, headline, concrete, copy_sentence, note, context_label=None):
    context = f'<div class="copy-label" style="margin-bottom:0.3rem;">{context_label}</div>' if context_label else ""
    copy_block = ""
    if copy_sentence:
        copy_label = "Use with caution:" if strength_tag.startswith("WEAK PATTERN") else "Write this as:"
        copy_block = f'<div class="copy-label">{copy_label}</div><div class="copy-box">{copy_sentence}</div>'
    return (
        f'<div class="finding {strength_cls}">'
        f'<div class="strength-tag">{strength_tag}</div>'
        f'{context}'
        f'<div class="headline">{headline}</div>'
        f'<div class="body">{concrete}</div>'
        f'{copy_block}'
        f'<div class="footnote">{note}</div>'
        f'</div>'
    )


def _how_to_read():
    with st.expander("How to read this result"):
        st.markdown(
            """
**STRONG PATTERN (abs(r) >= 0.70)** - The municipality-level relationship is clear enough to describe directly.
**MODERATE PATTERN (abs(r) 0.50-0.70)** - There is a consistent tendency, but it is still not an explanation.
**WEAK PATTERN (abs(r) 0.30-0.50)** - Use with caution. It is a weak municipality-level association.
**NO PATTERN (abs(r) below 0.30)** - Do not write a pattern claim.

Positive r = both rise together. Negative r = they move in opposite directions.

*Correlation is not cause. The point is to describe the visible municipality-level pattern honestly.*
            """
        )


def _format_party(party, country_config, party_name_mode, *, compact=False, prose=False):
    return format_party_name(
        party,
        metadata=country_config.party_metadata,
        mode=party_name_mode,
        compact=compact,
        prose=prose,
    )


def render(country_config, selected_country_label, runtime_context):
    bundle = load_bundle(country_config)
    municipal = bundle["municipal"]
    national = bundle["national"]
    national_source_scope = bundle["national_source_scope"]
    factor_frames = bundle["factor_frames"]
    years = sorted(year for year in municipal["election_year"].dropna().astype(int).unique().tolist() if year in NETHERLANDS_LIVE_YEARS)
    available_municipalities = sorted(municipal["municipality"].dropna().unique().tolist(), key=_municipality_sort_key)

    with st.sidebar:
        st.markdown('<div class="hr-wordmark">HEDEGREEN RESEARCH<span class="dot"> ●</span></div>', unsafe_allow_html=True)
        st.markdown("**Dutch Politics Data**")
        st.markdown(
            "<p style='font-size:0.75rem;color:#6a6a7a;line-height:1.6;margin-top:0.3rem;'>"
            "Public Netherlands preview. Tweede Kamer 2023/2025, European municipalities only, with eight CBS structural factors."
            "</p>",
            unsafe_allow_html=True,
        )
        st.divider()
        party_name_mode = st.selectbox("Party names", PARTY_NAME_MODES, index=0, key="netherlands_party_name_mode")
        st.divider()
        page_options = ["Explore", "Compare municipalities", "By Municipality"]
        if not national.empty:
            page_options.append("National trends")
        page_options.append("About & sources")
        page = st.radio(
            "nav",
            page_options,
            label_visibility="collapsed",
            key="netherlands_page",
        )
        st.divider()
        render_country_sidebar_footer(country_config)

    if municipal.empty or not years:
        st.error("The internal Netherlands data pack is not available yet.")
        return

    if page == "Explore":
        if "netherlands_explore_show" not in st.session_state:
            st.session_state["netherlands_explore_show"] = False
        if "netherlands_all_parties" not in st.session_state:
            st.session_state["netherlands_all_parties"] = True
        if st.session_state.pop("netherlands_pending_explore_show", False):
            st.session_state["netherlands_explore_show"] = True

        st.markdown(
            "<p style='font-size:0.65rem;font-weight:500;letter-spacing:0.12em;text-transform:uppercase;color:#aaaabc;margin-bottom:0.2rem;'>"
            "Dutch Politics Data</p>",
            unsafe_allow_html=True,
        )
        st.title("Is there a pattern?")
        st.markdown(
            "<p style='font-size:0.95rem;color:#5a5a6a;margin-bottom:2rem;'>"
            "Pick one or more factors, one or more parties, and an election year. Then find out."
            "</p>",
            unsafe_allow_html=True,
        )

        st.markdown('<div class="step-label">Step 1 — Which election year?</div>', unsafe_allow_html=True)
        year = st.select_slider(
            "year",
            options=years,
            value=years[-1],
            key="netherlands_year",
            label_visibility="collapsed",
        )
        municipal_year = municipal[municipal["election_year"] == year].copy()

        metric_items = _metric_items_for_year(year, factor_frames)
        metric_labels = [label for _, label, _ in metric_items]
        pending_factors = st.session_state.pop("netherlands_pending_cx_factors", None)
        if pending_factors is not None:
            st.session_state["netherlands_cx_factors"] = [label for label in pending_factors if label in metric_labels]
        if "netherlands_cx_factors" not in st.session_state:
            st.session_state["netherlands_cx_factors"] = ["Income"] if "Income" in metric_labels else metric_labels[:1]
        current_factors = [label for label in st.session_state.get("netherlands_cx_factors", []) if label in metric_labels]
        if not current_factors and metric_labels:
            current_factors = [metric_labels[0]]
        st.session_state["netherlands_cx_factors"] = current_factors

        factor_label_to_key = {label: key for key, label, _ in metric_items}
        st.markdown('<div class="step-label" style="margin-top:1rem;">Step 2 — What factors are available for that year?</div>', unsafe_allow_html=True)
        selected_metric_labels = st.pills(
            "netherlands-factors",
            metric_labels,
            key="netherlands_cx_factors",
            selection_mode="multi",
            label_visibility="collapsed",
        )
        if not selected_metric_labels:
            st.markdown(
                "<p style='font-size:0.74rem;color:#8888a0;margin-bottom:0;'>"
                "No factor is currently selected. Municipality-level pattern analysis requires at least one factor."
                "</p>",
                unsafe_allow_html=True,
            )

        party_profiles = get_netherlands_party_profiles(municipal_year)
        all_party_options = party_profiles["party"].tolist()
        default_public_parties = party_profiles.loc[party_profiles["default_public"], "party"].tolist()
        st.markdown('<div class="step-label" style="margin-top:1rem;">Step 3 — Pick a party</div>', unsafe_allow_html=True)
        include_low_coverage = st.checkbox(
            "Show smaller parties too",
            key="netherlands_include_low_coverage",
            help="Default internal view keeps only parties with at least 25 municipalities and at least 0.5% mean municipality vote share.",
        )
        party_options = all_party_options if include_low_coverage else default_public_parties
        pending_all_parties = st.session_state.pop("netherlands_pending_all_parties", None)
        if pending_all_parties is not None:
            st.session_state["netherlands_all_parties"] = bool(pending_all_parties)
        pending_parties = st.session_state.pop("netherlands_pending_parties", None)
        if pending_parties is not None:
            st.session_state["netherlands_parties"] = [party for party in pending_parties if party in party_options]
        if "netherlands_parties" not in st.session_state:
            st.session_state["netherlands_parties"] = party_options[:5]
        current_selected = [party for party in st.session_state.get("netherlands_parties", []) if party in party_options]
        if not current_selected:
            current_selected = party_options[:] if st.session_state.get("netherlands_all_parties") else party_options[:1]
        st.session_state["netherlands_parties"] = current_selected
        select_all = st.checkbox("All parties", key="netherlands_all_parties")
        if select_all:
            selected_parties = party_options
            st.session_state["netherlands_parties"] = party_options
        else:
            selected_parties = st.pills(
                "netherlands-parties",
                party_options,
                key="netherlands_parties",
                selection_mode="multi",
                format_func=lambda party: _format_party(party, country_config, party_name_mode, compact=True),
                label_visibility="collapsed",
            )
            if not selected_parties:
                st.markdown(
                    "<p style='font-size:0.74rem;color:#8888a0;margin-top:0.45rem;margin-bottom:0;'>"
                    "No party is currently selected. Municipality-level pattern analysis requires at least one party selection."
                    "</p>",
                    unsafe_allow_html=True,
                )
        st.markdown(
            "<p style='font-size:0.72rem;color:#8888a0;margin-top:0.35rem;margin-bottom:0;'>"
            "Default party view filters out micro-parties and very small lists.</p>",
            unsafe_allow_html=True,
        )

        st.markdown('<div class="step-label" style="margin-top:1rem;">Step 4 — Highlight a specific municipality? (optional)</div>', unsafe_allow_html=True)
        highlight_choice = st.selectbox(
            "Highlight municipality",
            ["— none —"] + available_municipalities,
            key="netherlands_highlight",
            label_visibility="collapsed",
        )
        highlight_municipality = None if highlight_choice == "— none —" else highlight_choice

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        def precompute_netherlands_correlations():
            rows = []
            for party in default_public_parties:
                votes = municipal_year[municipal_year["party"] == party][["public_geography_id", "municipality", "share"]]
                for metric_label in metric_labels:
                    metric_key = factor_label_to_key[metric_label]
                    metric_series = _get_metric_series(metric_key, year, factor_frames)
                    if metric_series.empty:
                        continue
                    merged = votes.merge(metric_series, on="public_geography_id", how="inner")
                    computed = compute_correlation_result(
                        merged,
                        factor=metric_label,
                        party=party,
                        year=year,
                        mode="precompute-netherlands",
                    )
                    if computed["valid"]:
                        rows.append(
                            {
                                "party": party,
                                "factor": metric_label,
                                "r": computed["r"],
                            }
                        )
            return pd.DataFrame(rows)

        col_main, col_surprise = st.columns([3, 1])
        with col_main:
            if st.button("Show me what the data reveals →", type="primary", width="stretch", key="netherlands_show"):
                st.session_state["netherlands_explore_show"] = True
        with col_surprise:
            if st.button("Surprise me →", width="stretch", key="netherlands_surprise"):
                interesting = precompute_netherlands_correlations()
                interesting = interesting[interesting["r"].abs() >= 0.40] if not interesting.empty else interesting
                if not interesting.empty:
                    mode = random.choice(["single", "multi_factor", "multi_party"])
                    anchor = interesting.sample(1).iloc[0]
                    if mode == "single":
                        factors = [anchor["factor"]]
                        parties = [anchor["party"]]
                    elif mode == "multi_factor":
                        same = interesting[interesting["party"] == anchor["party"]].copy()
                        same = same.reindex(same["r"].abs().sort_values(ascending=False).index)
                        factors = same["factor"].tolist()[:3] if len(same) >= 2 else [anchor["factor"]]
                        parties = [anchor["party"]]
                    else:
                        same = interesting[interesting["factor"] == anchor["factor"]].copy()
                        same = same.reindex(same["r"].abs().sort_values(ascending=False).index)
                        factors = [anchor["factor"]]
                        parties = same["party"].tolist()[:3] if len(same) >= 2 else [anchor["party"]]
                    st.session_state["netherlands_pending_cx_factors"] = factors
                    st.session_state["netherlands_pending_parties"] = parties
                    st.session_state["netherlands_pending_all_parties"] = False
                    st.session_state["netherlands_pending_explore_show"] = True
                    st.rerun()

        if not st.session_state.get("netherlands_explore_show"):
            return

        if not selected_metric_labels or not selected_parties:
            st.markdown(
                '<div class="finding weak">'
                '<div class="strength-tag">SELECTION INCOMPLETE</div>'
                '<div class="headline">This analysis cannot run yet.</div>'
                '<div class="body">Netherlands municipality-level correlation requires at least one factor and at least one party selection.</div>'
                '</div>',
                unsafe_allow_html=True,
            )
            return

        results = []
        for party in selected_parties:
            votes = municipal_year[municipal_year["party"] == party][["public_geography_id", "municipality", "share"]]
            for metric_label in selected_metric_labels:
                metric_key = factor_label_to_key[metric_label]
                metric_series = _get_metric_series(metric_key, year, factor_frames)
                merged = votes.merge(metric_series, on="public_geography_id", how="inner")
                computed = compute_correlation_result(
                    merged,
                    factor=metric_label,
                    party=party,
                    year=year,
                    mode="explore-netherlands",
                )
                results.append(
                    {
                        "party": party,
                        "factor": metric_label,
                        "metric_key": metric_key,
                        "label": _metric_label(metric_key),
                        "r": computed["r"],
                        "merged": computed["merged"],
                        "valid": computed["valid"],
                        "strength": corr_strength_label(computed["r"]),
                    }
                )

        valid_results = [row for row in results if row["valid"]]
        if not valid_results:
            st.markdown(
                '<div class="finding weak">'
                '<div class="strength-tag">NO VALID RESULT</div>'
                '<div class="headline">No valid Netherlands result is available.</div>'
                '<div class="body">The current selection did not produce a reliable municipality-level correlation value.</div>'
                '</div>',
                unsafe_allow_html=True,
            )
            return

        _result_divider()

        if len(selected_parties) == 1 and len(selected_metric_labels) == 1:
            row = valid_results[0]
            strength_cls, strength_tag, headline, concrete, copy_sentence, note = build_country_finding(
                row["r"],
                row["factor"],
                row["label"],
                row["party"],
                year,
                row["merged"],
                party_name_mode,
                country_config,
            )
            note = _append_factor_source_pointer(note)
            st.markdown(
                _finding_html(strength_cls, strength_tag, headline, concrete, copy_sentence, note),
                unsafe_allow_html=True,
            )
            _how_to_read()

            scatter_df = row["merged"].copy()
            scatter_df["highlight"] = scatter_df["municipality"].eq(highlight_municipality)
            scatter = alt.Chart(scatter_df).mark_circle(size=62).encode(
                x=alt.X("metric:Q", title=row["label"]),
                y=alt.Y(
                    "share:Q",
                    title=f"Vote share · {_format_party(row['party'], country_config, party_name_mode, prose=True)}",
                ),
                color=alt.condition(alt.datum.highlight, alt.value("#ef4444"), alt.value("#22d966")),
                tooltip=[
                    alt.Tooltip("municipality:N", title="Municipality"),
                    alt.Tooltip("metric:Q", title=row["label"], format=".2f"),
                    alt.Tooltip("share:Q", title="Vote share", format=".2f"),
                ],
            )
            st.altair_chart(scatter, width="stretch")

            metric_short = METRIC_SHORT_LABELS.get(row["factor"], row["label"])
            ranked = row["merged"].sort_values("metric").rename(
                columns={
                    "municipality": "Municipality",
                    "metric": metric_short,
                    "share": "Vote share",
                }
            )
            if highlight_municipality:
                highlight = ranked[ranked["Municipality"] == highlight_municipality]
                if not highlight.empty:
                    st.caption(f"Highlighted municipality: {highlight_municipality}")
                    render_compact_dataframe(highlight[["Municipality", metric_short, "Vote share"]])
            tab_lo, tab_hi = st.tabs([f"Lowest {metric_short}", f"Highest {metric_short}"])
            with tab_lo:
                render_compact_dataframe(ranked.head(10)[["Municipality", metric_short, "Vote share"]])
            with tab_hi:
                render_compact_dataframe(ranked.tail(10).sort_values(metric_short, ascending=False)[["Municipality", metric_short, "Vote share"]])

        elif len(selected_parties) == 1 and len(selected_metric_labels) > 1:
            ranked = sorted(valid_results, key=lambda row: abs(float(row["r"])), reverse=True)
            summary = pd.DataFrame(
                [{"Factor": row["factor"], "Label": row["factor"], "r": row["r"], "Strength": row["strength"]} for row in ranked]
            )
            st.markdown(
                "<p style='font-size:0.75rem;color:#aaaabc;margin-bottom:0.3rem;'>"
                "Results are ranked by correlation strength (absolute value). Positive = more votes where factor is higher. Negative = more votes where factor is lower.</p>",
                unsafe_allow_html=True,
            )
            render_bar_chart(summary, "Label", "r", tooltip_label="Factor", full_label_col="Factor")
            meaningful = [row for row in ranked if abs(float(row["r"])) >= 0.30] or ranked[:1]
            no_pattern = [row for row in ranked if abs(float(row["r"])) < 0.30]
            for row in meaningful:
                strength_cls, strength_tag, headline, concrete, copy_sentence, note = build_country_finding(
                    row["r"], row["factor"], row["label"], row["party"], year, row["merged"], party_name_mode, country_config
                )
                note = _append_factor_source_pointer(note)
                st.markdown(_finding_html(strength_cls, strength_tag, headline, concrete, copy_sentence, note), unsafe_allow_html=True)
            if no_pattern:
                st.markdown(
                    f"<p style='font-size:0.75rem;color:#aaaabc;margin-top:0.5rem;'>No pattern found for: {', '.join(row['factor'] for row in no_pattern)} (abs(r) below 0.30).</p>",
                    unsafe_allow_html=True,
                )
            _how_to_read()
            with st.expander("See full ranking table"):
                render_compact_dataframe(summary[["Factor", "r", "Strength"]])

        elif len(selected_parties) > 1 and len(selected_metric_labels) == 1:
            ranked = sorted(valid_results, key=lambda row: abs(float(row["r"])), reverse=True)
            summary = pd.DataFrame(
                [
                    {
                        "Party": _format_party(row["party"], country_config, party_name_mode, compact=True),
                        "Party_full": _format_party(row["party"], country_config, party_name_mode),
                        "r": row["r"],
                        "Strength": row["strength"],
                    }
                    for row in ranked
                ]
            )
            st.markdown(
                "<p style='font-size:0.75rem;color:#aaaabc;margin-bottom:0.3rem;'>"
                "Results are ranked by correlation strength (absolute value). Positive = more votes where factor is higher. Negative = more votes where factor is lower.</p>",
                unsafe_allow_html=True,
            )
            render_bar_chart(summary, "Party", "r", tooltip_label="Party", full_label_col="Party_full")
            meaningful = [row for row in ranked if abs(float(row["r"])) >= 0.30] or ranked[:1]
            no_pattern = [row for row in ranked if abs(float(row["r"])) < 0.30]
            for row in meaningful:
                strength_cls, strength_tag, headline, concrete, copy_sentence, note = build_country_finding(
                    row["r"], row["factor"], row["label"], row["party"], year, row["merged"], party_name_mode, country_config
                )
                note = _append_factor_source_pointer(note)
                st.markdown(_finding_html(strength_cls, strength_tag, headline, concrete, copy_sentence, note), unsafe_allow_html=True)
            if no_pattern:
                st.markdown(
                    f"<p style='font-size:0.75rem;color:#aaaabc;margin-top:0.5rem;'>No pattern found for: {', '.join(_format_party(row['party'], country_config, party_name_mode, compact=True) for row in no_pattern)} (abs(r) below 0.30).</p>",
                    unsafe_allow_html=True,
                )
            _how_to_read()
            with st.expander("See full ranking table"):
                render_compact_dataframe(summary[["Party_full", "r", "Strength"]], rename_map={"Party_full": "Party"})

        else:
            top = max(valid_results, key=lambda item: abs(float(item["r"])))
            strength_cls, strength_tag, headline, concrete, copy_sentence, note = build_country_finding(
                top["r"],
                top["factor"],
                top["label"],
                top["party"],
                year,
                top["merged"],
                party_name_mode,
                country_config,
            )
            note = _append_factor_source_pointer(note)
            st.markdown(
                "<p style='font-size:0.75rem;color:#aaaabc;margin-bottom:0.5rem;'>"
                "Showing highest correlation across selected factors and parties. Use the full correlation table to inspect all results.</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                _finding_html(
                    strength_cls,
                    strength_tag,
                    headline,
                    concrete,
                    copy_sentence,
                    note,
                    context_label=f"Strongest signal: {_format_party(top['party'], country_config, party_name_mode, compact=True)} x {top['factor']}",
                ),
                unsafe_allow_html=True,
            )
            _how_to_read()
            with st.expander("See full correlation table"):
                flat_df = pd.DataFrame(
                    [
                        {
                            "Party": _format_party(row["party"], country_config, party_name_mode),
                            "Factor": row["factor"],
                            "r": row["r"],
                            "Strength": row["strength"],
                        }
                        for row in valid_results
                    ]
                ).assign(abs_r=lambda frame: frame["r"].abs()).sort_values("abs_r", ascending=False).drop(columns="abs_r")
                render_compact_dataframe(flat_df)

    elif page == "Compare municipalities":
        st.markdown(
            "<p style='font-size:0.65rem;font-weight:500;letter-spacing:0.12em;text-transform:uppercase;color:#aaaabc;margin-bottom:0.2rem;'>"
            "Dutch Politics Data</p>",
            unsafe_allow_html=True,
        )
        st.title("Compare two municipalities")
        st.markdown(
            "<p style='font-size:0.95rem;color:#5a5a6a;margin-bottom:1.5rem;'>"
            "Pick two municipalities and compare their party profile and CBS factor layer for the selected election year."
            "</p>",
            unsafe_allow_html=True,
        )
        compare_year = st.selectbox("Election year", years, index=len(years) - 1, key="netherlands_compare_year")
        compare_votes = municipal[municipal["election_year"] == compare_year].copy()
        municipalities_for_year = sorted(compare_votes["municipality"].dropna().unique().tolist(), key=_municipality_sort_key)
        col1, col2 = st.columns(2)
        with col1:
            mun_a = st.selectbox(
                "Municipality A",
                municipalities_for_year,
                index=_preferred_index(municipalities_for_year, "Amsterdam"),
                key="netherlands_compare_a",
            )
        with col2:
            mun_b = st.selectbox(
                "Municipality B",
                municipalities_for_year,
                index=_preferred_index(municipalities_for_year, "Rotterdam", fallback=1),
                key="netherlands_compare_b",
            )
        if mun_a == mun_b:
            st.warning("Select two different municipalities.")
            return

        st.markdown("## Voting patterns")
        votes_a = compare_votes[compare_votes["municipality"] == mun_a].set_index("party")["share"]
        votes_b = compare_votes[compare_votes["municipality"] == mun_b].set_index("party")["share"]
        common = votes_a.index.intersection(votes_b.index)
        if len(common):
            gap_series = (votes_a[common] - votes_b[common]).sort_values(key=lambda series: series.abs(), ascending=False)
            top_parties = gap_series.head(8).index.tolist()
            gap_chart_df = pd.DataFrame(
                {
                    "Party": [_format_party(party, country_config, party_name_mode, compact=True) for party in top_parties],
                    "Party_full": [_format_party(party, country_config, party_name_mode) for party in top_parties],
                    "Gap": [float(gap_series[party]) for party in top_parties],
                }
            )
            st.markdown(
                f"<p style='font-size:0.82rem;color:#6a6a7a;margin-bottom:0.5rem;'>"
                f"Percentage point gap in vote share: <strong>{mun_a}</strong> minus <strong>{mun_b}</strong>. "
                f"Positive bar = {mun_a} votes more for that party. Negative = {mun_b} does.</p>",
                unsafe_allow_html=True,
            )
            render_bar_chart(gap_chart_df, "Party", "Gap", tooltip_label="Party", full_label_col="Party_full")
            biggest_party = gap_series.index[0]
            biggest_gap = float(gap_series.iloc[0])
            direction = mun_a if biggest_gap > 0 else mun_b
            st.markdown(
                f'<div class="finding moderate">'
                f'<div class="headline">Biggest difference: {_format_party(biggest_party, country_config, party_name_mode, prose=True)}</div>'
                f'<div class="body"><strong>{direction}</strong> is currently <strong>{abs(biggest_gap):.1f} percentage points</strong> higher on this party in the Netherlands {compare_year} municipality layer.</div>'
                f'<div class="footnote">Tweede Kamer {compare_year} · internal municipality candidate · {country_config.source_note}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            with st.expander("See full vote snapshot for both municipalities"):
                display_parties = gap_series.index.tolist()
                tab_a, tab_b = st.tabs([mun_a, mun_b])
                with tab_a:
                    votes_a_display = votes_a[display_parties].round(2).reset_index()
                    votes_a_display["party"] = votes_a_display["party"].apply(lambda value: _format_party(value, country_config, party_name_mode))
                    render_compact_dataframe(votes_a_display.rename(columns={"party": "Party", "share": "Vote %"}))
                with tab_b:
                    votes_b_display = votes_b[display_parties].round(2).reset_index()
                    votes_b_display["party"] = votes_b_display["party"].apply(lambda value: _format_party(value, country_config, party_name_mode))
                    render_compact_dataframe(votes_b_display.rename(columns={"party": "Party", "share": "Vote %"}))

        st.markdown("## Current factor profile")
        st.markdown(
            "<p style='font-size:0.82rem;color:#6a6a7a;margin-bottom:0.8rem;'>"
            "Factor profile using the selected election year. Detailed source periods and method boundaries are documented in About & sources.</p>",
            unsafe_allow_html=True,
        )
        geo_lookup = compare_votes.drop_duplicates("municipality").set_index("municipality")["public_geography_id"]
        geo_a = geo_lookup.get(mun_a)
        geo_b = geo_lookup.get(mun_b)
        cards = []
        for metric_key, label, _metric_text in _metric_items_for_year(compare_year, factor_frames):
            metric_series = _get_metric_series(metric_key, compare_year, factor_frames)
            left_value = metric_series.loc[metric_series["public_geography_id"] == geo_a, "metric"]
            right_value = metric_series.loc[metric_series["public_geography_id"] == geo_b, "metric"]
            cards.append(
                {
                    "Metric": label,
                    mun_a: f"{left_value.iloc[0]:.2f}" if not left_value.empty else "—",
                    mun_b: f"{right_value.iloc[0]:.2f}" if not right_value.empty else "—",
                    "Year": str(compare_year),
                }
            )
        render_profile_cards(cards, mun_a, mun_b)

    elif page == "By Municipality":
        st.markdown(
            "<p style='font-size:0.65rem;font-weight:500;letter-spacing:0.12em;text-transform:uppercase;color:#aaaabc;margin-bottom:0.2rem;'>"
            "Dutch Politics Data</p>",
            unsafe_allow_html=True,
        )
        st.title("By Municipality")
        st.markdown(
            "<p style='font-size:0.95rem;color:#5a5a6a;margin-bottom:1.5rem;'>"
            "Pick a party and a year. See where that party was strongest and weakest across European Netherlands municipalities."
            "</p>",
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)
        with col1:
            year = st.selectbox("Election year", years, index=len(years) - 1, key="netherlands_muni_year")
        with col2:
            party_options = _party_options(municipal, year)
            party = st.selectbox(
                "Party",
                party_options,
                format_func=lambda value: _format_party(value, country_config, party_name_mode),
                key="netherlands_single_party",
            )
        municipal_year = municipal[municipal["election_year"] == year].copy()
        filtered = municipal_year[municipal_year["party"] == party].sort_values("share", ascending=False)
        if filtered.empty:
            st.warning("No municipality rows are available for this selection.")
            return
        top = filtered.iloc[0]
        bottom = filtered.iloc[-1]
        avg = filtered["share"].mean()
        party_label = _format_party(party, country_config, party_name_mode, prose=True)
        st.markdown(
            f"<p style='font-size:0.86rem;color:#3a3a4a;margin-bottom:0.35rem;'>"
            f"In <strong>{year}</strong>, <strong>{party_label}</strong> had its highest municipality share in "
            f"<strong>{top['municipality']}</strong> ({top['share']:.1f}%) and its lowest in "
            f"<strong>{bottom['municipality']}</strong> ({bottom['share']:.1f}%). "
            f"The unweighted municipality average was <strong>{avg:.1f}%</strong>.</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='font-size:0.74rem;color:#8888a0;margin-bottom:0.8rem;'>"
            "The table is sorted by local vote share. `Vote %` is the party's share of valid votes in that municipality, not the national result.</p>",
            unsafe_allow_html=True,
        )
        display = filtered[["municipality", "province", "votes", "valid_votes", "share"]].rename(
            columns={
                "municipality": "Municipality",
                "province": "Province",
                "votes": "Votes",
                "valid_votes": "Valid votes",
                "share": "Vote %",
            }
        )
        render_compact_dataframe(display)
        with st.expander("Show full municipality ranking chart"):
            render_bar_chart(
                filtered.assign(municipality_label=filtered["municipality"]),
                "municipality_label",
                "share",
                tooltip_label="Municipality",
                full_label_col="municipality",
            )

    elif page == "National trends":
        st.markdown(
            "<p style='font-size:0.65rem;font-weight:500;letter-spacing:0.12em;text-transform:uppercase;color:#aaaabc;margin-bottom:0.2rem;'>"
            "Dutch Politics Data</p>",
            unsafe_allow_html=True,
        )
        st.title("National trends")
        if national_source_scope == "official_land_total":
            st.markdown(
                "<p style='font-size:0.95rem;color:#5a5a6a;margin-bottom:1.5rem;'>"
                "Official national vote-share view from the `L528 / Nederland` rows in the internal 2023 and 2025 Kiesraad source packages."
                "</p>",
                unsafe_allow_html=True,
            )
            st.info(
                "Official source scope: this view uses the national land-total rows from TK2023_uitslag.csv and TK2025_uitslag.csv. "
                "That includes the source's national scope, while the pattern explorer remains limited to European Netherlands municipalities."
            )
        else:
            st.markdown(
                "<p style='font-size:0.95rem;color:#5a5a6a;margin-bottom:1.5rem;'>"
                "Derived national vote-share view from the internal 2023 and 2025 municipality result layer."
                "</p>",
                unsafe_allow_html=True,
            )
            st.info(
                "Derived view only: this page sums municipality rows from the internal candidate file. "
                "It is not a separate official national-summary harvest yet."
            )
        parties_nat = ordered_netherlands_national_parties(national)
        default_nat = [party for party in top_netherlands_national_parties(national, top_n=5) if party in parties_nat]
        selected = st.multiselect(
            "Parties",
            parties_nat,
            default=default_nat,
            format_func=lambda party: _format_party(party, country_config, party_name_mode, compact=True),
            key="netherlands_national_parties",
        )
        if selected:
            chart_df = national[national["party"].isin(selected)].copy()
            chart_df["party_label"] = chart_df["party"].apply(lambda party: _format_party(party, country_config, party_name_mode, compact=True))
            pivot = chart_df.pivot_table(index="election_year", columns="party_label", values="share")
            render_national_trend_chart(chart_df, "election_year", "party_label", "share")
            st.dataframe(format_display_table(pivot, decimals=2), width="stretch")
        if national_source_scope == "official_land_total":
            st.markdown(
                "<p style='font-size:0.72rem;color:#8888a0;margin-top:0.8rem;'>"
                "Source: L528 Nederland rows in the Kiesraad/data.overheid.nl research CSV packages. This is a national land-total view, not the same geography scope as the European-municipality correlation layer.</p>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<p style='font-size:0.72rem;color:#8888a0;margin-top:0.8rem;'>"
                "This is a derived convenience view, not a separate official national trend harvest yet. It sums municipality party votes and divides by one unique valid-vote denominator per municipality.</p>",
                unsafe_allow_html=True,
            )

    else:
        st.markdown(
            "<p style='font-size:0.65rem;font-weight:500;letter-spacing:0.12em;text-transform:uppercase;color:#aaaabc;margin-bottom:0.2rem;'>"
            "Dutch Politics Data</p>",
            unsafe_allow_html=True,
        )
        st.title("About & sources")
        st.markdown(
            f"""
Tweede Kamer results for 2023 and 2025 across European Netherlands municipalities, cross-referenced with eight CBS municipality-level structural indicators.
Built as a public preview for journalists and researchers. No login required. The data sources are public; the TID door is preview-labelled, not a full country launch.

Built by [Hedegreen Research](https://hedegreenresearch.com).

- Country: `{country_config.display_name}`
- Election scope: `Tweede Kamer 2023` and `Tweede Kamer 2025`
- Runtime views: `Explore`, `Compare municipalities`, `By Municipality`, official land-total `National trends`, and `About & sources`
- Public geography: European Netherlands `{country_config.public_geography_label}`
- Public geography count: `{country_config.public_geography_count}`
- Statistics source: `{country_config.statistics_source_name}`
- Runtime status: public preview with a preview TID door

The adapter deliberately excludes `G9010 NBSB`, Bonaire, Sint Eustatius, Saba, and any abroad-style aggregate rows from the first municipality layer.
"""
        )
        st.markdown(
            """
**Publication boundary**

- Public-preview surface only.
- Public GitHub mirror, public Streamlit preview, and preview-labelled TID door are allowed; no public homepage link, public country-switch exposure, or cross-country claim yet.
- Full public-launch readiness still needs source wording review, national-vs-municipality scope wording review, and turnout-denominator resolution.
"""
        )
        st.markdown(
            """
**Method note**
- Correlation is not causation.
- Party/list rows follow parent-kieskring ballot availability; absent national lists are not blindly backfilled into every municipality.
- `party_id` is year-local and should not be treated as a cross-year party bridge.
- The `National trends` page uses the `L528 / Nederland` land-total rows from the Kiesraad/data.overheid.nl research CSV packages. This national scope is not the same as the European-municipality pattern layer.
- A turnout audit exists, but turnout stays out of the live picker because raw `Opkomst / Kiesgerechtigden` exceeds 100% in some island municipalities.
- The factor picker is intentionally restricted to `population`, `population density`, `age 65+`, `education`, `income`, `one-person households`, `owner-occupied housing`, and `cars`.
- Age 65+ uses CBS `03759NED`, summed from ages 65-94 plus the CBS 95+ aggregate and divided by total population on January 1.
- Education uses CBS `85525NED` `hbo/wo` share for ages 15-75. The 2025 election view uses the latest available 2024 source period, and Schiermonnikoog is absent because CBS publishes a null value.
- Income uses CBS `70072NED` average standardized income for private households excluding student households. The 2025 election view uses latest available 2024 source data, with six CBS-null municipalities omitted.
- One-person households and private cars use CBS `70072NED` current-period `2023` and `2025` rows with full municipality coverage.
- Owner-occupied housing uses CBS `70072NED` `Koopwoningen_94`; the 2025 election view uses latest available 2024 source data because the 2025 field is not usable in the harvested rowset.
"""
        )
        render_compact_dataframe(pd.DataFrame(_factor_rows(factor_frames)))
        st.subheader("Data sources")
        st.markdown(
            """
<div class="source-item"><strong>Kiesraad / data.overheid.nl</strong> - Tweede Kamer 2023 and 2025 CSV result packages.</div>
<div class="source-item"><strong>CBS municipality classifications</strong> - 2023 and 2025 municipality code/name reconciliation.</div>
<div class="source-item"><strong>CBS StatLine 03759NED</strong> - Population on January 1.</div>
<div class="source-item"><strong>CBS StatLine 03759NED</strong> - Age 65+ share derived from population by age.</div>
<div class="source-item"><strong>CBS StatLine 70072NED</strong> - Population density, residents on January 1 per km2 land.</div>
<div class="source-item"><strong>CBS StatLine 85525NED</strong> - Highest completed education level by region.</div>
<div class="source-item"><strong>CBS StatLine 70072NED</strong> - Average standardized household income.</div>
<div class="source-item"><strong>CBS StatLine 70072NED</strong> - One-person households, owner-occupied housing, and private passenger cars per 1,000 residents.</div>
            """,
            unsafe_allow_html=True,
        )
