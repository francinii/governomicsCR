import pandas as pd
import numpy as np
from typing import List, Optional

def compute_basic_statistics(df, value_col="PIB_TC", groupby_col="Label"):
    stats = (
        df.groupby(groupby_col)[value_col]
        .agg(
            mean="mean",
            median="median",
            std="std",
            min="min",
            p25=lambda x: x.quantile(0.25),
            p75=lambda x: x.quantile(0.75),
            max="max",
            count="count"
        )
    )
    return stats


def calculate_component_percentages(
    df: pd.DataFrame,
    total_col: Optional[str] = None,
    component_cols: Optional[List[str]] = None,
    decimals: int = 2
) -> pd.DataFrame:
    """
    Calculate the percentage contribution of component columns relative to a total column.
    If the total column is not provided or does not exist, it is created as the sum of components.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing total and component columns.
    total_col : str, optional
        Name of the column representing the total value.
        If None or missing in df, the total will be computed as the row-wise sum of the component columns.
    component_cols : list of str, optional
        List of columns representing components to compare against the total.
        If None, all numeric columns (except the total, if it exists) are used.
    decimals : int, default=2
        Number of decimals to round the resulting percentages.

    Returns
    -------
    pd.DataFrame
        DataFrame containing only percentage columns, with one column per component.

    Examples
    --------
    >>> data = pd.DataFrame({
    ...     "A": [30, 50],
    ...     "B": [20, 30],
    ...     "C": [50, 20]
    ... })
    >>> calculate_component_percentages(data)
         A     B     C
    0  30.0  20.0  50.0
    1  50.0  30.0  20.0
    """
    df = df.copy()

    # --- Identify component columns ---
    if component_cols is None:
        if total_col and total_col in df.columns:
            component_cols = df.select_dtypes(include="number").columns.drop(total_col).tolist()
        else:
            component_cols = df.select_dtypes(include="number").columns.tolist()

    if not component_cols:
        raise ValueError("No component columns found or specified.")

    # --- Handle total column creation or validation ---
    if total_col is None or total_col not in df.columns:
        total_col = total_col or "total"
        df[total_col] = df[component_cols].sum(axis=1)

    # --- Avoid division by zero ---
    if (df[total_col] == 0).any():
        raise ValueError("Total column contains zeros — cannot compute percentages safely.")

    # --- Compute percentages ---
    pct_df = pd.DataFrame(index=df.index)
    for col in component_cols:
        pct_df[col] = (df[col] / df[total_col] * 100).round(decimals)

    return pct_df

def validate_percentage_sum(
    df: pd.DataFrame,
    expected_sum: float = 100.0,
    tolerance: float = 0.05,
    verbose: bool = True
) -> dict:
    """
    Validate that the sum of percentage columns per row approximates a target value (default = 100).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing only percentage columns.
    expected_sum : float, default=100.0
        Expected sum of the percentages per row.
    tolerance : float, default=0.05
        Allowed absolute deviation (± tolerance).
    verbose : bool, default=True
        Whether to print a summary message.

    Returns
    -------
    dict
        Dictionary with:
            - 'n_total': total number of rows
            - 'n_valid': number of rows within tolerance
            - 'n_invalid': number of rows outside tolerance
            - 'invalid_rows': index of invalid rows
            - 'max_abs_deviation': maximum deviation observed
    """
    row_sums = df.sum(axis=1)
    deviations = (row_sums - expected_sum).abs()

    valid_mask = deviations <= tolerance
    n_total = len(df)
    n_valid = valid_mask.sum()
    n_invalid = n_total - n_valid
    invalid_rows = df.index[~valid_mask].tolist()
    max_dev = deviations.max() if n_total else np.nan

    result = {
        "n_total": n_total,
        "n_valid": n_valid,
        "n_invalid": n_invalid,
        "invalid_rows": invalid_rows,
        "max_abs_deviation": round(float(max_dev), 5),
    }

    if verbose:
        print(f"✅ Percentage check: {n_valid}/{n_total} rows within ±{tolerance} of {expected_sum}.")
        if n_invalid > 0:
            print(f"⚠️  {n_invalid} rows failed validation. Max deviation: {result['max_abs_deviation']}.")
    
    return result