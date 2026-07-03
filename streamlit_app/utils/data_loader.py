from pathlib import Path
from html import escape

import pandas as pd
import streamlit as st


APP_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = APP_ROOT / "assets"


def page_config(title: str) -> None:
    st.set_page_config(page_title=title, layout="wide")
    load_css()


def load_css() -> None:
    css_path = ASSETS_DIR / "styles.css"
    if css_path.exists():
        st.markdown(
            f"<style>{css_path.read_text(encoding='utf-8')}</style>",
            unsafe_allow_html=True,
        )


def page_header(title: str, caption: str, icon_class: str = "icon-dashboard") -> None:
    st.markdown(
        (
            f'<div class="app-header"><span class="icon {escape(icon_class)}"></span>'
            f'<div><h1 class="app-title">{escape(title)}</h1>'
            f'<p class="app-caption">{escape(caption)}</p></div></div>'
        ),
        unsafe_allow_html=True,
    )


def section_title(title: str, icon_class: str = "icon-dashboard") -> None:
    st.markdown(
        f'<div class="section-title"><span class="icon {escape(icon_class)}"></span>{escape(title)}</div>',
        unsafe_allow_html=True,
    )


def metric_row(metrics: list[tuple[str, str, str | None]]) -> None:
    columns = st.columns(len(metrics))
    for column, (label, value, note) in zip(columns, metrics):
        with column:
            st.metric(label=str(label), value=str(value), help=str(note) if note else None)


def read_csv(relative_path: str, parse_dates: list[str] | None = None) -> pd.DataFrame | None:
    path = PROJECT_ROOT / relative_path
    if not path.exists():
        st.warning(f"Missing file: {relative_path}")
        st.code(str(path))
        return None

    return pd.read_csv(path, parse_dates=parse_dates)


def cached_csv(relative_path: str, parse_dates: tuple[str, ...] = ()) -> pd.DataFrame | None:
    path = PROJECT_ROOT / relative_path
    if not path.exists():
        return None

    return _cached_csv(
        str(path),
        parse_dates,
        path.stat().st_mtime,
    )


@st.cache_data
def _cached_csv(path: str, parse_dates: tuple[str, ...], modified_time: float) -> pd.DataFrame:
    return pd.read_csv(path, parse_dates=list(parse_dates) or None)


def require_columns(df: pd.DataFrame, columns: set[str], label: str) -> bool:
    missing = columns - set(df.columns)
    if missing:
        st.error(f"{label} is missing required columns.")
        st.write("Missing columns:", sorted(missing))
        st.write("Available columns:", list(df.columns))
        return False

    return True


def format_number(value: float, decimals: int = 0) -> str:
    if pd.isna(value):
        return "0"

    return f"{value:,.{decimals}f}"
