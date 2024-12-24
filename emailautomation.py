import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import pandas as pd

class EmailSender:
    def __init__(self, smtp_server, smtp_port, email_address, email_password):
        """
        Initialize the EmailSender with SMTP server details and email credentials.

        Args:
            smtp_server (str): SMTP server address.
            smtp_port (int): SMTP server port.
            email_address (str): Sender's email address.
            email_password (str): Sender's email password.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_address = email_address
        self.email_password = email_password

    def send_email_with_templates(self, csv_file_path, template_folder):
        """
        Send emails with respective templates to the recipients listed in the CSV file.

        Args:
            csv_file_path (str): Path to the CSV file containing recipient email and template mapping.
            template_folder (str): Path to the folder containing email templates.

        Returns:
            str: Success or error message.
        """
        try:
            # Read the CSV file
            data = pd.read_csv(csv_file_path)

            # Verify required columns
            if 'vendor_email' not in data.columns or 'template_name' not in data.columns:
                return "CSV file must contain 'vendor_email' and 'template_name' columns."

            # Connect to the SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_address, self.email_password)

            # Send emails
            for _, row in data.iterrows():
                recipient_email = row['vendor_email']
                template_file = row['template_name']

                # Construct full template path
                template_path = os.path.join(template_folder, template_file)

                if not os.path.exists(template_path):
                    print(f"Template file not found: {template_path}")
                    continue

                # Read the template content
                with open(template_path, 'r') as file:
                    email_body = file.read()

                # Create the email
                msg = MIMEMultipart()
                msg['From'] = self.email_address
                msg['To'] = recipient_email
                msg['Subject'] = "Automated Email with Template"

                # Attach email body
                msg.attach(MIMEText(email_body, 'plain'))

                # Send the email
                server.send_message(msg)
                print(f"Email sent successfully to {recipient_email}")

            # Disconnect from the server
            server.quit()

            return "All emails processed successfully."
        except Exception as e:
            return f"An error occurred: {str(e)}"

# Example usage:
# email_sender = EmailSender(
#     smtp_server="smtp.gmail.com",
#     smtp_port=587,
#     email_address="chiragtrytest@gmail.com",
#     email_password="krucsivapyxuzhvo"
# )
# csv_file_path = r"C:\Users\keren\OneDrive\Downloads\capstone\recipients.csv"
# template_folder = r"C:\Users\keren\OneDrive\Downloads\capstone\templates"
# result = email_sender.send_email_with_templates(csv_file_path, template_folder)
# print(result)
