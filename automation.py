import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText




my_email="chiragtrytest@gmail.com"
password="krucsivapyxuzhvo"

# ata = pd.read_csv(r"C:\Users\Chirag S\Desktop\finance recepting using RPA\datasets\card_reciepts.csv")

emails = data['vendor_email']

for email in emails:

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:


        connection.starttls()
        connection.login(user=my_email, password=password)

        msg = MIMEMultipart()
        msg['From'] = my_email
        msg['To'] = email
        msg['Subject'] = "Finance Reciepts"

        msg.attach(MIMEText(message, 'plain'))
        connection.send_message(msg)