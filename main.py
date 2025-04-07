import json
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import datetime
import pandas as pd
import dash_bootstrap_components as dbc  # For better styling (optional)
from emailNotif import send_email
from pythonCSV import get_data_from_sheets
from io import StringIO

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div([ 
    html.H1('Summer Workout Position Averages', style={'textAlign': 'center', 'margin': '20px'}),
    html.Div([ 
        html.H3("Email Notifications"),
        html.Div([ 
            html.Label("Send reminders to all athletes:"),
            html.Button("Send Reminders", id="send-reminders-btn", n_clicks=0, 
                        style={'marginLeft': '10px', 'background': '#4CAF50', 'color': 'white', 'border': 'none', 'padding': '10px', 'borderRadius': '5px'}),
            html.Div(id="email-status", style={'marginTop': '10px'})
        ], style={'marginBottom': '20px'}),
        html.Button("Refresh Data", id="refresh-data-btn", n_clicks=0, 
                    style={'background': '#2196F3', 'color': 'white', 'border': 'none', 'padding': '10px', 'borderRadius': '5px', 'marginRight': '10px'}),
        html.Div(id="last-update", style={'marginTop': '5px', 'fontSize': '0.8em', 'color': '#666'})
    ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px', 'margin': '20px'}),
    html.Div([ 
        dcc.Graph(id='position-averages'),
        dcc.Graph(id='position-daily-avg')
    ]),
    html.Div(id='data-store', style={'display': 'none'})
])

@app.callback(
    [Output('data-store', 'children'),
     Output('last-update', 'children')],
    [Input('refresh-data-btn', 'n_clicks')]
)
def refresh_data(n_clicks):
    df, df_long, df_position_daily_avg = get_data_from_sheets()
    data_json = {
        'df_position_avg': df.groupby('Position')['Average Value'].mean().reset_index().to_json(orient='split'),
        'df_position_daily_avg': df_position_daily_avg.to_json(orient='split')
    }
    last_update_text = f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    return json.dumps(data_json), last_update_text

@app.callback(
    [Output('position-averages', 'figure'),
     Output('position-daily-avg', 'figure')],
    [Input('data-store', 'children')]
)
def update_graphs(json_data):
    if not json_data:
        df, _, df_position_daily_avg = get_data_from_sheets()
        df_position_avg = df.groupby('Position')['Average Value'].mean().reset_index()
    else:
        data_dict = json.loads(json_data)
        
        # Use StringIO to wrap the JSON string
        df_position_avg = pd.read_json(StringIO(data_dict['df_position_avg']), orient='split')
        df_position_daily_avg = pd.read_json(StringIO(data_dict['df_position_daily_avg']), orient='split')
        
        df_position_daily_avg['Date'] = pd.to_datetime(df_position_daily_avg['Date'])

    bar_fig = px.bar(df_position_avg, x='Position', y='Average Value', title="Average Summer Workout Value per Position",
                     color='Position', color_discrete_sequence=px.colors.qualitative.Vivid)

    line_fig = px.line(df_position_daily_avg, x='Date', y='Value', color='Position',
                       title="Position Group Average Change Over Time", markers=True)

    line_fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Average RPE Value",
        legend_title="Position",
        hovermode="closest"
    )

    return bar_fig, line_fig

@app.callback(
    Output('email-status', 'children'),
    [Input('send-reminders-btn', 'n_clicks')]
)
def send_reminders(n_clicks):
    if n_clicks == 0:
        return ""
    
    df, _, _ = get_data_from_sheets()
    success_count = 0
    fail_count = 0

    # Filter out any rows where the email is blank or None
    valid_emails = df["Email"].dropna().unique()

    for email in valid_emails:
        if email == "":  # Skip empty emails
            continue
        
        # Send simple reminder with NO graph
        message = (
            f"Hello,\n\n"
            f"This is a reminder to fill out your RPE data for today's workout.\n"
            f"Your input helps us track and optimize training.\n\n"
            f"Thank you!"
        )
        if send_email(email, subject="Daily RPE Data Reminder", message=message, include_graph=False):
            success_count += 1
        else:
            fail_count += 1

    return f"Emails sent: {success_count} successful, {fail_count} failed. (Sent at {datetime.now().strftime('%H:%M:%S')})"


if __name__ == '__main__':
    app.run(debug=True)
