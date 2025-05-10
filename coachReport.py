import io
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

import os
from pathlib import Path
from dotenv import load_dotenv

# Get the absolute path to the project root
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from the project root
env_path = BASE_DIR / '.env'
print(f"Loading .env from: {env_path}")
load_dotenv(dotenv_path=env_path)

# Verify environment variables are loaded
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = os.getenv('SMTP_PORT')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
print(f"Loaded email config: Server={SMTP_SERVER}, Port={SMTP_PORT}, Email={SENDER_EMAIL}")

# Specify Truman State Color Palette
TRUMAN_PURPLE = (79/255, 45/255, 127/255)  # RGB for PDF
TRUMAN_LIGHT_BLUE = (0/255, 178/255, 227/255)  # RGB for PDF
TRUMAN_WHITE = (1, 1, 1)

# Function to set performance metric report
def generate_coach_report(df, df_position_avg, df_position_daily_avg, selected_coaches=None):
    """
    Generate and send performance reports to coaches
    
    Parameters:
    -----------
    df : pandas DataFrame
        The main athlete data
    df_position_avg : pandas DataFrame
        Position average data
    df_position_daily_avg : pandas DataFrame
        Daily position average data
    selected_coaches : list, optional
        List of coach emails to send reports to. If None, uses default list.
    
    Returns:
    --------
    dict
        Success/failure counts and status message
    """
    print("Starting coach report generation...")
    
    # Define coaches emails - default list
    default_coaches = [
        "head_coach@truman.edu",
        "assistant_coach@truman.edu",
        "strength_coach@truman.edu"
    ]
    
    # Use emails specified in default_coaches if selected_coaches is empty
    coach_emails = selected_coaches if selected_coaches else default_coaches
    print(f"Preparing to send reports to: {coach_emails}")
    
    try:
        # Create the PDF report and provide UI feedback
        print("Creating PDF report...")
        buffer = create_pdf_report(df, df_position_avg, df_position_daily_avg)
        print("PDF report created successfully")
        
        # Graph creation is skipped in current implementation
        print("Skipping graph creation to avoid errors")
        
        # Success/Failure count for trainers understanding and error handling
        success_count = 0
        fail_count = 0
        
        # Get today's date for the report
        today = datetime.now().strftime('%B %d, %Y')
        
        # Apply scaling to average values if outliers are present
        if 'Average Value' in df.columns:
            df_scaled = df.copy()
            
            # Scale down values that are too high
            if df_scaled['Average Value'].max() > 10:
                # Values over 1000 get divided by 1000
                mask_1000 = df_scaled['Average Value'] > 1000
                df_scaled.loc[mask_1000, 'Average Value'] = df_scaled.loc[mask_1000, 'Average Value'] / 1000
                
                # Values over 100 get divided by 100
                mask_100 = (df_scaled['Average Value'] > 100) & (df_scaled['Average Value'] <= 1000)
                df_scaled.loc[mask_100, 'Average Value'] = df_scaled.loc[mask_100, 'Average Value'] / 100
                
                # Values over 10 get divided by 10
                mask_10 = (df_scaled['Average Value'] > 10) & (df_scaled['Average Value'] <= 100)
                df_scaled.loc[mask_10, 'Average Value'] = df_scaled.loc[mask_10, 'Average Value'] / 10
                
                # Set cap at 10
                df_scaled.loc[df_scaled['Average Value'] > 10, 'Average Value'] = 10.0

            # Find the team average and set it to 0 if no data is present
            team_avg = df_scaled['Average Value'].mean()
        else:
            team_avg = 0
        
        # Email subject and message for coaching staff
        # Call for team average and athlete count
        email_subject = f"Truman Bulldogs - Performance Report {today}"
        email_message = f"""
Hello Coach,

Attached is the latest performance report for the Truman State Bulldogs team as of {today}.

QUICK SUMMARY:
- Team Average RPE: {team_avg:.2f}
- {len(df)} athletes tracked
- Data collected from {len([col for col in df.columns if col not in ['Email', 'Last 4 digits', 'Last Name', 'First Name', 'Position', 'Summer Attendance', 'Name', 'Average Value']])} workout sessions

The report includes a special section highlighting athletes with high acute:chronic workload ratios (>1.35), which may indicate increased injury risk. The A:C ratio now compares the last 7 days of workload to the last 28 days for a more accurate measurement of injury risk.

The full report is attached as a PDF with detailed breakdowns by position and individual athletes.

Go Bulldogs!
Truman State Coaching Staff
"""
        
        # Send emails to coaches
        print("Sending emails to coaches...")

        # Loop through each specificed coach email and send the report
        for email in coach_emails:
            try:
                success = send_email_with_pdf(
                    recipient=email,
                    subject=email_subject,
                    message=email_message,
                    pdf_buffer=buffer
                )
                # Error handling for trainer understanding
                # If the email was sent successfully, increment success count
                # If the email failed to send, increment fail count
                if success:
                    success_count += 1
                    print(f"Successfully sent email to {email}")
                else:
                    fail_count += 1
                    print(f"Failed to send email to {email}")
            except Exception as e:
                print(f"Error sending coach report to {email}: {str(e)}")
                import traceback
                traceback.print_exc()
                fail_count += 1
        # Produce summary of success and failure counts
        return {
            "success_count": success_count,
            "fail_count": fail_count,
            "message": f"Coach reports sent: {success_count} successful, {fail_count} failed."
        }
    
    except Exception as e:
        print(f"Error in generate_coach_report: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success_count": 0,
            "fail_count": len(coach_emails),
            "message": f"Failed to generate coach reports: {str(e)}"
        }

