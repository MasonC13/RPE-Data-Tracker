import json
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

def get_data_from_sheets():
    """Fetch and process data from Google Sheets"""
    with open("credentials.json", "r") as file:
        creds_data = json.load(file)

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(creds_data, scopes=scopes)
    client = gspread.authorize(creds)

    sheet_id = "1W-wT-2nBcXROuThRrMFK6rTLljDC02aJ6kqL8iDlitE"
    workbook = client.open_by_key(sheet_id)
    worksheet = workbook.worksheet("RPE Sheet")

    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    df.columns = df.columns.str.strip()

    print("Available columns:", df.columns.tolist())

    date_columns = df.columns[6:]
    df[date_columns] = df[date_columns].apply(pd.to_numeric, errors='coerce')
    df['Average Value'] = df[date_columns].mean(axis=1)

    id_columns = ['Position']
    if 'Name' in df.columns:
        id_columns.append('Name')
    if 'Email' in df.columns:
        id_columns.append('Email')

    print("Using ID columns:", id_columns)

    df_long = df.melt(id_vars=id_columns, 
                      value_vars=date_columns, 
                      var_name="Date", 
                      value_name="Value")
    df_long['Date'] = pd.to_datetime(df_long['Date'], errors='coerce')
    df_position_daily_avg = df_long.groupby(['Position', 'Date'])['Value'].mean().reset_index()

    return df, df_long, df_position_daily_avg
