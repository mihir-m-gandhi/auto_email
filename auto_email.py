import smtplib
from email.mime.text import MIMEText
import csv
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Inputs
data_file_path = "data.csv" 
resume_path = "resume.pdf"
subject_path = "subject.txt"
message_path = "message.txt"
sender = "enter_your_email_id_here"
password = "enter_your_password_here"

# Get text from txt file
def get_text(file_path):
    with open(file_path, "r") as file:
        return file.read()

# Function to send email
def send_email(subject, body, sender, name, recipients, password):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = "your_name"
    msg['To'] = ', '.join(recipients)
    body = "Hi " + name + ", \n\n" + body
    msg.attach(MIMEText(body))
    part = MIMEBase('application', "octet-stream")
    with open(resume_path, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',
                    'attachment; filename={}'.format(Path(resume_path).name))
    msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent to", recipients[0])

body = get_text(message_path)
subject = get_text(subject_path)
# Read emails from csv file and send emails
with open(data_file_path, "r") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    next(reader)
    for row in reader:
        send_email(subject, body, sender, row[0], [row[2]], password)