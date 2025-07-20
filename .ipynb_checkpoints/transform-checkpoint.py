
import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    # Drop rows where *any* column has blank or missing value
    df = df.dropna()
    df = df[~df.apply(lambda row: row.astype(str).str.strip().eq("").any(), axis=1)]

    # Parse timestamp safely again, in case anything slipped through
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])

    # Derive week_start_date
    df['week_start_date'] = df['timestamp'].dt.to_period('W').apply(lambda r: r.start_time)

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

def generate_charts(agg_df: pd.DataFrame):
    import matplotlib.pyplot as plt
    import seaborn as sns
    import os

    os.makedirs("output", exist_ok=True)

    pie_df = agg_df.groupby('client_type')['total_volume'].sum()
    plt.figure(figsize=(6,6))
    pie_df.plot.pie(autopct='%1.1f%%', startangle=140)
    plt.title('Total Volume Share by Client Type')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig("output/pie_chart.png")
    plt.close()

    line_df = agg_df.groupby(['week_start_date', 'symbol'])['trade_count'].sum().reset_index()
    plt.figure(figsize=(10,6))
    sns.lineplot(data=line_df, x='week_start_date', y='trade_count', hue='symbol', marker="o")
    plt.title('Trade Count Dynamics by Symbol')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("output/line_chart.png")
    plt.close()
