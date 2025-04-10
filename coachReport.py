from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from emailNotif import send_email
import io
import json

# Truman State University Colors
TRUMAN_PURPLE = (79/255, 45/255, 127/255)  # RGB for PDF
TRUMAN_LIGHT_BLUE = (0/255, 178/255, 227/255)  # RGB for PDF
TRUMAN_WHITE = (1, 1, 1)

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
    # Default coach emails - replace with actual coach emails
    default_coaches = [
        "mc6383@truman.edu"
    ]
    
    # Use provided coaches or default list
    coach_emails = selected_coaches if selected_coaches else default_coaches
    
    # Create the PDF report
    buffer = create_pdf_report(df, df_position_avg, df_position_daily_avg)
    
    # Create performance summary graphs
    position_graph_buffer = create_position_graph(df_position_avg)
    trend_graph_buffer = create_trend_graph(df_position_daily_avg)
    
    # Track success/failure
    success_count = 0
    fail_count = 0
    
    # Generate email content
    today = datetime.now().strftime('%B %d, %Y')
    team_avg = df['Average Value'].mean() if 'Average Value' in df.columns else 0
    
    email_subject = f"Truman Bulldogs - Performance Report {today}"
    email_message = f"""
Hello Coach,

Attached is the latest performance report for the Truman State Bulldogs team as of {today}.

QUICK SUMMARY:
- Team Average RPE: {team_avg:.2f}
- {len(df)} athletes tracked
- Data collected from {len([col for col in df.columns if col not in ['Email', 'Last 4 digits', 'Last Name', 'First Name', 'Position', 'Summer Attendance', 'Name', 'Average Value']])} workout sessions

The full report is attached as a PDF with detailed breakdowns by position and individual athletes.

Go Bulldogs!
Truman State Coaching Staff
"""
    
    # Send emails to coaches
    for email in coach_emails:
        try:
            # Use the custom send_email function with PDF attachment
            if send_email_with_pdf(
                recipient=email,
                subject=email_subject,
                message=email_message,
                pdf_buffer=buffer,
                position_graph_buffer=position_graph_buffer,
                trend_graph_buffer=trend_graph_buffer
            ):
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"Error sending coach report to {email}: {e}")
            fail_count += 1
    
    return {
        "success_count": success_count,
        "fail_count": fail_count,
        "message": f"Coach reports sent: {success_count} successful, {fail_count} failed."
    }

def send_email_with_pdf(recipient, subject, message, pdf_buffer, position_graph_buffer=None, trend_graph_buffer=None):
    """Send email with PDF report and graphs attached"""
    
    try:
        with open("credentials.json", "r") as file:
            creds_data = json.load(file)
        
        # Email Setup using credentials.json
        try:
            SMTP_SERVER = creds_data["email_settings"]["smtp_server"]
            SMTP_PORT = creds_data["email_settings"]["smtp_port"]
            SENDER_EMAIL = creds_data["email_settings"]["sender_email"]
            SENDER_PASSWORD = creds_data["email_settings"]["sender_password"]
        except KeyError as e:
            print(f"Missing key in email settings: {e}")
            return False

        # Safety check
        if not SENDER_EMAIL or not SENDER_PASSWORD:
            print("Email or password is not set in credentials.json. Skipping email.")
            return False

        try:
            # Create the email
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.application import MIMEApplication
            import smtplib
            
            msg = MIMEMultipart()
            msg["From"] = SENDER_EMAIL
            msg["To"] = recipient
            msg["Subject"] = subject

            # Attach the message
            msg.attach(MIMEText(message, "plain"))
            
            # Attach the PDF
            pdf_attachment = MIMEApplication(pdf_buffer.read(), _subtype="pdf")
            pdf_buffer.seek(0)  # Reset buffer position
            pdf_attachment.add_header('Content-Disposition', 'attachment', filename="TrumanBulldogs_Report.pdf")
            msg.attach(pdf_attachment)
            
            # Connect to server and send
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
            server.quit()
            
            print(f"Email with PDF report sent to {recipient}")
            return True
            
        except Exception as e:
            print(f"Error sending email with PDF to {recipient}: {e}")
            return False
            
    except Exception as e:
        print(f"Error in send_email_with_pdf: {e}")
        return False

