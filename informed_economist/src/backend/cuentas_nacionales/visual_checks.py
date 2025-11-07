from __future__ import annotations
from typing import Sequence, Optional
import pandas as pd
import matplotlib.pyplot as plt

def plot_sum_identity(
    df: pd.DataFrame,
    total_col: str,
    part_cols: Sequence[str],
    title: Optional[str] = None,
    show_diff: bool = True,
) -> None:
    """
    Dibuja en una misma figura:
    - Línea del total (total_col)
    - Línea de la suma de componentes (sum(part_cols))
    - (Opcional) Línea de la diferencia (total - suma), para ver desviaciones pequeñas.

    Si falta alguna columna, imprime un mensaje y no rompe.
    """
    missing = [c for c in [total_col, *part_cols] if c not in df.columns]
    if missing:
        print(f"[AVISO] Faltan columnas: {missing} → se omite este gráfico.")
        return

    total = df[total_col]
    suma = df[part_cols].sum(axis=1)
    diff = total - suma

    plt.figure(figsize=(9, 4.5))
    total.plot(label=total_col)
    suma.plot(label="+".join(part_cols))
    if show_diff:
        diff.plot(label="(total - suma)")
    plt.legend(loc="best")
    plt.title(title or f"{total_col} = suma({', '.join(part_cols)})")
    plt.tight_layout()
    plt.show()
