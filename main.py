from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime, timedelta
import numpy as np
import json
from io import StringIO

# Dashboard imports
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

# Import other modules
try:
    from emailNotif import send_email
    from coachReport import generate_coach_report
    email_module_available = True
except ImportError:
    email_module_available = False
    print("Email notification modules not available. Email features will be disabled.")

# Truman State University Colors
TRUMAN_PURPLE = "#4F2D7F"  # Primary purple
TRUMAN_LIGHT_BLUE = "#00B2E3"  # Light blue/cyan accent
TRUMAN_PURPLE_LIGHT = "#8F73B3"  # Lighter shade of purple for alternating elements
TRUMAN_WHITE = "#FFFFFF"  # White

# Custom Plotly color sequence using school colors
TRUMAN_COLOR_SEQUENCE = [TRUMAN_PURPLE, TRUMAN_LIGHT_BLUE, TRUMAN_PURPLE_LIGHT, "#9E1B34", "#F1C038"]

# Hardcoded coach emails - REPLACE THESE WITH ACTUAL COACH EMAILS
COACH_EMAILS = [
    "mc6383@truman.edu"
]

# CSV file path - used by both apps
CSV_FILE = "responses.csv"

# Define base headers
BASE_COLUMNS = [
    "Email",
    "Last 4 Digits",
    "Last Name",
    "First Name",
    "Position",
    "Summer Attendance"
]

# Ensure the CSV exists
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=BASE_COLUMNS)
    df.to_csv(CSV_FILE, index=False)

# Create the Flask app
flask_app = Flask(__name__)
CORS(flask_app)

