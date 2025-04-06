import pandas as pd
import datetime
import os
import smtplib
from email.mime.text import MIMEText

# 1. Fetch Email Credentials from GitHub Secrets or Environment Variables
EMAIL = os.environ.get("EMAIL")  # Sender's email fetched securely
PASSWORD = os.environ.get("PASSWORD")  # App password fetched securely

# 2. File Path to the CSV Schedule (Ensure it's in the same repo with this script)
CSV_FILE = "task_schedule.csv"

# 3. Load the task schedule from the CSV
try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    print("Error: The CSV file was not found.")
    exit(1)

# 4. Get Today's Date in the format used in the CSV
today = datetime.datetime.now().strftime("%a %d %b")

# 5. Filter for Today's Tasks
today_tasks = df[df["Date"] == today]

# 6. Check if there are tasks for today
if today_tasks.empty:
    print("No tasks scheduled for today!")
else:
    # Go through each task column and send tasks to the assigned person
    for column in today_tasks.columns[1:]:  # Skip the "Date" column
        task_description = column
        recipient_info = today_tasks[column].values[0]  # Fetch recipient from the column

        # Parse recipient's name and email from the cell (e.g., "Shashank (Shashankbandari777@gmail.com)")
        try:
            recipient_name, recipient_email = recipient_info.split("(")
            recipient_email = recipient_email.strip(")")  # Clean up the email
        except ValueError:
            print(f"Error parsing recipient info: {recipient_info}")
            continue

        # Prepare the email content
        subject = f"Task Reminder: {task_description}"
        body = f"""
        Hello {recipient_name.strip()},\n\n
        Here is your assigned task for today ({today}):\n
        Task: {task_description}\n\n
        Please ensure it's completed today.\n\n
        Thank you!
        """

        # Set up the email
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL
        msg["To"] = recipient_email

        # 7. Send Email via Gmail SMTP
        try:
            print(f"Sending task reminder to {recipient_name.strip()} ({recipient_email})...")
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Secure the connection
                server.login(EMAIL, PASSWORD)  # Log in to the SMTP server
                server.sendmail(EMAIL, recipient_email, msg.as_string())
                print(f"Task reminder sent successfully to {recipient_name.strip()}!")
        except Exception as e:
            print(f"Failed to send email to {recipient_email}. Error: {e}")
