import pandas as pd

def get_data_from_csv():
    """Fetch and process data from responses.csv"""
    df = pd.read_csv("responses.csv")
    df.columns = df.columns.str.strip()

    print("Available columns:", df.columns.tolist())

    # Adjust the range if the date columns are in different positions
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

