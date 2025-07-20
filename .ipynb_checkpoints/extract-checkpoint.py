
import pandas as pd

def extract_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path, parse_dates=['timestamp'])