# Future implementation could include a graph of the data *not currently implemented*
def send_email_with_pdf(recipient, subject, message, pdf_buffer):
    """Send email with PDF report attached"""
    
    try:
        # Load credentials from environment variables
        
        SMTP_SERVER = os.getenv('SMTP_SERVER')
        SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
        SENDER_EMAIL = os.getenv('SENDER_EMAIL')
        SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
        
        # Error check for environment variables
        if not all([SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD]):
            print("Missing email configuration in environment variables. Please check your .env file.")
            return False

        # Create email with attachment
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = recipient
        msg["Subject"] = subject

        # Attach the message
        msg.attach(MIMEText(message, "plain"))
        
        # Attach the PDF
        pdf_buffer.seek(0)  # Reset buffer position to beginning
        pdf_attachment = MIMEApplication(pdf_buffer.read(), _subtype="pdf")
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename="TrumanBulldogs_Report.pdf")
        msg.attach(pdf_attachment)
        
        # Connect to SMTP server and send
        print(f"Connecting to SMTP server: {SMTP_SERVER}:{SMTP_PORT}")
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        print(f"Logging in as: {SENDER_EMAIL}")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print(f"Sending email to: {recipient}")
        server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
        server.quit()
        
        print(f"Email with PDF report sent to {recipient}")
        return True
        
    except Exception as e:
        print(f"Error sending email with PDF to {recipient}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

# Function to calculate acute:chronic workload ratio
def calculate_acute_chronic_ratio(df):
    """
    Calculate acute:chronic workload ratio for each athlete
    
    Acute = average of last 7 days
    Chronic = average of last 28 days (rolling window)
    Trend = comparison of latest value to previous 7-day average
    
    Returns a DataFrame with athlete information, A:C ratios, and trends
    """
    try:
        print("Calculating acute:chronic workload ratios...")
        
        # Skip if we don't have the necessary data
        if 'Last Name' not in df.columns or 'Position' not in df.columns:
            print("Missing required columns for A:C ratio calculation")
            return pd.DataFrame()
        
        # Create a copy to avoid modifying the original
        df_copy = df.copy()
        
        # Get date columns - filter out unnamed columns
        base_columns = ['Email', 'Last 4 digits', 'Last Name', 'First Name', 'Position', 'Summer Attendance', 'Name', 'Average Value']
        date_columns = [col for col in df_copy.columns 
                       if col not in base_columns and not col.lower().startswith('unnamed')]
        
        # Sort date columns by date
        date_columns.sort(key=lambda x: pd.to_datetime(x, errors='coerce'))
        
        # For each athlete, calculate acute (last 7 days) and chronic (last 28 days) workload
        result_data = []
        
        for _, row in df_copy.iterrows():
            if pd.isna(row['Last Name']) or pd.isna(row['Position']):
                continue
                
            last_name = row['Last Name']
            position = row['Position']
            
            # Scale values if needed
            values = []
            for col in date_columns:
                value = row[col]
                if pd.notna(value) and value != '':
                    try:
                        # Convert to number and scale if needed
                        if isinstance(value, str):
                            value = ''.join(c for c in value if c.isdigit() or c == '.')
                            value = float(value) if value else None
                        else:
                            value = float(value)
                        # Value scaling for outliers    
                        if value is not None:
                            # Scale values outside normal RPE range
                            if value > 1000:
                                value /= 1000
                            elif value > 100:
                                value /= 100
                            elif value > 10:
                                value /= 10
                                
                            # Cap at 10
                            value = min(value, 10.0)
                            values.append((col, value))
                    except:
                        continue
            
            if not values:
                continue
                
            # Sort values by date
            values.sort(key=lambda x: pd.to_datetime(x[0], errors='coerce'))
            
            # Get all RPE values
            total_values = [v[1] for v in values]
            
            # Calculate acute workload (last 7 days average)
            last_7_values = total_values[-4:] if len(total_values) >= 4 else total_values
            acute = sum(last_7_values) / len(last_7_values) if last_7_values else 0
            
            # Calculate chronic workload (last 28 days average)
            last_28_values = total_values[-8:] if len(total_values) >= 8 else total_values
            chronic = sum(last_28_values) / len(last_28_values) if last_28_values else 0
            
            # Calculate A:C ratio
            ac_ratio = acute / chronic if chronic > 0 else 0
            
            # Calculate trend (comparing most recent value to previous week average)
            # If only one data point exists, trend is "neutral"
            trend = "neutral"
            latest_value = total_values[-1] if total_values else 0
            
            if len(total_values) > 1:
                # Get the average of previous 7 days, excluding most recent
                prev_values = total_values[-8:-1] if len(total_values) >= 8 else total_values[:-1]
                prev_avg = sum(prev_values) / len(prev_values) if prev_values else 0
                
                # Determine trend (using 5% threshold for significance)
                if latest_value > prev_avg * 1.05:
                    trend = "increasing"
                elif latest_value < prev_avg * 0.95:
                    trend = "decreasing"
            
            result_data.append({
                'Last Name': last_name,
                'Position': position,
                'Acute': acute,
                'Chronic': chronic,
                'A:C Ratio': ac_ratio,
                'Latest RPE': total_values[-1] if total_values else 0,
                'Trend': trend
            })
        
        ac_df = pd.DataFrame(result_data)
        print(f"Calculated A:C ratios for {len(ac_df)} athletes")
        return ac_df
        
    except Exception as e:
        print(f"Error calculating A:C ratios: {str(e)}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()  # Return empty DataFrame on error

def create_pdf_report(df, df_position_avg, df_position_daily_avg):
    """Create a PDF report using ReportLab"""
    print("Inside create_pdf_report function")
    
    # Create a buffer to store the PDF
    buffer = io.BytesIO()
    
    try:
        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=0.5*inch,
            rightMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        # Container for PDF elements
        elements = []
        
        # Create styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            name='TrumanTitle',
            parent=styles['Heading1'],
            textColor=colors.Color(*TRUMAN_PURPLE),
            alignment=TA_CENTER,
            fontSize=18,
            spaceAfter=12
        )
        
        subtitle_style = ParagraphStyle(
            name='TrumanSubtitle',
            parent=styles['Heading2'],
            textColor=colors.Color(*TRUMAN_PURPLE),
            fontSize=14,
            spaceBefore=6,
            spaceAfter=6
        )
        
        section_style = ParagraphStyle(
            name='TrumanSection',
            parent=styles['Heading3'],
            textColor=colors.Color(*TRUMAN_PURPLE),
            fontSize=12,
            spaceBefore=10,
            spaceAfter=6
        )
        
        # Add title
        today = datetime.now().strftime('%B %d, %Y')
        elements.append(Paragraph(f"TRUMAN STATE BULLDOGS", title_style))
        elements.append(Paragraph(f"Summer Workout Performance Report", subtitle_style))
        elements.append(Paragraph(f"Generated on {today}", styles['Italic']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Apply scaling to data if needed
        if 'Average Value' in df.columns:
            df_scaled = df.copy()
            
            # Scale down values that are too high
            if df_scaled['Average Value'].max() > 10:
                # Values over 1000 get divided by 1000
                mask_1000 = df_scaled['Average Value'] > 1000
                df_scaled.loc[mask_1000, 'Average Value'] = df_scaled.loc[mask_1000, 'Average Value'] / 1000
                
                # Values over 100 get divided by 100
                mask_100 = (df_scaled['Average Value'] > 100) & (df_scaled['Average Value'] <= 1000)
                df_scaled.loc[mask_100, 'Average Value'] = df_scaled.loc[mask_100, 'Average Value'] / 100
                
                # Values over 10 get divided by 10
                mask_10 = (df_scaled['Average Value'] > 10) & (df_scaled['Average Value'] <= 100)
                df_scaled.loc[mask_10, 'Average Value'] = df_scaled.loc[mask_10, 'Average Value'] / 10
                
                # Cap at 10
                df_scaled.loc[df_scaled['Average Value'] > 10, 'Average Value'] = 10.0
        else:
            df_scaled = df
        
        if not df_position_avg.empty and 'Position' in df_position_avg.columns:
            df_position_avg_scaled = df_position_avg.copy()
            
            # Scale down position averages if needed
            if df_position_avg_scaled['Average Value'].max() > 10:
                # Values over 1000 get divided by 1000
                mask_1000 = df_position_avg_scaled['Average Value'] > 1000
                df_position_avg_scaled.loc[mask_1000, 'Average Value'] = df_position_avg_scaled.loc[mask_1000, 'Average Value'] / 1000
                
                # Values over 100 get divided by 100
                mask_100 = (df_position_avg_scaled['Average Value'] > 100) & (df_position_avg_scaled['Average Value'] <= 1000)
                df_position_avg_scaled.loc[mask_100, 'Average Value'] = df_position_avg_scaled.loc[mask_100, 'Average Value'] / 100
                
                # Values over 10 get divided by 10
                mask_10 = (df_position_avg_scaled['Average Value'] > 10) & (df_position_avg_scaled['Average Value'] <= 100)
                df_position_avg_scaled.loc[mask_10, 'Average Value'] = df_position_avg_scaled.loc[mask_10, 'Average Value'] / 10
                
                # Cap at 10
                df_position_avg_scaled.loc[df_position_avg_scaled['Average Value'] > 10, 'Average Value'] = 10.0
        else:
            df_position_avg_scaled = df_position_avg
        
        # Team Overview Section
        elements.append(Paragraph("TEAM OVERVIEW", section_style))
        
        # Calculate team stats
        team_avg = df_scaled['Average Value'].mean() if 'Average Value' in df_scaled.columns else 0
        
        # Filter workout date columns - exclude 'unnamed' columns and other non-date columns
        workout_dates = [col for col in df.columns 
                        if col not in ['Email', 'Last 4 digits', 'Last Name', 'First Name', 'Position', 'Summer Attendance', 'Name', 'Average Value'] 
                        and not col.lower().startswith('unnamed')]
        
        num_workouts = len(workout_dates)
        num_athletes = len(df)
        
        # Team stats table
        # Format the latest workout date if it exists
        latest_date = "N/A"
        if workout_dates:
            try:
                # Try to parse as a date for proper formatting
                date_obj = pd.to_datetime(workout_dates[-1], errors='coerce')
                if pd.notna(date_obj):
                    latest_date = date_obj.strftime('%B %d, %Y')
                else:
                    latest_date = workout_dates[-1]  # Use as is if parsing fails
            except:
                latest_date = workout_dates[-1]  # Use as is if any error occurs
        
        team_data = [
            ["Metric", "Value"],
            ["Team Average RPE", f"{team_avg:.2f}"],
            ["Number of Athletes", str(num_athletes)],
            ["Workout Sessions", str(num_workouts)],
            ["Latest Workout Date", latest_date]
        ]
        
        team_table = Table(team_data, colWidths=[2*inch, 2*inch])
        team_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.Color(*TRUMAN_PURPLE)),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(team_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Position Analysis Section
        elements.append(Paragraph("POSITION ANALYSIS", section_style))
        
        # Sort positions by average value
        position_data = []
        
        if not df_position_avg_scaled.empty and 'Position' in df_position_avg_scaled.columns:
            sorted_positions = df_position_avg_scaled.sort_values('Average Value', ascending=False)
            
            position_data = [["Position", "Average RPE", "Rank"]]
            for i, (_, row) in enumerate(sorted_positions.iterrows(), 1):
                position_data.append([
                    row['Position'],
                    f"{row['Average Value']:.2f}",
                    f"#{i}"
                ])
        
        if position_data:
            position_table = Table(position_data, colWidths=[2*inch, 1.5*inch, 1*inch])
            position_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(*TRUMAN_PURPLE)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                # Highlight top performer
                ('BACKGROUND', (0, 1), (-1, 1), colors.Color(0.8, 1, 0.8)),
                # Highlight bottom performer if we have more than 2 positions
                ('BACKGROUND', (0, len(position_data)-1), (-1, len(position_data)-1), 
                 colors.Color(1, 0.8, 0.8) if len(position_data) > 2 else colors.white)
            ]))
            
            elements.append(position_table)
        else:
            elements.append(Paragraph("No position data available", styles['Normal']))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # THE "HIGHEST RPE ATHLETES" SECTION HAS BEEN REMOVED FROM HERE
        
        # Athletes with High Acute:Chronic Ratio Section (formerly "Athletes Needing Attention")
        elements.append(Paragraph("ATHLETES WITH HIGH ACUTE:CHRONIC RATIO (INJURY RISK)", section_style))
        elements.append(Paragraph("Athletes with A:C ratio > 1.35 may be at increased risk of injury", styles['Italic']))
        elements.append(Paragraph("A:C ratio compares last 7 days of workload (acute) to last 28 days (chronic)", styles['Italic']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Calculate acute:chronic workload ratios
        ac_ratio_df = calculate_acute_chronic_ratio(df)
        
        attention_data = []
        if not ac_ratio_df.empty:
            # Get athletes with A:C ratio > 1.35 (CHANGED FROM 1.5)
            high_risk_athletes = ac_ratio_df[ac_ratio_df['A:C Ratio'] > 1.35].sort_values('A:C Ratio', ascending=False)
            
            if not high_risk_athletes.empty:
                attention_data = [["Athlete", "Position", "A:C Ratio", "Latest RPE", "Trend"]]
                for _, row in high_risk_athletes.iterrows():
                    # Add symbols for trend
                    trend_symbol = "→"  # neutral
                    if row['Trend'] == "increasing":
                        trend_symbol = "↑"  # increasing
                    elif row['Trend'] == "decreasing":
                        trend_symbol = "↓"  # decreasing
                        
                    attention_data.append([
                        row['Last Name'],
                        row['Position'],
                        f"{row['A:C Ratio']:.2f}",
                        f"{row['Latest RPE']:.1f}",
                        trend_symbol
                    ])
        
        if attention_data:
            attention_table = Table(attention_data, colWidths=[1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch, 0.7*inch])
            attention_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(*TRUMAN_PURPLE)),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                # Highlight very high risk (>2.0) with darker red
                *[('BACKGROUND', (0, i), (-1, i), colors.Color(1, 0.6, 0.6)) 
                  for i in range(1, len(attention_data)) 
                  if float(attention_data[i][2].replace(':', '.')) > 2.0]
            ]))
            
            elements.append(attention_table)
        else:
            elements.append(Paragraph("No athletes with elevated acute:chronic workload ratio identified", styles['Normal']))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Footer with Truman branding
        footer_text = "Truman State University Bulldogs - Go Bulldogs!"
        elements.append(Paragraph(footer_text, ParagraphStyle(
            name='Footer',
            parent=styles['Normal'],
            textColor=colors.Color(*TRUMAN_PURPLE),
            alignment=TA_CENTER,
            fontSize=10,
            spaceBefore=20
        )))
        
        # Build the PDF
        print("Building PDF document...")
        doc.build(elements)
        print("PDF document built successfully")
        buffer.seek(0)
        return buffer
    
    except Exception as e:
        print(f"Error creating PDF report: {str(e)}")
        import traceback
        traceback.print_exc()
        # Return an empty PDF with an error message
        try:
            # Create simple error PDF
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            elements.append(Paragraph("Error Creating Report", styles['Title']))
            elements.append(Paragraph(f"An error occurred: {str(e)}", styles['Normal']))
            doc.build(elements)
            buffer.seek(0)
            return buffer
        except:
            # If even that fails, return empty buffer
            buffer = io.BytesIO()
            buffer.write(b"Error creating PDF")
            buffer.seek(0)
            return buffer
