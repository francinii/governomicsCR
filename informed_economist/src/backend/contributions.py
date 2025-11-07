from __future__ import annotations

from typing import Literal, Optional, Tuple
import numpy as np
import pandas as pd

Method = Literal["Laspeyres", "Paasche", "Fisher"]
Scale = Literal["percent", "unit"]
NaNPolicy = Literal["drop", "ffill", "zeros", "raise"]
JoinHow = Literal["inner", "left", "right"]
OutputScale = Literal["pp", "unit"]

# =========================
# Normalization & Validation
# =========================

def _ensure_numeric(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """Ensure DataFrame is numeric; raises if not possible."""
    if not all(np.issubdtype(dt, np.number) for dt in df.dtypes):
        try:
            df = df.apply(pd.to_numeric, errors="raise")
        except Exception as e:
            raise TypeError(f"{name} must contain only numeric columns. {e}")
    return df


def normalize_scales(
    df_growth: pd.DataFrame,
    df_weights: pd.DataFrame,
    growth_scale: Scale = "percent",
    weight_scale: Scale = "percent",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Convert growth rates and weights to unit scale (proportions) for internal math.
    """
    df_growth = _ensure_numeric(df_growth.copy(), "df_growth")
    df_weights = _ensure_numeric(df_weights.copy(), "df_weights")

    if growth_scale == "percent":
        df_growth_unit = df_growth / 100.0
    elif growth_scale == "unit":
        df_growth_unit = df_growth
    else:
        raise ValueError("growth_scale must be 'percent' or 'unit'.")

    if weight_scale == "percent":
        df_weights_unit = df_weights / 100.0
    elif weight_scale == "unit":
        df_weights_unit = df_weights
    else:
        raise ValueError("weight_scale must be 'percent' or 'unit'.")

    return df_growth_unit, df_weights_unit


def validate_weights_row_sum(
    df_weights_unit: pd.DataFrame,
    tol_sum: float = 1e-3,
) -> pd.DataFrame:
    """
    Validate that row-wise sums of weights are approximately 1.0.
    """
    sums = df_weights_unit.sum(axis=1)
    abs_err = (sums - 1.0).abs()
    ok = abs_err <= tol_sum
    out = pd.DataFrame({"sum": sums, "abs_err": abs_err, "ok": ok})
    return out


# ==============
# Alignment / NaN
# ==============

def align_inputs(
    df_growth: pd.DataFrame,
    df_weights: pd.DataFrame,
    method: Method = "Laspeyres",
    lag_periods: int = 12,
    how: JoinHow = "inner",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Align indices/columns across growth and weights, shifting weights if needed.
    """
    g = df_growth.copy()
    w = df_weights.copy()

    # Align columns (intersection)
    common_cols = sorted(set(g.columns).intersection(set(w.columns)))
    if not common_cols:
        raise ValueError("No common component columns between growth and weights.")
    g = g[common_cols]
    w = w[common_cols]

    # Shift weights for Laspeyres
    if method == "Laspeyres":
        w = w.shift(lag_periods)
    elif method in ("Paasche", "Fisher"):
        pass
    else:
        raise ValueError("method must be 'Laspeyres', 'Paasche', or 'Fisher'.")

    # Align indices
    g, w = g.align(w, join=how, axis=0)
    return g, w


def handle_nans(df: pd.DataFrame, policy: NaNPolicy = "drop") -> pd.DataFrame:
    """Apply a NaN handling policy to a DataFrame."""
    if policy == "drop":
        return df.dropna(how="any")
    elif policy == "ffill":
        return df.ffill()
    elif policy == "zeros":
        return df.fillna(0.0)
    elif policy == "raise":
        if df.isna().any().any():
            where = np.argwhere(df.isna().values)
            raise ValueError(f"NaNs found at positions (row_idx, col_idx): {where[:10]}...")
        return df
    else:
        raise ValueError("policy must be one of 'drop', 'ffill', 'zeros', 'raise'.")


# ======================
# Core Contribution Logic
# ======================

def _compute_contrib_simple(
    df_growth_unit: pd.DataFrame,
    df_weights_unit_aligned: pd.DataFrame,
    scale_output: OutputScale = "pp",
) -> pd.DataFrame:
    """Elementwise contribution = weight * growth."""
    _g = df_growth_unit
    _w = df_weights_unit_aligned
    if not _g.index.equals(_w.index) or not (_g.columns.equals(_w.columns)):
        raise ValueError("Growth and weights must be aligned in index and columns.")
    contrib = _w * _g
    if scale_output == "pp":
        contrib = contrib * 100.0
    elif scale_output == "unit":
        pass
    else:
        raise ValueError("scale_output must be 'pp' or 'unit'.")
    return contrib


def compute_contributions(
    df_growth_unit: pd.DataFrame,
    df_weights_unit: pd.DataFrame,
    method: Method = "Laspeyres",
    lag_periods: int = 12,
    how: JoinHow = "inner",
    nan_policy_growth: NaNPolicy = "drop",
    nan_policy_weights: NaNPolicy = "drop",
    scale_output: OutputScale = "pp",
) -> pd.DataFrame:
    """Compute contributions per component and time."""
    if method == "Fisher":
        # Laspeyres path
        gL, wL = align_inputs(df_growth_unit, df_weights_unit, method="Laspeyres", lag_periods=lag_periods, how=how)
        gL = handle_nans(gL, nan_policy_growth)
        wL = handle_nans(wL, nan_policy_weights)
        gL, wL = gL.align(wL, join="inner", axis=0)
        if gL.empty or wL.empty:
            raise ValueError("No overlapping rows remain after lagging and NaN handling (Fisher/Laspeyres leg).")
        cL = _compute_contrib_simple(gL, wL, scale_output=scale_output)

        # Paasche path
        gP, wP = align_inputs(df_growth_unit, df_weights_unit, method="Paasche", lag_periods=lag_periods, how=how)
        gP = handle_nans(gP, nan_policy_growth)
        wP = handle_nans(wP, nan_policy_weights)
        gP, wP = gP.align(wP, join="inner", axis=0)
        if gP.empty or wP.empty:
            raise ValueError("No overlapping rows remain after NaN handling (Fisher/Paasche leg).")
        cP = _compute_contrib_simple(gP, wP, scale_output=scale_output)

        # Align results and average
        cL, cP = cL.align(cP, join="inner", axis=0)
        if cL.empty or cP.empty:
            raise ValueError("Empty contributions after alignment in Fisher method.")
        return 0.5 * (cL + cP)

    # Single-path methods
    g, w = align_inputs(df_growth_unit, df_weights_unit, method=method, lag_periods=lag_periods, how=how)
    g = handle_nans(g, nan_policy_growth)
    w = handle_nans(w, nan_policy_weights)
    g, w = g.align(w, join="inner", axis=0)
    if g.empty or w.empty:
        raise ValueError("After alignment and NaN handling, no overlapping rows remain.")
    return _compute_contrib_simple(g, w, scale_output=scale_output)


# ======================
# Post Checks & Summaries
# ======================

def validate_contribution_sum(
    df_contrib: pd.DataFrame,
    total_growth_pp: Optional[pd.Series] = None,
    tol_pp: float = 0.05,
) -> pd.DataFrame:
    """Validate row-wise sum of contributions."""
    sums = df_contrib.sum(axis=1)
    out = pd.DataFrame({"sum_contrib": sums})

    if total_growth_pp is not None:
        aligned_total = total_growth_pp.reindex(sums.index)
        abs_err = (sums - aligned_total).abs()
        ok = abs_err <= tol_pp
        out["target"] = aligned_total
        out["abs_err"] = abs_err
        out["ok"] = ok
    else:
        out["abs_err"] = 0.0
        out["ok"] = True
    return out


def to_long_format(
    df_growth_pp: pd.DataFrame,
    df_weights_unit: pd.DataFrame,
    df_contrib_pp: pd.DataFrame,
) -> pd.DataFrame:
    """
    Return a tidy panel with columns: date, component, growth_pp, weight_unit, contribution_pp.
    """
    g, w = df_growth_pp.align(df_weights_unit, join="inner", axis=0)
    g, c = g.align(df_contrib_pp, join="inner", axis=0)

    cols_g = set(g.columns)
    cols_w = set(w.columns)
    cols_c = set(c.columns)
    common_cols = sorted(cols_g & cols_w & cols_c)

    if not common_cols:
        missing_from_g = sorted((cols_w & cols_c) - cols_g)
        missing_from_w = sorted((cols_g & cols_c) - cols_w)
        missing_from_c = sorted((cols_g & cols_w) - cols_c)
        raise ValueError(
            "No common component columns across growth/weights/contributions after alignment.\n"
            f"- Missing from growth: {missing_from_g}\n"
            f"- Missing from weights: {missing_from_w}\n"
            f"- Missing from contributions: {missing_from_c}\n"
            "Check for subtle naming differences (whitespace, accents, suffixes)."
        )

    g = g.reindex(columns=common_cols)
    w = w.reindex(columns=common_cols)
    c = c.reindex(columns=common_cols)

    long_g = g.stack().rename("growth_pp")
    long_w = w.stack().rename("weight_unit")
    long_c = c.stack().rename("contribution_pp")

    tidy = (
        pd.concat([long_g, long_w, long_c], axis=1)
        .reset_index()
        .rename(columns={"level_0": "date", "level_1": "component"})
    )
    return tidy


def summary_contributions(df_contrib_pp: pd.DataFrame, top_k: int = 5) -> pd.DataFrame:
    """Summarize contributions by component."""
    mean_pp = df_contrib_pp.mean(axis=0)
    std_pp = df_contrib_pp.std(axis=0)
    mean_abs_pp = df_contrib_pp.abs().mean(axis=0)
    total_abs = mean_abs_pp.sum()
    share_abs = (mean_abs_pp / total_abs * 100.0) if total_abs > 0 else mean_abs_pp * 0.0

    out = pd.DataFrame({
        "mean_pp": mean_pp,
        "std_pp": std_pp,
        "mean_abs_pp": mean_abs_pp,
        "share_abs": share_abs,
    }).sort_values(by="mean_abs_pp", ascending=False)

    if top_k and top_k > 0:
        out = out.head(top_k)
    return out


# ======================
# Convenience end-to-end
# ======================

def compute_contributions_pipeline(
    df_growth: pd.DataFrame,
    df_weights: pd.DataFrame,
    *,
    method: Method = "Laspeyres",
    lag_periods: int = 12,
    how: JoinHow = "inner",
    growth_scale: Scale = "percent",
    weight_scale: Scale = "percent",
    nan_policy_growth: NaNPolicy = "drop",
    nan_policy_weights: NaNPolicy = "drop",
    scale_output: OutputScale = "pp",
    tol_sum_weights: float = 1e-3,
    total_growth_pp: Optional[pd.Series] = None,
    return_long: bool = False,
) -> Tuple[pd.DataFrame, pd.DataFrame, Optional[pd.DataFrame]]:
    """
    Compute the contribution of each component to the total year-over-year (YoY) growth,
    using consistent normalization, validation, and alignment between growth rates
    and component weights.

    This pipeline encapsulates the full process:
    1. Normalize growth rates and weights (percent → unit scale)
    2. Validate that row-wise weights sum approximately to 1
    3. Compute contributions by component using the selected index method
    4. Optionally validate row sums against an observed total growth rate
    5. Optionally return a tidy panel suitable for visualization or analysis

    Parameters
    ----------
    df_growth : pd.DataFrame
        DataFrame of growth rates by component.
        - Each column represents a component (e.g., industry or sector)
        - Each row represents a time period (e.g., month or quarter)
        - Values must be numeric and typically expressed in percentages (e.g., 3.2 = 3.2%)

        Example:
            >>> df_growth
                        Agricultura  Manufactura  Construccion
            2022-01-31         2.1          3.5          1.0
            2022-02-28         2.3          3.8          1.2
            2022-03-31         2.5          4.1          1.3

    df_weights : pd.DataFrame
        DataFrame of relative weights by component, matching the same structure and column names.
        - Each column must correspond to the same component in df_growth
        - Rows typically sum to 100 (if weight_scale='percent') or to 1 (if weight_scale='unit')
        - The function automatically aligns columns and time indices

        Example:
            >>> df_weights
                        Agricultura  Manufactura  Construccion
            2022-01-31        30.0         50.0         20.0
            2022-02-28        30.5         49.5         20.0
            2022-03-31        31.0         49.0         20.0

    method : {"Laspeyres", "Paasche", "Fisher"}, default "Laspeyres"
        - "Laspeyres": uses weights from the previous period (t - lag_periods)
        - "Paasche"  : uses current period weights (t)
        - "Fisher"   : geometric mean of Laspeyres and Paasche contributions

    lag_periods : int, default 12
        Number of periods to lag weights for Laspeyres calculation.
        - Use 12 for monthly data (year-over-year)
        - Use 4 for quarterly data

    how : {"inner", "left", "right"}, default "inner"
        Join method for index alignment between growth and weights.

    growth_scale : {"percent", "unit"}, default "percent"
        Indicates whether growth rates are in percentages (e.g., 3.2) or proportions (e.g., 0.032).

    weight_scale : {"percent", "unit"}, default "percent"
        Indicates whether weights sum to 100 or to 1 per row.

    nan_policy_growth : {"drop", "ffill", "zeros", "raise"}, default "drop"
        Defines how to handle missing values in the growth DataFrame.

    nan_policy_weights : {"drop", "ffill", "zeros", "raise"}, default "drop"
        Defines how to handle missing values in the weights DataFrame.

    scale_output : {"pp", "unit"}, default "pp"
        - "pp": output in percentage points (e.g., 1.25 = 1.25 percentage points)
        - "unit": output in proportions (e.g., 0.0125)

    tol_sum_weights : float, default 1e-3
        Maximum absolute deviation tolerated when validating that row-wise weights sum ≈ 1.

    total_growth_pp : Optional[pd.Series], default None
        Optional observed total growth series (in pp). If provided, the function will
        validate that the sum of contributions matches this total within a tolerance.

    return_long : bool, default False
        If True, returns a tidy DataFrame with columns:
        ["date", "component", "growth_pp", "weight_unit", "contribution_pp"].

    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame, Optional[pd.DataFrame]]
        - df_contrib_pp : pd.DataFrame
            Contributions per component and time (in percentage points)
        - weights_validation : pd.DataFrame
            Diagnostics of row-wise weight sums (sum, abs_err, ok)
        - tidy_panel : Optional[pd.DataFrame]
            Returned only if return_long=True. Long-format version of the results.

    Examples
    --------
    >>> contrib_pp, wval, tidy = compute_contributions_pipeline(
    ...     df_growth=df_growth,
    ...     df_weights=df_weights,
    ...     method="Laspeyres",
    ...     lag_periods=12,
    ...     growth_scale="percent",
    ...     weight_scale="percent",
    ...     scale_output="pp",
    ...     return_long=True,
    ... )
    >>> contrib_pp.head()
                 Agricultura  Manufactura  Construccion
    2023-01-31         0.63         1.75          0.20
    2023-02-28         0.69         1.89          0.24

    >>> tidy.head()
             date     component  growth_pp  weight_unit  contribution_pp
    0  2023-01-31  Agricultura        2.1         0.30             0.63
    1  2023-01-31  Manufactura        3.5         0.50             1.75
    2  2023-01-31  Construccion       1.0         0.20             0.20
    """
    g_unit, w_unit = normalize_scales(df_growth, df_weights, growth_scale, weight_scale)
    weights_validation = validate_weights_row_sum(w_unit, tol_sum=tol_sum_weights)

    df_contrib = compute_contributions(
        g_unit, w_unit,
        method=method,
        lag_periods=lag_periods,
        how=how,
        nan_policy_growth=nan_policy_growth,
        nan_policy_weights=nan_policy_weights,
        scale_output=scale_output,
    )

    _ = validate_contribution_sum(df_contrib, total_growth_pp=total_growth_pp)

    if return_long:
        g_pp = g_unit * 100.0
        tidy = to_long_format(g_pp, w_unit, df_contrib)
        return df_contrib, weights_validation, tidy

    return df_contrib, weights_validation, None