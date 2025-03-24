import gspread      # Library to interact with Google Sheets
from google.oauth2.service_account import Credentials
import pandas as pd # Library to handle data manipulation

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)       # Client to access different sheets

sheet_id = "1W-wT-2nBcXROuThRrMFK6rTLljDC02aJ6kqL8iDlitE"  
workbook = client.open_by_key(sheet_id)     # Access sheet with sheet url ID

worksheet = workbook.worksheet("RPE Sheet")  # Access specific worksheet by name

data = worksheet.get_all_records()  # Get all records from the worksheet

df = pd.DataFrame(data)  # Convert data to a pandas DataFrame

position_filter = "OL"
position_data = df[df['Position'] == position_filter]  # Filter data by position

difficulty_by_position = position_data["RPE"]

position_stats = position_data.describe()  # Get statistics for the filtered data

print(f"Data for position: {position_filter}")
print(position_data)
print("\nStatistics for this position:")
print(position_stats)

for position in df["Position"].unique():
    position_group = df[df['Position'] == position]
    pos_average = position_group["RPE"].mean()
    print(f"{position} average difficulty: {pos_average}")