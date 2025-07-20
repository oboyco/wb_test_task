
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
    
def save_agg_df(agg_df: pd.DataFrame):
    agg_df.to_excel("output/agg_df.xlsx", sheet_name='agg_df')

def save_to_database(agg_df: pd.DataFrame):
    conn = sqlite3.connect("output/agg_result.db")
    agg_df.to_sql("agg_trades_weekly", conn, if_exists="replace", index=False)
    conn.close()
    
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

    line_df = agg_df.groupby(['week_start_date'])['trade_count'].sum().reset_index()
    # Convert week_start_date to string for consistent tick labels
    line_df['week_start_date'] = line_df['week_start_date'].astype(str)
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=line_df, x='week_start_date', y='trade_count', marker="o")
    plt.title('Trade Actions Dynamics, Weekly')
    # Set x-ticks manually to ensure each point has a label
    plt.xticks(ticks=range(len(line_df)), labels=line_df['week_start_date'], rotation=90)
    plt.tight_layout()
    plt.savefig("output/line_chart.png")
    plt.close()

    #line_df = agg_df.groupby(['week_start_date'])['trade_count'].sum().reset_index()
    #plt.figure(figsize=(10,6))
    #sns.lineplot(data=line_df, x='week_start_date', y='trade_count', marker="o")
    #plt.title('Trade Actions Dynamics, Weekly')
    #plt.xticks(rotation=90)
    #plt.tight_layout()
    #plt.savefig("output/line_chart.png")
    #plt.close()
