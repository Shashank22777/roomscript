import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
from datetime import datetime

# Load the schedule from a CSV file (ensure the CSV matches the header format in your table)
CSV_FILE = "task_schedule.csv"  # Rename this based on your file's name
df = pd.read_csv(CSV_FILE)

# Email credentials and settings
SMTP_SERVER = "smtp.gmail.com"  # Change to your SMTP server
SMTP_PORT = 587
EMAIL = "shashankbandari777@gmail.com"  # Replace with your email
PASSWORD = "tlku brop vvhr avnn"  # Replace with your email password

def send_email(to_email, subject, body):
    try:
        # Set up the email
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Establish SMTP connection and send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {e}")

def send_daily_emails():
    # Get today's date in the format used in the CSV (e.g., "Sun 06 Apr")
    today = datetime.now().strftime("%a %d %b")
    if today not in df["Date"].values:
        print("No tasks scheduled for today.")
        return

    # Filter today's tasks
    tasks_today = df[df["Date"] == today]

    # Iterate through columns and send emails accordingly
    for task in tasks_today.columns[1:]:  # Skip the 'Date' column
        email = tasks_today[task].values[0]
        task_description = task
        subject = "Daily Task Reminder"
        body = f"Good morning!\n\nHere is your task for today:\n\n{task_description}\n\nHave a productive day!"
        send_email(email, subject, body)

# Schedule this function to run daily at 7 AM IST
send_daily_emails()