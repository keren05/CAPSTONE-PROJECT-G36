import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import json
import logging


class ReceiptEmailAutomation:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        """Initialize with email server settings."""
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password

        # Set up logging
        logging.basicConfig(
            filename='email_automation.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def parse_receipt(self, receipt_data):
        """Parse receipt data into required fields."""
        try:
            return {
                'transaction_id': receipt_data.get('transaction_id'),
                'amount': receipt_data.get('amount'),
                'date': receipt_data.get('date'),
                'items': receipt_data.get('items', []),
                'customer_email': receipt_data.get('customer_email')
            }
        except Exception as e:
            logging.error(f"Error parsing receipt: {str(e)}")
            raise

    def create_email_content(self, receipt_data):
        """Create email content from receipt data."""
        parsed_data = self.parse_receipt(receipt_data)

        html_content = f"""
        <html>
            <body>
                <h2>Receipt for Transaction #{parsed_data['transaction_id']}</h2>
                <p>Date: {parsed_data['date']}</p>
                <h3>Items:</h3>
                <ul>
        """

        for item in parsed_data['items']:
            html_content += f"<li>{item['name']} - ${item['price']:.2f}</li>"

        html_content += f"""
                </ul>
                <p><strong>Total Amount: ${parsed_data['amount']:.2f}</strong></p>
                <p>Thank you for your business!</p>
            </body>
        </html>
        """

        return html_content

    def send_email(self, to_email, subject, html_content):
        """Send email with receipt information."""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = to_email

            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)

            logging.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logging.error(f"Error sending email: {str(e)}")
            raise

    def process_receipt(self, receipt_data):
        """Main method to process receipt and send email."""
        try:
            parsed_data = self.parse_receipt(receipt_data)
            subject = f"Receipt for Transaction #{parsed_data['transaction_id']}"
            html_content = self.create_email_content(receipt_data)

            self.send_email(
                parsed_data['customer_email'],
                subject,
                html_content
            )

            return True

        except Exception as e:
            logging.error(f"Error processing receipt: {str(e)}")
            return False


# Example usage
if __name__ == "__main__":
    # Email server settings
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SENDER_EMAIL = "your-email@gmail.com"
    SENDER_PASSWORD = "your-app-specific-password"

    # Sample receipt data
    sample_receipt = {
        "transaction_id": "12345",
        "amount": 99.99,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": [
            {"name": "Product 1", "price": 49.99},
            {"name": "Product 2", "price": 50.00}
        ],
        "customer_email": "customer@example.com"
    }

    # Initialize automation
    automation = ReceiptEmailAutomation(
        SMTP_SERVER,
        SMTP_PORT,
        SENDER_EMAIL,
        SENDER_PASSWORD
    )

    # Process receipt
    automation.process_receipt(sample_receipt)