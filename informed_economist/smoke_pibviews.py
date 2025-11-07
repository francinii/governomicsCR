from backend.cuentas_nacionales.pib import PIBViews
from backend.cuentas_nacionales.pib.pib_constantes import ConstantesPIB as C
import pandas as pd

# 1) Preparamos un DataFrame mínimo con las columnas que usan los métodos "get_*"
#    Lo hacemos para dos sufijos (_TC y _SD) para probar el cambio de series_type.
idx = pd.period_range("2020Q1", periods=3, freq="Q").to_timestamp("Q")
bases_oferta = [C.PIB, C.VALOR_AGREGADO, C.IMPUESTOS]
bases_demanda_cat = [
    C.GASTO_CONSUMO_FINAL_HOGARES,
    C.GASTO_CONSUMO_FINAL_GOBIERNO,
    C.FORMACION_BRUTA_CAPITAL_FIJO,
    C.EXPORTACIONES_TOTALES,
    C.IMPORTACIONES_TOTALES,
]
bases_consumo_hogares = [
    C.GASTO_CONSUMO_FINAL_HOGARES,
    C.BIENES_CONSUMO_DURADERO,
    C.BIENES_CONSUMO_SEMI_DURADEROS,
    C.BIENES_CONSUMO_NO_DURADEROS,
    C.SERVICIOS,  # tu regex acepta 'PIB_' opcional, aquí usamos la forma con 'PIB_' que trae la constante
]

all_bases = set(bases_oferta + bases_demanda_cat + bases_consumo_hogares)
suffixes = ["_TC", "_SD"]

data = {}
for suf in suffixes:
    for base in all_bases:
        col = f"{base}{suf}"
        data[col] = pd.Series([1.0, 2.0, 3.0], index=idx)  # valores dummy

df = pd.DataFrame(data, index=idx)

# 2) Instanciamos PIBViews (acepta "TC" o "_TC"; se normaliza internamente a "_TC")
pv = PIBViews(df, series_type="TC")

# 3) Probar Oferta
of_cat = pv.oferta.get_categorias_principales()
print("Oferta.get_categorias_principales ->", of_cat.columns.tolist())

of_ind = pv.oferta.get_industrias()  # si C.INDUSTRIAS no está en df, devolverá vacío; está bien para una smoke.
print("Oferta.get_industrias -> shape", of_ind.shape)

# 4) Probar Demanda
de_cat = pv.demanda.get_categorias_principales()
print("Demanda.get_categorias_principales ->", de_cat.columns.tolist())

de_ch = pv.demanda.get_consumo_hogares()
print("Demanda.get_consumo_hogares ->", de_ch.columns.tolist())

# 5) Cambiar series_type en caliente y volver a consultar (debe tomar *_SD)
pv.series_type = "SD"
de_cat_sd = pv.demanda.get_categorias_principales()
print("Demanda.get_categorias_principales (SD) ->", de_cat_sd.columns.tolist())

print("OK: smoke test terminado.")