def create_pdf_report(df, df_position_avg, df_position_daily_avg):
    """Create a PDF report using ReportLab"""
    
    # Create a buffer to store the PDF
    buffer = io.BytesIO()
    
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
    
    # Team Overview Section
    elements.append(Paragraph("TEAM OVERVIEW", section_style))
    
    # Calculate team stats
    team_avg = df['Average Value'].mean() if 'Average Value' in df.columns else 0
    workout_dates = [col for col in df.columns if col not in ['Email', 'Last 4 digits', 'Last Name', 'First Name', 'Position', 'Summer Attendance', 'Name', 'Average Value']]
    num_workouts = len(workout_dates)
    num_athletes = len(df)
    
    # Team stats table
    team_data = [
        ["Metric", "Value"],
        ["Team Average RPE", f"{team_avg:.2f}"],
        ["Number of Athletes", str(num_athletes)],
        ["Workout Sessions", str(num_workouts)],
        ["Latest Workout Date", workout_dates[-1] if workout_dates else "N/A"]
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
    
    if not df_position_avg.empty and 'Position' in df_position_avg.columns:
        sorted_positions = df_position_avg.sort_values('Average Value', ascending=False)
        
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
    
    # Top Athletes Section
    elements.append(Paragraph("TOP PERFORMING ATHLETES", section_style))
    
    athlete_data = []
    if 'Name' in df.columns and 'Average Value' in df.columns and 'Position' in df.columns:
        # Get top 5 athletes
        top_athletes = df.sort_values('Average Value', ascending=False).head(5)
        
        athlete_data = [["Athlete", "Position", "Average RPE"]]
        for _, row in top_athletes.iterrows():
            name = row['Name'] if pd.notna(row['Name']) else row['Last Name'] if 'Last Name' in row else "Unknown"
            athlete_data.append([
                name,
                row['Position'],
                f"{row['Average Value']:.2f}"
            ])
    
    if athlete_data:
        athlete_table = Table(athlete_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        athlete_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(*TRUMAN_PURPLE)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(athlete_table)
    else:
        elements.append(Paragraph("No athlete data available", styles['Normal']))
    
    elements.append(Spacer(1, 0.2*inch))
    
    # Athletes Needing Attention Section
    elements.append(Paragraph("ATHLETES NEEDING ATTENTION", section_style))
    
    attention_data = []
    if 'Name' in df.columns and 'Average Value' in df.columns and 'Position' in df.columns:
        # Get bottom 5 athletes with non-zero values
        non_zero_df = df[df['Average Value'] > 0]
        bottom_athletes = non_zero_df.sort_values('Average Value').head(5)
        
        attention_data = [["Athlete", "Position", "Average RPE"]]
        for _, row in bottom_athletes.iterrows():
            name = row['Name'] if pd.notna(row['Name']) else row['Last Name'] if 'Last Name' in row else "Unknown"
            attention_data.append([
                name,
                row['Position'],
                f"{row['Average Value']:.2f}"
            ])
    
    if attention_data:
        attention_table = Table(attention_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        attention_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.Color(*TRUMAN_PURPLE)),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(attention_table)
    else:
        elements.append(Paragraph("No athletes requiring attention found", styles['Normal']))
    
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
    doc.build(elements)
    buffer.seek(0)
    return buffer

def create_position_graph(df_position_avg):
    """Create a graph showing position averages"""
    # Create a buffer to store the image
    buffer = io.BytesIO()
    
    # Create the graph
    if not df_position_avg.empty:
        fig = px.bar(
            df_position_avg.sort_values('Average Value', ascending=False), 
            x='Position', 
            y='Average Value',
            title="Average RPE by Position",
            color_discrete_sequence=['#4F2D7F', '#00B2E3']  # Truman colors
        )
        
        fig.update_layout(
            xaxis_title="Position",
            yaxis_title="Average RPE Value",
            plot_bgcolor='white',
            font=dict(family="Arial", color="#4F2D7F")
        )
        
        # Save to buffer
        fig.write_image(buffer, format="png")
        buffer.seek(0)
    
    return buffer

def create_trend_graph(df_position_daily_avg):
    """Create a trend graph showing position performance over time"""
    # Create a buffer to store the image
    buffer = io.BytesIO()
    
    # Create the graph
    if not df_position_daily_avg.empty and 'Date' in df_position_daily_avg.columns:
        fig = px.line(
            df_position_daily_avg, 
            x='Date', 
            y='Value', 
            color='Position',
            title="Position Performance Trends",
            markers=True,
            color_discrete_sequence=['#4F2D7F', '#00B2E3', '#8F73B3', '#9E1B34']  # Truman colors + extras
        )
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Average RPE Value",
            plot_bgcolor='white',
            font=dict(family="Arial", color="#4F2D7F")
        )
        
        # Save to buffer
        fig.write_image(buffer, format="png")
        buffer.seek(0)
    
    return buffer