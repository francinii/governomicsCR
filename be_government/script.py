import pandas as pd
import numpy as np

# ====================================================================
# PARTE 1: Módulo 'political_terms.py' (Funciones para el Contexto Político)
#          (Sin cambios)
# ====================================================================

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
    """Retorna la etiqueta del apellido simplificada para un presidente."""
    if name in SURNAME_LABEL:
        return SURNAME_LABEL[name]
    return name.split()[-1] if name else ""

def build_cr_terms() -> pd.DataFrame:
    """Construye un DataFrame de los períodos presidenciales de Costa Rica (1990 en adelante)."""
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

def assign_by_terms(index: pd.DatetimeIndex, terms_df: pd.DataFrame, column: str) -> pd.Series:
    """Asigna atributos políticos a cada marca de tiempo en un DatetimeIndex."""
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
    """Añade columnas de contexto político a un DataFrame basado en su DatetimeIndex."""
    if terms_df is None:
        terms_df = build_cr_terms()
    out = df.copy()
    for c in add_cols:
        out[c] = assign_by_terms(out.index, terms_df, c)
    return out

# ====================================================================
# PARTE 2: Lógica principal para la carga, etiquetado y agregación
# ====================================================================

def generar_estadisticas_por_gobierno(file_name: str, output_suffix: str) -> list[str]:
    """
    Carga un archivo CSV, lo etiqueta con la variable 'Label' del presidente,
    calcula estadísticas descriptivas para CADA variable por 'Label' y guarda
    el resultado en un nuevo CSV para CADA variable.

    Parameters
    ----------
    file_name : str
        Nombre del archivo CSV a cargar.
    output_suffix : str
        Sufijo para los archivos de salida (e.g., 'MENSUAL' o 'TRIMESTRAL').
        
    Returns
    -------
    list[str]
        Lista de nombres de archivos generados.
    """
    print(f"-> Procesando archivo base: {file_name}")
    generated_files = []

    try:
        # 1. Cargar datos y configurar el índice
        # Usamos read_csv ya que los archivos adjuntos son CSV.
        df = pd.read_excel(file_name, index_col='fecha', parse_dates=True)
    except FileNotFoundError:
        print(f"ERROR: Archivo no encontrado: {file_name}. Asegúrate de que el nombre y la ruta sean correctos.")
        return []

    # 2. Etiquetar el DataFrame con el contexto político
    df_tagged = tag_politics(df)

    # 3. Definir las funciones de agregación
    agg_functions = [
        'mean',
        'median',
        'std',
        'min',
        ('p25', lambda x: x.quantile(0.25)),
        ('p75', lambda x: x.quantile(0.75)),
        'max',
        'count'
    ]

    # Columnas a excluir del análisis de estadísticas (columnas políticas añadidas)
    exclude_cols = ["President", "Party", "Term", "Label"]
    
    # Extraer las columnas de datos
    data_cols = [col for col in df.columns if col not in exclude_cols]
    
    # 4. Iterar sobre CADA variable y calcular las estadísticas
    for variable in data_cols:
        print(f"   -> Calculando estadísticas para la variable: {variable}")
        
        # Agrupar por 'Label' y calcular las estadísticas SÓLO para la variable actual
        # Usamos [variable] para obtener un DataFrame o Series con solo esa columna/variable
        results = df_tagged.groupby('Label')[variable].agg(agg_functions).reset_index()

        # 5. Formatear el DataFrame de resultados
        # Cambiamos los nombres de las columnas de métricas para incluir la variable (aunque ya la sabemos)
        # y añadimos la columna de Presidente
        metric_names = [f"{variable}_{name}" if name not in ['p25', 'p75'] else f"{variable}_{name}" 
                        for name in ['mean', 'median', 'std', 'min', 'p25', 'p75', 'max', 'count']]
        
        # Asegurar que el nombre de la columna 'Label' sea 'Presidente'
        results.columns = ['Presidente'] + [col[1] if isinstance(col, tuple) else col for col in results.columns][1:]
        
        # Renombrar las columnas de métricas de forma más limpia
        results.columns = ['Presidente'] + [f"{variable}_{name}" for name in ['mean', 'median', 'std', 'min', 'p25', 'p75', 'max', 'count']]

        # 6. Guardar el resultado en un nuevo CSV por variable
        # Limpiamos el nombre de la variable para el nombre de archivo (reemplazar _TC con _TC_ si es necesario, aunque en este caso la variable ya es limpia)
        file_variable_name = variable.replace(' ', '_').replace('.', '') 
        output_file = f"PIB_Estadisticas_por_Gobierno_{file_variable_name}_{output_suffix}.csv"
        results.to_csv(output_file, index=False)
        
        generated_files.append(output_file)
        # print(f"   -> Archivo generado: {output_file}") # Descomentar si quieres ver cada archivo generado

    return generated_files

# ====================================================================
# PARTE 3: Función para generar Variables_PIB_TCV2.xlsx
# ====================================================================

def create_pib_tc_v2_with_president(file_name: str, output_file_name: str):
    """
    Carga un archivo XLSX, le añade la columna del presidente según el año de gobierno,
    y guarda el resultado en un nuevo archivo XLSX.
    """
    print(f"-> Creando {output_file_name} con contexto político...")
    try:
        df = pd.read_excel(file_name, index_col='fecha', parse_dates=True)
    except FileNotFoundError:
        print(f"ERROR: Archivo no encontrado: {file_name}. Asegúrate de que el nombre y la ruta sean correctos.")
        return

    df_tagged = tag_politics(df, add_cols=("President",))
    df_tagged.to_excel(output_file_name, index=True)
    print(f"-> Archivo generado: {output_file_name}")

# ====================================================================
# EJECUCIÓN PRINCIPAL
# ====================================================================
if __name__ == "__main__":
    
    # === ATENCIÓN: Nombres de archivos corregidos para coincidir con los CSV adjuntos ===
    # Uso los nombres de los archivos CSV que subiste para asegurar que el script funcione.
    archivos_pib = [
        {"file": "data/raw/Variables_PIB_TC.xlsx", "suffix": "MENSUAL"},
        {"file": "data/raw/Variables_PIB_SO.xlsx", "suffix": "TRIMESTRAL"},
    ]
    
    generated_files = []
    
    print("--- INICIANDO PROCESO DE GENERACIÓN DE ESTADÍSTICAS POR VARIABLE Y GOBIERNO ---")

    #for item in archivos_pib:
    #    file_list = generar_estadisticas_por_gobierno(item["file"], item["suffix"])
    #    generated_files.extend(file_list)

    # === Generar Variables_PIB_TCV2.xlsx ===
    create_pib_tc_v2_with_president("app/data/raw/Variables_PIB_TC.xlsx", "app/data/raw/Variables_PIB_TCV2.xlsx")

    # Mostrar la lista de archivos generados al final
    #print("\nProceso completado. Archivos de estadísticas individuales generados:")
    #for f in generated_files:
    #    print(f"- {f}")