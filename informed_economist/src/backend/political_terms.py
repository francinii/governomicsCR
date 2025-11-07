"""
political_terms.py
------------------

This module provides utilities to tag economic or financial time series
with political context based on Costa Rican presidential terms.

Functions
---------
- build_cr_terms() :
    Returns a DataFrame with the start and end dates of each presidential term,
    including President, Party, Term (e.g., "2006–2010"), and Label (short surname).

- assign_by_terms(index, terms_df, column) :
    Maps each timestamp in a DatetimeIndex to the corresponding political
    attribute (e.g., President or Party) according to the presidential terms.

- tag_politics(df, terms_df=None, add_cols=("President","Party","Term","Label")) :
    Appends political context columns to an existing DataFrame whose index
    is a DatetimeIndex (monthly, quarterly, or custom frequency).
    Each row is tagged with the President in office, political party,
    the four-year Term, and a simplified surname Label.

Notes
-----
- The mapping is currently specific to Costa Rica from 1990 onwards.
- The Label field uses the most recognizable surname (e.g., "Arias", "Solís", "Chaves").
- Overlapping transfer dates (e.g., May 8) are handled gracefully using
  pandas IntervalIndex with non-unique lookups.
"""

import pandas as pd

# -----------------------------
# 1) Mapping of short surnames
# -----------------------------
SURNAME_LABEL = {
    "Rafael Ángel Calderón Fournier": "Calderón",
    "José María Figueres Olsen": "Olsen",
    "Miguel Ángel Rodríguez Echeverría": "Rodríguez",
    "Abel Pacheco": "Pacheco",
    "Óscar Arias Sánchez": "Arias",
    "Laura Chinchilla Miranda": "Chinchilla",
    "Luis Guillermo Solís Rivera": "Solís",
    "Carlos Alvarado Quesada": "Alvarado",
    "Rodrigo Chaves Robles": "Chaves",
}

def _short_label(name: str) -> str:
    """
    Return the simplified surname label for a given president's full name.

    Parameters
    ----------
    name : str
        Full name of the president.

    Returns
    -------
    str
        Short surname as defined in SURNAME_LABEL.
        If the name is not in the mapping, the function falls back
        to the last token of the full name.
    """
    if name in SURNAME_LABEL:
        return SURNAME_LABEL[name]
    return name.split()[-1] if name else ""

# ------------------------------------
# 2) Costa Rican presidential terms
# ------------------------------------
def build_cr_terms() -> pd.DataFrame:
    """
    Build a DataFrame of Costa Rican presidential terms (1990 onwards).

    Returns
    -------
    pd.DataFrame
        A DataFrame with columns:
        - start : datetime64, start date of the term
        - end   : datetime64, end date of the term
        - President : str, full name of the president
        - Party     : str, party acronym
        - Term      : str, formatted range (e.g., "2006–2010")
        - Label     : str, simplified surname for easier reference
    """
    terms = [
        ("1990-05-08", "1994-05-08", "Rafael Ángel Calderón Fournier", "PUSC"),
        ("1994-05-08", "1998-05-08", "José María Figueres Olsen", "PLN"),
        ("1998-05-08", "2002-05-08", "Miguel Ángel Rodríguez Echeverría", "PUSC"),
        ("2002-05-08", "2006-05-08", "Abel Pacheco", "PUSC"),
        ("2006-05-08", "2010-05-08", "Óscar Arias Sánchez", "PLN"),
        ("2010-05-08", "2014-05-08", "Laura Chinchilla Miranda", "PLN"),
        ("2014-05-08", "2018-05-08", "Luis Guillermo Solís Rivera", "PAC"),
        ("2018-05-08", "2022-05-08", "Carlos Alvarado Quesada", "PAC"),
        ("2022-05-08", "2026-05-08", "Rodrigo Chaves Robles", "PPSD"),
    ]
    df = pd.DataFrame(terms, columns=["start","end","President","Party"])
    df["start"] = pd.to_datetime(df["start"])
    df["end"]   = pd.to_datetime(df["end"])

    df["Term"] = df["start"].dt.strftime("%Y") + "–" + df["end"].dt.strftime("%Y")
    df["Label"] = df["President"].map(_short_label)
    return df

# ---------------------------------------------------
# 3) Generic assignment engine (handles overlaps)
# ---------------------------------------------------
def assign_by_terms(index: pd.DatetimeIndex, terms_df: pd.DataFrame, column: str) -> pd.Series:
    """
    Assign political attributes to each timestamp in a DatetimeIndex.

    Parameters
    ----------
    index : pd.DatetimeIndex
        Index of dates to be mapped to political terms.
    terms_df : pd.DataFrame
        DataFrame returned by build_cr_terms(), containing intervals
        defined by 'start' and 'end' columns.
    column : str
        Column name in terms_df to be assigned (e.g., "President", "Party", "Term", "Label").

    Returns
    -------
    pd.Series
        A Series aligned with the input index, containing the mapped values.
        Rows outside the defined intervals return <NA>.
    """
    intervals = pd.IntervalIndex.from_arrays(terms_df["start"], terms_df["end"], closed="both")
    locs, _ = intervals.get_indexer_non_unique(index)

    out = pd.Series(pd.NA, index=index, dtype="object")
    mask = locs >= 0
    if mask.any():
        values = terms_df[column].to_numpy()
        out[mask] = values[locs[mask]]
    return out

def tag_politics(df: pd.DataFrame,
                 terms_df: pd.DataFrame | None = None,
                 add_cols: tuple[str, ...] = ("President","Party","Term","Label")) -> pd.DataFrame:
    """
    Append political context columns to a DataFrame based on its DatetimeIndex.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame whose index is a DatetimeIndex.
    terms_df : pd.DataFrame, optional
        Custom DataFrame with political terms.
        If None, build_cr_terms() is used.
    add_cols : tuple of str, default ("President","Party","Term","Label")
        Columns from terms_df to append to the DataFrame.

    Returns
    -------
    pd.DataFrame
        Copy of the input DataFrame with additional columns:
        - President (full name)
        - Party     (acronym)
        - Term      (period string "YYYY–YYYY")
        - Label     (short surname)
    """
    if terms_df is None:
        terms_df = build_cr_terms()
    out = df.copy()
    for c in add_cols:
        out[c] = assign_by_terms(out.index, terms_df, c)
    return out

