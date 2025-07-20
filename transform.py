
import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    # Drop rows where any column has blank or missing value
    df = df.dropna()
    df = df[~df.apply(lambda row: row.astype(str).str.strip().eq("").any(), axis=1)]

    # Parse timestamp safely again, in case anything slipped through
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])

    # Derive week_start_date
    df['week_start_date'] = df['timestamp'].dt.to_period('W-SUN').apply(lambda r: r.start_time)

    # Compute total_volume
    df['total_volume'] = df['quantity'] * df['price']

    # Aggregate
    agg_df = df.groupby(
        ['week_start_date', 'client_type', 'user_id', 'symbol'], as_index=False
    ).agg(
        total_volume=('total_volume', 'sum'),
        trade_count=('timestamp', 'count')
    )

    return agg_df
