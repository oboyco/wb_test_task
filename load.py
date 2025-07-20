
import pandas as pd
import sqlite3
import os

def save_charts_to_excel():
    with pd.ExcelWriter("output/charts.xlsx", engine='xlsxwriter') as writer:
        workbook = writer.book
        worksheet = workbook.add_worksheet("Charts")
        writer.sheets['Charts'] = worksheet
        worksheet.insert_image('B2', 'output/pie_chart.png')
        worksheet.insert_image('B20', 'output/line_chart.png')

def save_top_clients(agg_df: pd.DataFrame):
    top_clients = agg_df[agg_df['client_type'] == 'bronze'].groupby('user_id')['total_volume'].sum().nlargest(3)
    top_clients.to_excel("output/top_clients.xlsx", sheet_name='Top Bronze Clients')

def save_to_database(agg_df: pd.DataFrame):
    conn = sqlite3.connect("output/agg_result.db")
    agg_df.to_sql("agg_trades_weekly", conn, if_exists="replace", index=False)
    conn.close()
