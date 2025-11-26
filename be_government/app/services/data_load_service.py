# be_government/app/services/data_load_service.py
import os

class DataLoadService:
    def __init__(self):
        pass

    def _get_full_data_path(self, relative_path: str) -> str:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        return os.path.join(base_dir, "app", relative_path)

    def load_data(self, relative_file_path: str) -> str:
        """
        Loads the content of a data file from the given relative path.
        Tries UTF-8 first, falls back to latin-1 if decode error occurs.
        """
        full_file_path = self._get_full_data_path(relative_file_path)
        if not os.path.exists(full_file_path):
            raise FileNotFoundError(f"Data file not found at: {full_file_path}")

        try:
            with open(full_file_path, 'r', encoding='utf-8') as f:
                data = f.read()
        except UnicodeDecodeError:
            # Fallback: try latin-1
            with open(full_file_path, 'r', encoding='latin-1') as f:
                data = f.read()
        return data