# Create the Dash app
dash_app = dash.Dash(
    __name__, 
    server=flask_app,
    url_base_pathname='/dashboard/',
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
dash_app.config.suppress_callback_exceptions = True

# Form submission endpoint
@flask_app.route("/submit", methods=["POST"])
def submit_form():
    data = request.json
    today_str = datetime.today().strftime("%m/%d/%Y")  # e.g. 4/15/2025

    # Load existing CSV
    df = pd.read_csv(CSV_FILE)

    # Add today's date column if not exists
    if today_str not in df.columns:
        df[today_str] = ""

    # Check if user already exists (by email)
    email = data.get("email")
    user_index = df[df["Email"] == email].index

    if len(user_index) > 0:
        # Update existing row with intensity level
        idx = user_index[0]
        df.at[idx, today_str] = data.get("intensityLevel")  # Store intensity level for today
    else:
        # Create new row with intensity level
        new_row = {
            "Email": data.get("email"),
            "Last 4 Digits": data.get("last4"),
            "Last Name": data.get("lastName"),
            "First Name": data.get("firstName"),
            "Position": data.get("position"),
            "Summer Attendance": data.get("summerAttendance"),
            today_str: data.get("intensityLevel")  # Store intensity level for today
        }

        # Fill missing date columns
        for col in df.columns:
            if col not in new_row:
                new_row[col] = ""

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Reorder columns: base + dates
    date_cols = [col for col in df.columns if col not in BASE_COLUMNS]
    df = df[BASE_COLUMNS + sorted(date_cols, key=lambda x: datetime.strptime(x, "%m/%d/%Y"))]

    df.to_csv(CSV_FILE, index=False)
    return jsonify({"message": "Data saved successfully"}), 200

# Redirect root to dashboard
@flask_app.route("/")
def index():
    return flask_app.redirect("/dashboard/")

# Function to get data from CSV (moved from pythonCSV.py)
def get_data_from_csv():
    try:
        # Read the CSV file
        df = pd.read_csv(CSV_FILE)
        
        # Create Name field from first and last name if needed
        if 'First Name' in df.columns and 'Last Name' in df.columns and 'Name' not in df.columns:
            df['Name'] = df['First Name'] + ' ' + df['Last Name']
            
        # Identify base columns and date columns
        base_columns = [col for col in df.columns if col in BASE_COLUMNS or col == 'Name']
        date_columns = [col for col in df.columns if col not in base_columns]
        
        # Restructure data for time series analysis
        restructured_data = []
        
        for _, row in df.iterrows():
            athlete_name = row.get('Name', '') or f"{row.get('First Name', '')} {row.get('Last Name', '')}"
            position = row.get('Position', '')
            email = row.get('Email', '')
            
            for date_col in date_columns:
                value = row[date_col]
                # Skip empty values
                if pd.notna(value) and str(value).strip() != '':
                    # Make sure value is numeric
                    try:
                        if isinstance(value, str):
                            clean_value = ''.join(c for c in value if c.isdigit() or c == '.')
                            numeric_value = float(clean_value) if clean_value else None
                        else:
                            numeric_value = float(value)
                            
                        # Cap values at reasonable RPE max (10)
                        if numeric_value is not None:
                            if numeric_value > 100:
                                numeric_value = numeric_value / 100
                            elif numeric_value > 10:
                                numeric_value = numeric_value / 10
                            
                            # Final cap at 10
                            numeric_value = min(numeric_value, 10.0)
                            
                            restructured_data.append({
                                'Name': athlete_name,
                                'Position': position,
                                'Email': email,
                                'Date': date_col,
                                'Value': numeric_value
                            })
                    except (ValueError, TypeError):
                        continue
        
        # Create dataframe from restructured data
        df_long = pd.DataFrame(restructured_data)
        
        # Convert dates to datetime
        df_long['Date'] = pd.to_datetime(df_long['Date'], format="%m/%d/%Y", errors='coerce')
        
        # Calculate daily position averages
        df_position_daily_avg = df_long.groupby(['Date', 'Position'])['Value'].mean().reset_index()
        
        return df, df_long, df_position_daily_avg
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# Define the tabs with Truman colors
tabs = dbc.Tabs(
    [
        dbc.Tab(
            label="Dashboard", 
            tab_id="tab-overview",
            label_style={
                "background-color": TRUMAN_PURPLE, 
                "color": TRUMAN_WHITE,
                "border-color": TRUMAN_PURPLE,
                "font-weight": "bold"
            },
            active_label_style={
                "background-color": TRUMAN_LIGHT_BLUE,
                "color": TRUMAN_WHITE,
                "border-color": TRUMAN_LIGHT_BLUE
            }
        ),

        dbc.Tab(
    label="CSV", 
    tab_id="tab-csv",
    label_style={
        "background-color": TRUMAN_PURPLE, 
        "color": TRUMAN_WHITE,
        "border-color": TRUMAN_PURPLE,
        "font-weight": "bold"
    },
    active_label_style={
        "background-color": TRUMAN_LIGHT_BLUE,
        "color": TRUMAN_WHITE,
        "border-color": TRUMAN_LIGHT_BLUE
    }
),
        dbc.Tab(
            label="Notifications", 
            tab_id="tab-notifications",
            label_style={
                "background-color": TRUMAN_PURPLE, 
                "color": TRUMAN_WHITE,
                "border-color": TRUMAN_PURPLE,
                "font-weight": "bold"
            },
            active_label_style={
                "background-color": TRUMAN_LIGHT_BLUE,
                "color": TRUMAN_WHITE,
                "border-color": TRUMAN_LIGHT_BLUE
            }
        ),
    ],
    id="dashboard-tabs",
    active_tab="tab-overview",
    style={"border-bottom": f"2px solid {TRUMAN_PURPLE}"}
)

# Define the layout with Truman State University styling
dash_app.layout = html.Div([
    # Header with Truman styling
    html.Div([
        html.H1('Truman State Bulldogs - RPE', 
                style={
                    'textAlign': 'center', 
                    'margin': '20px',
                    'color': TRUMAN_PURPLE,
                    'fontWeight': 'bold'
                }),
        html.Div([
        
        ], style={'textAlign': 'center'})
    ], style={
        'backgroundColor': TRUMAN_WHITE,
        'padding': '10px',
        'borderBottom': f'5px solid {TRUMAN_LIGHT_BLUE}',
        'marginBottom': '20px'
    }),
    
    # Refresh data button and last update timestamp
    html.Div([
        html.Button("Refresh Data", id="refresh-data-btn", n_clicks=0,
                    style={
                        'background': TRUMAN_PURPLE, 
                        'color': TRUMAN_WHITE, 
                        'border': 'none', 
                        'padding': '10px', 
                        'borderRadius': '5px', 
                        'marginRight': '10px',
                        'fontWeight': 'bold'
                    }),
        html.Div(id="last-update", style={'marginTop': '5px', 'fontSize': '0.8em', 'color': '#666'})
    ], style={'textAlign': 'right', 'margin': '10px'}),
    
    # Tabs for different views
    tabs,
    
    # Content of each tab
    html.Div(id="tab-content", style={'margin': '20px'}),
    
    # Hidden div to store the data
    html.Div(id='data-store', style={'display': 'none'}),
    
    # Footer with Truman branding
    html.Div([
        html.P("It's a Great Day To Be a Bulldog!",
               style={
                   'textAlign': 'center',
                   'color': TRUMAN_WHITE,
                   'margin': '10px'
               })
    ], style={
        'backgroundColor': TRUMAN_PURPLE,
        'padding': '10px',
        'marginTop': '30px'
    })
], style={'fontFamily': 'Arial, sans-serif'})

# Callback to update the tab content based on the active tab
@dash_app.callback(
    Output("tab-content", "children"),
    [Input("dashboard-tabs", "active_tab"),
     Input("data-store", "children")]
)
def render_tab_content(active_tab, json_data):
    if not json_data:
        return html.Div([
            html.H3("Welcome to Truman State Bulldogs Workout Tracker!", style={'color': TRUMAN_PURPLE}),
            html.P("Please click 'Refresh Data' to load the dashboard.", style={'fontSize': '1.2em'}),
            html.Div([
                html.Img(src="https://via.placeholder.com/300x200/4F2D7F/FFFFFF?text=Truman+State+Bulldogs", 
                         style={'display': 'block', 'margin': 'auto', 'borderRadius': '10px'})
            ], style={'textAlign': 'center', 'margin': '40px'})
        ], style={'textAlign': 'center', 'padding': '30px'})
    
    data_dict = json.loads(json_data)
    
    # Debug information
    column_info = data_dict.get('column_info', {})
    
    # Load data from storage
    df_position_avg = pd.read_json(StringIO(data_dict['df_position_avg']), orient='split')
    df_position_daily_avg = pd.read_json(StringIO(data_dict['df_position_daily_avg']), orient='split')
    df = pd.read_json(StringIO(data_dict['df']), orient='split')
    
    # Ensure dates are properly parsed
    if 'Date' in df_position_daily_avg.columns:
        df_position_daily_avg['Date'] = pd.to_datetime(df_position_daily_avg['Date'], errors='coerce')
    
    if active_tab == "tab-overview":
        return render_overview_tab(df_position_avg, df_position_daily_avg)
    elif active_tab == "tab-notifications":
        return render_notifications_tab()
    elif active_tab == "tab-csv":
        return render_csv_tab(df)

    
    return html.Div("This tab's content is being developed.")

def render_csv_tab(df):
    return html.Div([
        html.H3("Full CSV Data Table", style={
            'color': TRUMAN_PURPLE,
            'fontWeight': 'bold',
            'marginBottom': '20px',
            'textAlign': 'center'
        }),

        html.Div([
            html.Label("Search by Player Name:", style={
                'fontWeight': 'bold',
                'color': TRUMAN_PURPLE
            }),
            dcc.Input(
                id='csv-search-input',
                type='text',
                placeholder='Enter player name...',
                style={
                    'width': '100%',
                    'padding': '10px',
                    'border': f'2px solid {TRUMAN_PURPLE}',
                    'borderRadius': '5px',
                    'marginBottom': '20px'
                }
            )
        ]),

        dash_table.DataTable(
            id='csv-data-table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            page_size=20,
            style_table={
                'overflowX': 'auto',
                'border': f'1px solid {TRUMAN_PURPLE}'
            },
            style_header={
                'backgroundColor': TRUMAN_PURPLE_LIGHT,
                'color': 'white',
                'fontWeight': 'bold'
            },
            style_cell={
                'textAlign': 'center',
                'backgroundColor': TRUMAN_WHITE,
                'color': TRUMAN_PURPLE,
                'minWidth': '100px',
                'whiteSpace': 'normal'
            },
            sort_action="native",
            filter_action="native",
            fixed_rows={'headers': True}
        )
    ])

def render_overview_tab(df_position_avg, df_position_daily_avg):
    # Check if we have date values to calculate week-over-week changes
    has_date_values = not df_position_daily_avg.empty and 'Date' in df_position_daily_avg.columns
    
    # Only calculate weekly changes if we have date values
    if has_date_values:
        try:
            df_position_daily_avg['Week'] = df_position_daily_avg['Date'].dt.isocalendar().week
            df_weekly_avg = df_position_daily_avg.groupby(['Position', 'Week'])['Value'].mean().reset_index()
            df_weekly_change = df_weekly_avg.copy()
            df_weekly_change['PrevWeekValue'] = df_weekly_change.groupby('Position')['Value'].shift(1)
            df_weekly_change['WeeklyChange'] = df_weekly_change['Value'] - df_weekly_change['PrevWeekValue']
            df_weekly_change['PercentChange'] = (df_weekly_change['WeeklyChange'] / df_weekly_change['PrevWeekValue']) * 100
            df_weekly_change.dropna(inplace=True)
        except Exception as e:
            print(f"Error calculating weekly changes: {str(e)}")
            df_weekly_change = pd.DataFrame(columns=['Position', 'Week', 'Value', 'PrevWeekValue', 'WeeklyChange', 'PercentChange'])
    else:
        df_weekly_change = pd.DataFrame(columns=['Position', 'Week', 'Value', 'PrevWeekValue', 'WeeklyChange', 'PercentChange'])
    
    # Get unique positions for the filter dropdown
    positions = []
    if not df_position_avg.empty and 'Position' in df_position_avg.columns:
        positions = df_position_avg['Position'].unique().tolist()
    
    # Overview Tab Content with Truman styling
    return html.Div([
        html.H3("Bulldog RPE Dashboard", 
                style={
                    'marginBottom': '20px', 
                    'color': TRUMAN_PURPLE,
                    'textAlign': 'center',
                    'fontWeight': 'bold',
                    'borderBottom': f'2px solid {TRUMAN_LIGHT_BLUE}',
                    'paddingBottom': '10px'
                }),
        
        # Add position filter dropdown with Truman styling
        dbc.Card([
            dbc.CardHeader("Position Filters", 
                          style={
                              'backgroundColor': TRUMAN_PURPLE, 
                              'color': TRUMAN_WHITE,
                              'fontWeight': 'bold'
                          }),
            dbc.CardBody([
                html.Label("Select Position(s):", style={'fontWeight': 'bold', 'color': TRUMAN_PURPLE}),
                dcc.Dropdown(
                    id='position-filter-dropdown',
                    options=[{'label': pos, 'value': pos} for pos in positions],
                    value=positions,  # Default to ALL positions
                    multi=True,
                    placeholder="Select positions to display",
                    style={
                        'border': f'1px solid {TRUMAN_PURPLE}',
                        'borderRadius': '5px'
                    }
                )
            ], style={'backgroundColor': TRUMAN_WHITE})
        ], style={
            'marginBottom': '20px', 
            'border': f'1px solid {TRUMAN_PURPLE}',
            'borderRadius': '10px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        }),
        
        # Position Averages Graph with Truman styling
        dbc.Card([
            dbc.CardHeader("Average RPE Value by Position", 
                          style={
                              'backgroundColor': TRUMAN_PURPLE, 
                              'color': TRUMAN_WHITE,
                              'fontWeight': 'bold'
                          }),
            dbc.CardBody([
                dcc.Graph(id='position-avg-graph')
            ], style={'backgroundColor': TRUMAN_WHITE})
        ], style={
            'marginBottom': '20px', 
            'border': f'1px solid {TRUMAN_PURPLE}',
            'borderRadius': '10px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        }),
        
        # Position Daily Averages Graph with Truman styling
        dbc.Card([
            dbc.CardHeader("Position Group Average Change Over Time", 
                          style={
                              'backgroundColor': TRUMAN_PURPLE, 
                              'color': TRUMAN_WHITE,
                              'fontWeight': 'bold'
                          }),
            dbc.CardBody([
                dcc.Graph(id='position-time-graph')
            ], style={'backgroundColor': TRUMAN_WHITE})
        ], style={
            'marginBottom': '20px', 
            'border': f'1px solid {TRUMAN_PURPLE}',
            'borderRadius': '10px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        }),
        
        # Weekly Change Table with Truman styling
        dbc.Card([
            dbc.CardHeader("Week-over-Week Changes by Position", 
                          style={
                              'backgroundColor': TRUMAN_PURPLE, 
                              'color': TRUMAN_WHITE,
                              'fontWeight': 'bold'
                          }),
            dbc.CardBody([
                dash_table.DataTable(
                    id='weekly-change-table',
                    columns=[
                        {"name": "Position", "id": "Position"},
                        {"name": "Week", "id": "Week"},
                        {"name": "Average Value", "id": "Value", "type": "numeric", "format": {"specifier": ".2f"}},
                        {"name": "Weekly Change", "id": "WeeklyChange", "type": "numeric", "format": {"specifier": ".2f"}},
                        {"name": "% Change", "id": "PercentChange", "type": "numeric", "format": {"specifier": ".1f", "locale": {"symbol": ["", "%"]}}}
                    ],
                    data=df_weekly_change.to_dict('records'),
                    style_data_conditional=[
                        {
                            'if': {
                                'filter_query': '{WeeklyChange} > 0',
                                'column_id': 'WeeklyChange'
                            },
                            'color': 'green'
                        },
                        {
                            'if': {
                                'filter_query': '{WeeklyChange} < 0',
                                'column_id': 'WeeklyChange'
                            },
                            'color': 'red'
                        }
                    ],
                    style_header={
                        'backgroundColor': TRUMAN_PURPLE_LIGHT,
                        'color': 'white',
                        'fontWeight': 'bold'
                    },
                    style_cell={
                        'textAlign': 'center'
                    },
                    style_data={
                        'backgroundColor': TRUMAN_WHITE
                    },
                    style_table={
                        'overflowX': 'auto',
                        'border': f'1px solid {TRUMAN_PURPLE}'
                    },
                    sort_action="native",
                    filter_action="native",
                    page_size=10
                )
            ], style={'backgroundColor': TRUMAN_WHITE})
        ], style={
            'marginBottom': '20px', 
            'border': f'1px solid {TRUMAN_PURPLE}',
            'borderRadius': '10px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        }),
        
        # Individual Player Data with Truman styling
        dbc.Card([
            dbc.CardHeader("Individual Player RPE",
                          style={
                              'backgroundColor': TRUMAN_PURPLE, 
                              'color': TRUMAN_WHITE,
                              'fontWeight': 'bold'
                          }),
            dbc.CardBody([
                dcc.Graph(id='player-performance-graph')
            ], style={'backgroundColor': TRUMAN_WHITE})
        ], style={
            'border': f'1px solid {TRUMAN_PURPLE}',
            'borderRadius': '10px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        })
    ])

def render_notifications_tab():
    return html.Div([
        html.H3("Bulldog Team Notifications", 
                style={
                    'marginBottom': '20px', 
                    'color': TRUMAN_PURPLE,
                    'textAlign': 'center',
                    'fontWeight': 'bold',
                    'borderBottom': f'2px solid {TRUMAN_LIGHT_BLUE}',
                    'paddingBottom': '10px'
                }),
        
        # Athlete reminders card
        dbc.Card([
            dbc.CardHeader("Send Workout Reminders", 
                          style={
                              'backgroundColor': TRUMAN_PURPLE, 
                              'color': TRUMAN_WHITE,
                              'fontWeight': 'bold'
                          }),
            dbc.CardBody([
                html.Label("Send reminders to all athletes:", 
                          style={
                              'fontWeight': 'bold',
                              'color': TRUMAN_PURPLE,
                              'fontSize': '1.1em'
                          }),
                html.Button("Send Reminders", 
                            id="send-reminders-btn", 
                            n_clicks=0, 
                            style={
                                'marginLeft': '10px', 
                                'background': TRUMAN_LIGHT_BLUE, 
                                'color': 'white', 
                                'border': 'none', 
                                'padding': '10px', 
                                'borderRadius': '5px',
                                'fontWeight': 'bold'
                            }),
                html.Div(id="email-status", style={'marginTop': '20px', 'padding': '10px'})
            ], style={'backgroundColor': TRUMAN_WHITE})
        ], style={
            'border': f'1px solid {TRUMAN_PURPLE}',
            'borderRadius': '10px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
            'marginBottom': '20px'
        }),
        
        # Coach reports card - SIMPLIFIED
        dbc.Card([
            dbc.CardHeader("Send Reports to Coaches", 
                          style={
                              'backgroundColor': TRUMAN_PURPLE, 
                              'color': TRUMAN_WHITE,
                              'fontWeight': 'bold'
                          }),
            dbc.CardBody([
                html.P("Click the button below to generate and send performance reports to the coaching staff:", 
                      style={
                          'color': TRUMAN_PURPLE,
                          'fontSize': '1.1em',
                          'marginBottom': '15px'
                      }),
                html.Div([
                    html.P(f"Coach emails: {', '.join(COACH_EMAILS)}", 
                          style={
                              'fontSize': '0.9em', 
                              'color': '#666', 
                              'fontStyle': 'italic',
                              'marginBottom': '15px'
                          }),
                ]),
                html.Button("Generate & Send Reports", 
                            id="send-coach-reports-btn", 
                            n_clicks=0, 
                            style={
                                'background': TRUMAN_LIGHT_BLUE, 
                                'color': 'white', 
                                'border': 'none', 
                                'padding': '10px', 
                                'borderRadius': '5px',
                                'fontWeight': 'bold'
                            }),
                            
                html.Div(id="coach-report-status", style={'marginTop': '20px', 'padding': '10px'})
            ], style={'backgroundColor': TRUMAN_WHITE})
        ], style={
            'border': f'1px solid {TRUMAN_PURPLE}',
            'borderRadius': '10px',
            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
        })
    ])

# Callback to refresh data
@dash_app.callback(
    [Output('data-store', 'children'),
     Output('last-update', 'children')],
    [Input('refresh-data-btn', 'n_clicks')]
)
def refresh_data(n_clicks):
    df, df_long, df_position_daily_avg = get_data_from_csv()
    
    # Create Name field from first and last name if needed
    if 'First Name' in df.columns and 'Last Name' in df.columns and 'Name' not in df.columns:
        df['Name'] = df['First Name'] + ' ' + df['Last Name']
    
    # Since you mentioned you have date columns after specific fields,
    # let's identify and process those date columns
    base_columns = ['Email', 'Last 4 Digits', 'Last Name', 'First Name', 'Position', 'Summer Attendance', 'Name']
    potential_date_columns = [col for col in df.columns if col not in base_columns]
    
    # Calculate average value per athlete (make sure values are numeric)
    numeric_date_columns = []
    for col in potential_date_columns:
        # Check if column contains numeric data
        try:
            # Convert to numeric and handle errors
            df[col] = pd.to_numeric(df[col], errors='coerce')
            numeric_date_columns.append(col)
        except:
            print(f"Column {col} could not be converted to numeric")
    
    # Only use numeric columns for average calculation
    if numeric_date_columns:
        df['Average Value'] = df[numeric_date_columns].mean(axis=1, skipna=True)
        # Check for unreasonably high values (RPE is typically 0-10)
        if df['Average Value'].max() > 10:
            print(f"Warning: Found unusually high average values. Max value: {df['Average Value'].max()}")
            # Scale down values based on their magnitude
            if (df['Average Value'] > 100).any():
                # Values over 100 get divided by 100
                df.loc[df['Average Value'] > 100, 'Average Value'] = df.loc[df['Average Value'] > 100, 'Average Value'] / 100
            
            if (df['Average Value'] > 10).any():
                # Values between 10 and 100 get divided by 10
                df.loc[df['Average Value'] > 10, 'Average Value'] = df.loc[df['Average Value'] > 10, 'Average Value'] / 10
            
            # Final safety check - cap at 10
            df.loc[df['Average Value'] > 10, 'Average Value'] = 10.0
    
    # Ensure dates are properly parsed
    if df_position_daily_avg is not None and 'Date' in df_position_daily_avg.columns:
        df_position_daily_avg['Date'] = pd.to_datetime(df_position_daily_avg['Date'], errors='coerce')
    
    # Create JSON data structure for storage
    data_json = {
        'df': df.to_json(orient='split')
    }
    
    # Also store the restructured long-format data if available
    if 'df_long' in locals() and not df_long.empty:
        data_json['df_long'] = df_long.to_json(orient='split')
    
    # Add position averages if we have the necessary columns
    if 'Position' in df.columns and 'Average Value' in df.columns:
        position_avg = df.groupby('Position')['Average Value'].mean().reset_index()
        
        # Check if position averages are unreasonably high (typical RPE is 0-10)
        if position_avg['Average Value'].max() > 10:
            print(f"Warning: Position averages appear to be too high. Max: {position_avg['Average Value'].max()}")
            
            # Apply different scaling based on magnitude of values
            if (position_avg['Average Value'] > 100).any():
                # Values over 100 get divided by 100
                position_avg.loc[position_avg['Average Value'] > 100, 'Average Value'] = position_avg.loc[position_avg['Average Value'] > 100, 'Average Value'] / 100
            
            if (position_avg['Average Value'] > 10).any():
                # Values between 10 and 100 get divided by 10
                position_avg.loc[position_avg['Average Value'] > 10, 'Average Value'] = position_avg.loc[position_avg['Average Value'] > 10, 'Average Value'] / 10
            
            # Final safety check - cap at 10
            position_avg.loc[position_avg['Average Value'] > 10, 'Average Value'] = 10.0
            
        data_json['df_position_avg'] = position_avg.to_json(orient='split')
    else:
        # Create empty dataframe with expected structure
        data_json['df_position_avg'] = pd.DataFrame(columns=['Position', 'Average Value']).to_json(orient='split')
    
    # Add daily position averages if available
    if df_position_daily_avg is not None and not df_position_daily_avg.empty:
        data_json['df_position_daily_avg'] = df_position_daily_avg.to_json(orient='split')
    else:
        # Create empty dataframe with expected structure
        data_json['df_position_daily_avg'] = pd.DataFrame(columns=['Date', 'Position', 'Value']).to_json(orient='split')
    
    # Include column information to help with debugging
    data_json['column_info'] = {
        'df_columns': df.columns.tolist(),
        'has_position': 'Position' in df.columns,
        'has_name': 'Name' in df.columns,
        'has_average_value': 'Average Value' in df.columns
    }
    
    last_update_text = f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    return json.dumps(data_json), last_update_text

# Add new callbacks for the position filter and individual player data
@dash_app.callback(
    [Output('position-avg-graph', 'figure'),
     Output('position-time-graph', 'figure'),
     Output('weekly-change-table', 'data'),
     Output('player-performance-graph', 'figure')],
    [Input('position-filter-dropdown', 'value'),
     Input('data-store', 'children')]
)
def update_filtered_graphs(selected_positions, json_data):
    # Create empty default figures and data
    empty_bar = px.bar(
        pd.DataFrame(columns=['Position', 'Value']), 
        x='Position', 
        y='Value', 
        title="No data available"
    ).update_layout(
        template="plotly_white",
        plot_bgcolor=TRUMAN_WHITE,
        paper_bgcolor=TRUMAN_WHITE,
        font=dict(family="Arial, sans-serif", color=TRUMAN_PURPLE)
    )
    
    empty_line = px.line(
        pd.DataFrame(columns=['Date', 'Position', 'Value']), 
        x='Date', 
        y='Value', 
        title="No data available"
    ).update_layout(
        template="plotly_white",
        plot_bgcolor=TRUMAN_WHITE,
        paper_bgcolor=TRUMAN_WHITE,
        font=dict(family="Arial, sans-serif", color=TRUMAN_PURPLE)
    )
    
    empty_player = px.line(
        pd.DataFrame(columns=['Date', 'Name', 'Value']), 
        x='Date', 
        y='Value', 
        title="No player data available"
    ).update_layout(
        template="plotly_white",
        plot_bgcolor=TRUMAN_WHITE,
        paper_bgcolor=TRUMAN_WHITE,
        font=dict(family="Arial, sans-serif", color=TRUMAN_PURPLE)
    )
    
    if not json_data or not selected_positions or len(selected_positions) == 0:
        # Return empty figures if no data or no positions selected
        return empty_bar, empty_line, [], empty_player
    
    data_dict = json.loads(json_data)
    df_position_avg = pd.read_json(StringIO(data_dict['df_position_avg']), orient='split')
    df_position_daily_avg = pd.read_json(StringIO(data_dict['df_position_daily_avg']), orient='split')
    df = pd.read_json(StringIO(data_dict['df']), orient='split')
    
    # Filter data for selected positions
    filtered_position_avg = df_position_avg[df_position_avg['Position'].isin(selected_positions)]
    
    # Ensure dates are properly parsed for time series data
    if 'Date' in df_position_daily_avg.columns:
        df_position_daily_avg['Date'] = pd.to_datetime(df_position_daily_avg['Date'], errors='coerce')
    
    # Filter time series data by selected positions
    filtered_position_daily_avg = df_position_daily_avg[df_position_daily_avg['Position'].isin(selected_positions)]
    
    # Create bar chart for position averages with Truman theming
    bar_fig = px.bar(
        filtered_position_avg, 
        x='Position', 
        y='Average Value', 
        title="Average Summer Workout Value per Position",
        color='Position', 
        color_discrete_sequence=TRUMAN_COLOR_SEQUENCE
    )
    
    # Update the bar chart layout with Truman styling
    bar_fig.update_layout(
        template="plotly_white",
        plot_bgcolor=TRUMAN_WHITE,
        paper_bgcolor=TRUMAN_WHITE,
        font=dict(family="Arial, sans-serif", color=TRUMAN_PURPLE),
        title_font=dict(size=18, color=TRUMAN_PURPLE, family="Arial, sans-serif"),
        legend_title_font=dict(size=14, color=TRUMAN_PURPLE),
        legend_font=dict(size=12, color=TRUMAN_PURPLE),
        xaxis_title_font=dict(size=14, color=TRUMAN_PURPLE),
        yaxis_title_font=dict(size=14, color=TRUMAN_PURPLE),
        xaxis_title="Position",
        yaxis_title="Average RPE Value"
    )
    
    # Create time series chart with Truman theming
    if 'Date' in filtered_position_daily_avg.columns and not filtered_position_daily_avg.empty:
        line_fig = px.line(
            filtered_position_daily_avg, 
            x='Date', 
            y='Value', 
            color='Position',
            title="Position Group Average Change Over Time", 
            markers=True,
            color_discrete_sequence=TRUMAN_COLOR_SEQUENCE
        )
        
        # Update the line chart layout with Truman styling
        line_fig.update_layout(
            template="plotly_white",
            plot_bgcolor=TRUMAN_WHITE,
            paper_bgcolor=TRUMAN_WHITE,
            font=dict(family="Arial, sans-serif", color=TRUMAN_PURPLE),
            title_font=dict(size=18, color=TRUMAN_PURPLE, family="Arial, sans-serif"),
            legend_title_font=dict(size=14, color=TRUMAN_PURPLE),
            legend_font=dict(size=12, color=TRUMAN_PURPLE),
            xaxis_title_font=dict(size=14, color=TRUMAN_PURPLE),
            yaxis_title_font=dict(size=14, color=TRUMAN_PURPLE),
            xaxis_title="Date",
            yaxis_title="Average RPE Value",
            legend_title="Position",
            hovermode="closest"
        )
    else:
        line_fig = px.line(
            pd.DataFrame({'Date': [], 'Value': [], 'Position': []}), 
            x='Date', 
            y='Value', 
            title="No time series data available"
        ).update_layout(
            template="plotly_white",
            plot_bgcolor=TRUMAN_WHITE,
            paper_bgcolor=TRUMAN_WHITE,
            font=dict(family="Arial, sans-serif", color=TRUMAN_PURPLE)
        )
    
    # Filter and prepare weekly change data
    weekly_change_data = []
    
    # Check if we have date values to calculate week-over-week changes
    has_date_values = not df_position_daily_avg.empty and 'Date' in df_position_daily_avg.columns
    
    if has_date_values:
        try:
            # Calculate weekly averages and changes
            df_position_daily_avg['Week'] = df_position_daily_avg['Date'].dt.isocalendar().week
            df_weekly_avg = df_position_daily_avg.groupby(['Position', 'Week'])['Value'].mean().reset_index()
            
            # Filter by selected positions
            df_weekly_avg = df_weekly_avg[df_weekly_avg['Position'].isin(selected_positions)]
            
            # Calculate week-over-week changes
            df_weekly_change = df_weekly_avg.copy()
            df_weekly_change['PrevWeekValue'] = df_weekly_change.groupby('Position')['Value'].shift(1)
            df_weekly_change['WeeklyChange'] = df_weekly_change['Value'] - df_weekly_change['PrevWeekValue']
            df_weekly_change['PercentChange'] = (df_weekly_change['WeeklyChange'] / df_weekly_change['PrevWeekValue']) * 100
            df_weekly_change.dropna(inplace=True)
            
            weekly_change_data = df_weekly_change.to_dict('records')
        except Exception as e:
            print(f"Error calculating weekly changes: {str(e)}")
    
    # Create individual player performance graph with Truman theming
    player_fig = empty_player
    
    # If we have player data in the original dataset
    try:
        # Get individual player data for the selected positions
        player_data = []
        
        # Use the original dataset
        if 'Position' in df.columns and 'Name' in df.columns:
            filtered_players = df[df['Position'].isin(selected_positions)]
            
            # Reconstruct time series from date columns
            base_columns = ['Email', 'Last 4 Digits', 'Last Name', 'First Name', 'Position', 'Summer Attendance', 'Name', 'Average Value']
            date_columns = [col for col in df.columns if col not in base_columns]
            
            for _, player in filtered_players.iterrows():
                player_position = player['Position']
                player_name = player['Name'] if 'Name' in player else ""
                # For display purposes, use Last Name instead of full name if available
                display_name = player['Last Name'] if 'Last Name' in player else player_name
                
                if not display_name or pd.isna(display_name):
                    continue  # Skip players without names
                
                for date_col in date_columns:
                    value = player[date_col]
                    if pd.notna(value) and value != '' and not pd.isna(value):
                        try:
                            # Convert to numeric value
                            numeric_value = float(value)
                            
                            # Apply appropriate scaling
                            if numeric_value > 100:
                                numeric_value = numeric_value / 100
                            elif numeric_value > 10:
                                numeric_value = numeric_value / 10
                                
                            # Cap at 10
                            numeric_value = min(numeric_value, 10)
                            
                            # Parse date - add error handling
                            try:
                                parsed_date = pd.to_datetime(date_col, errors='coerce')
                                if pd.isnull(parsed_date):
                                    continue  # Skip invalid dates
                                
                                player_data.append({
                                    'Name': display_name,
                                    'Position': player_position,
                                    'Date': parsed_date,
                                    'Value': numeric_value
                                })
                            except:
                                continue  # Skip if date parsing fails
                        except:
                            continue  # Skip if value conversion fails
        
        # Create player performance graph if we have data
        if len(player_data) > 0:
            player_df = pd.DataFrame(player_data)
            
            # Sort by date to show trends properly
            player_df = player_df.sort_values('Date')
            
            # Create line chart showing individual player performance with Truman theming
            player_fig = px.line(
                player_df,
                x='Date',
                y='Value',
                color='Name',
                title=f"Individual Bulldog Athletes - {', '.join(selected_positions)} Position(s)",
                markers=True,
                color_discrete_sequence=TRUMAN_COLOR_SEQUENCE
            )
            
            # Update the player chart layout with Truman styling
            player_fig.update_layout(
                template="plotly_white",
                plot_bgcolor=TRUMAN_WHITE,
                paper_bgcolor=TRUMAN_WHITE,
                font=dict(family="Arial, sans-serif", color=TRUMAN_PURPLE),
                title_font=dict(size=18, color=TRUMAN_PURPLE, family="Arial, sans-serif"),
                legend_title_font=dict(size=14, color=TRUMAN_PURPLE),
                legend_font=dict(size=12, color=TRUMAN_PURPLE),
                xaxis_title_font=dict(size=14, color=TRUMAN_PURPLE),
                yaxis_title_font=dict(size=14, color=TRUMAN_PURPLE),
                xaxis_title="Date",
                yaxis_title="RPE Value",
                legend_title="Player",
                hovermode="closest"
            )
            
            # Add a dotted line for the position average as reference with Truman styling
            for position in selected_positions:
                position_data = filtered_position_daily_avg[filtered_position_daily_avg['Position'] == position]
                if not position_data.empty:
                    player_fig.add_trace(
                        go.Scatter(
                            x=position_data['Date'],
                            y=position_data['Value'],
                            mode='lines',
                            line=dict(dash='dash', width=2, color=TRUMAN_PURPLE),
                            name=f"{position} Average",
                            opacity=0.7
                        )
                    )
    except Exception as e:
        print(f"Error creating player performance chart: {str(e)}")
        player_fig = px.line(
            pd.DataFrame({'Date': [], 'Name': [], 'Value': []}),
            x='Date',
            y='Value',
            title="Error loading player data"
        ).update_layout(
            template="plotly_white",
            plot_bgcolor=TRUMAN_WHITE,
            paper_bgcolor=TRUMAN_WHITE,
            font=dict(family="Arial, sans-serif", color=TRUMAN_PURPLE)
        )
    
    return bar_fig, line_fig, weekly_change_data, player_fig

# Callback for email notifications
@dash_app.callback(
    Output('email-status', 'children'),
    [Input('send-reminders-btn', 'n_clicks')],
    [State('data-store', 'children')]
)
def send_reminders(n_clicks, json_data):
    if n_clicks == 0:
        return ""
    
    if not json_data:
        return html.Div("Please refresh data before sending reminders.", 
                        style={'color': 'red', 'fontWeight': 'bold', 'padding': '10px'})
    
    data_dict = json.loads(json_data)
    df = pd.read_json(StringIO(data_dict['df']), orient='split')
    
    success_count = 0
    fail_count = 0

    # Make sure we have the email column
    if 'Email' not in df.columns:
        return html.Div("Error: Could not find 'Email' column in your data.", 
                        style={'color': 'red', 'fontWeight': 'bold', 'padding': '10px'})

    if not email_module_available:
        return html.Div("Email notification module is not available. Please ensure emailNotif.py is properly set up.", 
                       style={'color': 'red', 'fontWeight': 'bold', 'padding': '10px'})

    # Filter out any rows where the email is blank or None
    valid_emails = df["Email"].dropna().unique()

    for email in valid_emails:
        if email == "":  # Skip empty emails
            continue
        
        # Get athlete name if available
        athlete_name = ""
        if 'Name' in df.columns:
            matching_rows = df[df['Email'] == email]
            if not matching_rows.empty and 'Name' in matching_rows.columns:
                athlete_name = matching_rows['Name'].iloc[0]
        
        # Personalize the message if we have the athlete's name
        greeting = f"Hello {athlete_name}," if athlete_name else "Hello,"
        
        # Send simple reminder with NO graph but Truman branding
        message = (
            f"{greeting}\n\n"
            f"This is a reminder from the Truman State Bulldogs coaching staff to fill out your RPE data for today's workout.\n"
            f"Your input helps us track and optimize training for our team success.\n\n"
            f"Go Bulldogs!\n"
            f"Truman State University Coaching Staff"
        )
        if send_email(email, subject="Truman Bulldogs - Daily RPE Data Reminder", message=message, include_graph=False):
            success_count += 1
        else:
            fail_count += 1

    # Return styled status message with Truman colors
    return html.Div([
        html.P(f"Emails sent: {success_count} successful, {fail_count} failed.", 
              style={'fontSize': '1.1em', 'fontWeight': 'bold'}),
        html.P(f"Sent at {datetime.now().strftime('%H:%M:%S')}", 
              style={'fontSize': '0.9em', 'color': '#666'})
    ], style={
        'backgroundColor': '#e8f0fe',
        'border': f'1px solid {TRUMAN_PURPLE}',
        'borderRadius': '5px',
        'padding': '15px',
        'color': TRUMAN_PURPLE
    })

# Add a new callback for coach report generation with hardcoded emails
@dash_app.callback(
    Output('coach-report-status', 'children'),
    [Input('send-coach-reports-btn', 'n_clicks')],
    [State('data-store', 'children')]
)
def send_coach_performance_reports(n_clicks, json_data):
    if n_clicks == 0:
        return ""
    
    if not json_data:
        return html.Div(
            "Please refresh data before generating reports.", 
            style={'color': 'red', 'fontWeight': 'bold', 'padding': '10px'}
        )
    
    if not email_module_available:
        return html.Div("Email and report modules are not available. Please ensure coachReport.py is properly set up.", 
                       style={'color': 'red', 'fontWeight': 'bold', 'padding': '10px'})
    
    # Use the hardcoded coach emails
    selected_coaches = COACH_EMAILS
    
    # Load data from the data store
    data_dict = json.loads(json_data)
    df = pd.read_json(StringIO(data_dict['df']), orient='split')
    df_position_avg = pd.read_json(StringIO(data_dict['df_position_avg']), orient='split')
    df_position_daily_avg = pd.read_json(StringIO(data_dict['df_position_daily_avg']), orient='split')
    
    # Ensure dates are properly parsed
    if 'Date' in df_position_daily_avg.columns:
        df_position_daily_avg['Date'] = pd.to_datetime(df_position_daily_avg['Date'], errors='coerce')
    
    try:
        # Generate and send coach reports
        result = generate_coach_report(
            df=df,
            df_position_avg=df_position_avg,
            df_position_daily_avg=df_position_daily_avg,
            selected_coaches=selected_coaches
        )
        
        # Return styled status message with Truman colors
        return html.Div([
            html.P(result["message"], style={'fontSize': '1.1em', 'fontWeight': 'bold'}),
            html.P(f"Sent at {datetime.now().strftime('%H:%M:%S')}", style={'fontSize': '0.9em', 'color': '#666'})
        ], style={
            'backgroundColor': '#e8f0fe',
            'border': f'1px solid {TRUMAN_PURPLE}',
            'borderRadius': '5px',
            'padding': '15px',
            'color': TRUMAN_PURPLE
        })
        
    except Exception as e:
        # Handle errors gracefully
        error_message = str(e)
        return html.Div(
            f"Error generating coach reports: {error_message}", 
            style={'color': 'red', 'fontWeight': 'bold', 'padding': '10px'}
        )

@dash_app.callback(
    Output('csv-data-table', 'data'),
    [Input('csv-search-input', 'value'),
     Input('data-store', 'children')]
)
def filter_csv_table(search_value, json_data):
    if not json_data:
        return []

    data_dict = json.loads(json_data)
    df = pd.read_json(StringIO(data_dict['df']), orient='split')

    if search_value and search_value.strip():
        search_value = search_value.lower()
        if 'Name' in df.columns:
            df = df[df['Name'].str.lower().str.contains(search_value, na=False)]
        else:
            df = df[df['First Name'].str.lower().str.contains(search_value, na=False) |
                    df['Last Name'].str.lower().str.contains(search_value, na=False)]

    return df.to_dict('records')


if __name__ == '__main__':
    # Run the Flask app on port 4025 (originally used by your form submission server)
    # The dashboard will be accessible at http://127.0.0.1:4025/dashboard/
    flask_app.run(debug=True, port=4025)