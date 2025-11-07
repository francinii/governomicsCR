
import pandas as pd
import os
import glob
# import sys # Removed unnecessary sys import

# Add the project root to   Qu sys.path to enable imports from config
# script_dir = os.path.dirname(__file__)
# project_root = os.path.abspath(os.path.join(script_dir, ".."))
# if project_root not in sys.path:
#     sys.path.insert(0, project_root)

from app.core import config # Updated import path

def load_all_excel_data(directory="data/raw"):
    all_files = glob.glob(os.path.join(directory, "*.xlsx"))
    df_list = []
    for file_path in all_files:
        try:
            df = pd.read_excel(file_path)
            df_list.append(df)
        except Exception as e:
            print(f"Error loading Excel file {file_path}: {e}")
            return None
    
    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        if 'fecha' in combined_df.columns:
            combined_df['fecha'] = pd.to_datetime(combined_df['fecha'])
            combined_df = combined_df.sort_values(by='fecha').reset_index(drop=True)
        return combined_df
    else:
        print("No Excel files found or loaded.")
        return None

def assign_administration_period(df):
    if df is None or df.empty or 'fecha' not in df.columns:
        return pd.DataFrame()

    # Calculate the start year of each administration
    # Assuming administrations start at the beginning of a year
    # And are ADMINISTRATION_PERIOD_YEARS long
    df['admin_start_year'] = ((df['fecha'].dt.year - df['fecha'].dt.year.min()) // config.ADMINISTRATION_PERIOD_YEARS) * config.ADMINISTRATION_PERIOD_YEARS + df['fecha'].dt.year.min()
    df['administration'] = df['admin_start_year'].astype(str) + '-' + (df['admin_start_year'] + config.ADMINISTRATION_PERIOD_YEARS - 1).astype(str)
    return df.drop(columns=['admin_start_year'])


if __name__ == "__main__":
    combined_df = load_all_excel_data()
    if combined_df is not None:
        combined_df = assign_administration_period(combined_df)
        print(f"Column names: {combined_df.columns.tolist()}")
        print("First 5 rows of combined data with administration:")
        print(combined_df.head().to_markdown(index=False))
    
