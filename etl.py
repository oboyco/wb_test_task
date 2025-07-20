from extract import extract_data
from transform import transform_data, generate_charts
from load import save_charts_to_excel, save_top_clients, save_to_database
import os
import pandas as pd

def main():
    os.makedirs("output", exist_ok=True)
    df = extract_data("data/white_bit_trades.csv")
    agg_df = transform_data(df)
    generate_charts(agg_df)
    save_charts_to_excel()
    save_top_clients(agg_df)
    save_to_database(agg_df)

if __name__ == "__main__":
    main()