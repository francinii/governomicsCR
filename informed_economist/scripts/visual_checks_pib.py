# scripts/visual_checks_pib.py
import os
import pandas as pd
import matplotlib.pyplot as plt

from backend.cuentas_nacionales.pib import PIBViews
from backend.cuentas_nacionales.pib.pib_constantes import ConstantesPIB as C

# --------------------------------------------------------------------------------
# Carga de datos (ajusta paths si hace falta)
# --------------------------------------------------------------------------------
BASE = r"C:\Users\adolj\OneDrive\Documentos\APPS\informed_economist\data\raw"

def load_df(fname, sheet="pibQ"):
    df = pd.read_excel(os.path.join(BASE, fname), sheet_name=sheet)
    df = df.set_index("fecha")
    return df

quarterly_data_levels_TC = load_df("Variables_PIB_TC.xlsx")
quarterly_data_levels_SO = load_df("Variables_PIB_SO.xlsx")
quarterly_data_levels_SD = load_df("Variables_PIB_SD.xlsx")

# --------------------------------------------------------------------------------
# Helper: resuelve "PIB_<base>_SUF" o "<base>_SUF"
# --------------------------------------------------------------------------------
def resolve(df: pd.DataFrame, base: str, sufijo: str) -> str | None:
    for name in (f"PIB_{base}{sufijo}", f"{base}{sufijo}"):
        if name in df.columns:
            return name
    return None

def warn_missing(miss):
    print(f"[AVISO] Faltan columnas: {miss} → se omite este gráfico.")


print('\n\n********************************CARGA DE DATAFRAMES********************************\n\n')

print('\n1) Datos Tendencia Ciclo:\n')

quarterly_data_levels_TC.info()

print('\n2)Datos Serie Original:\n')

quarterly_data_levels_SO.info()

print('\n3) Datos Serie Desestacionalizada:\n')

quarterly_data_levels_SD.info()

print('\n\n****************************VISUALIZACIÓN DE IDENTIDADES****************************\n\n')


