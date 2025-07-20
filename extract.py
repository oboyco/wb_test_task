import pandas as pd

def extract_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv('data/white_bit_trades.csv')

    # Drop rows with any blank or missing values
    df = df.dropna()
    df = df[~df.apply(lambda row: row.astype(str).str.strip().eq("").any(), axis=1)]

    # Convert timestamp column
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Drop rows where timestamp couldn't be parsed
    df = df.dropna(subset=['timestamp'])

    return df