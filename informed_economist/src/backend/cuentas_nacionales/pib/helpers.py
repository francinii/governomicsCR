import pandas as pd
from typing import Sequence, Any

def _concat_by_constants(
    df: pd.DataFrame,
    constants: str | Sequence[str],
    return_dict: bool = False
) -> dict[str, Any] | pd.DataFrame:
    """
    Helper basado en df.filter(regex=c) por cada constante.
    Devuelve un dict con: data, found, constants_used, missing_constants, complete.
    """
    if isinstance(constants, str):
        constants = [constants]

    frames: list[pd.DataFrame] = []
    found: list[str] = []
    missing: list[str] = []

    for c in constants:
        sub = df.filter(regex=c)
        if not sub.empty:
            frames.append(sub)
            found.extend(sub.columns.tolist())
        else:
            missing.append(c)

    data = pd.concat(frames, axis=1) if frames else pd.DataFrame(index=df.index)
    s = {
        "data": data,
        "found": found,
        "constants_used": list(constants),
        "missing_constants": missing,
        "complete": len(missing) == 0,
    }
    return s if return_dict else data

def list_properties(obj) -> list[str]:
    """Return property names declared on the class."""
    return [n for n, v in vars(type(obj)).items() if isinstance(v, property)]

def iter_properties(obj):
    """Yield (name, value) for each @property."""
    for n in list_properties(obj):
        yield n, getattr(obj, n)

def get_property_by_index(obj, i: int) -> tuple[str, Any]:
    """Return (name, value) of the i-th @property."""
    props = list_properties(obj)
    name = props[i]
    return name, getattr(obj, name)