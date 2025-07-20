from extract import extract_data
from transform import transform_data
from load import generate_charts, save_charts_to_excel, save_top_clients, save_to_database, save_agg_df
import os

def main():
    os.makedirs("output", exist_ok=True)
    df = extract_data("data/white_bit_trades.csv")
    agg_df = transform_data(df)
    generate_charts(agg_df)
    save_charts_to_excel()
    save_top_clients(agg_df)
    save_to_database(agg_df)
    save_agg_df(agg_df)

if __name__ == "__main__":
    main()
