import os
import cv2
import pytesseract
import re
import pandas as pd
from faker import Faker
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "kerencsd05@gmail.com"
EMAIL_PASSWORD = "rensaysbye5"

# Initialize Faker and configure Tesseract
faker = Faker()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_field(text, pattern):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None


def process_receipt(image_path):
    """Process a single receipt image and extract standardized data."""
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    ocr_text = pytesseract.image_to_string(img)

    receipt_data = {
        "receipt_number": extract_field(ocr_text, r"Receipt\s*Number[:\-]?\s*(\S+)"),
        "date": extract_field(ocr_text, r"Date[:\-]?\s*(\d{2}/\d{2}/\d{4})"),
        "transaction_type": extract_field(ocr_text, r"Transaction\s*Type[:\-]?\s*(Card|Cheque)"),
        "amount": extract_field(ocr_text, r"Amount[:\-]?\s*(\d+\.\d{2})"),
        "vendor_name": extract_field(ocr_text, r"Vendor[:\-]?\s*([\w\s]+)"),
        "file_name": os.path.basename(image_path),
        "client_name": faker.name(),  # Added for email template compatibility
        "is_exception": faker.boolean(),  # Added for email template compatibility
        "is_paper": True  # Added for email template compatibility
    }

    # Fill missing data with synthetic data
    if receipt_data["receipt_number"] is None:
        receipt_data["receipt_number"] = faker.uuid4()
    if receipt_data["date"] is None:
        receipt_data["date"] = faker.date_this_year().strftime('%d/%m/%Y')
    if receipt_data["transaction_type"] is None:
        receipt_data["transaction_type"] = faker.random_element(["Card", "Cheque"])
    if receipt_data["amount"] is None:
        receipt_data["amount"] = f"{faker.random_number(digits=4)}.{faker.random_number(digits=2)}"
    if receipt_data["vendor_name"] is None:
        receipt_data["vendor_name"] = faker.company()

    return receipt_data


def process_receipts_from_folder(folder_path, output_csv="receipts_data.csv"):
    """Process all receipts in a folder and save to CSV."""
    data = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.pdf')):
            img_path = os.path.join(folder_path, filename)
            print(f"Processing: {filename}")
            receipt_data = process_receipt(img_path)
            data.append(receipt_data)

    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"\nProcessed data saved to {output_csv}")
    return df


def create_email_template(receipt_data):
    """Create a standardized email template for a receipt."""
    email_template = f"""Subject: Receipt Details - {receipt_data['receipt_number']}

Dear {receipt_data['vendor_name']},

Please find the details of your receipt below:

Receipt Number: {receipt_data['receipt_number']}
Transaction Type: {receipt_data['transaction_type']}
Client Name: {receipt_data['client_name']}
Amount: {receipt_data['amount']}
Date: {receipt_data['date']}
Exception Status: {"Yes" if receipt_data['is_exception'] else "No"}
Paper Receipt: {"Yes" if receipt_data['is_paper'] else "No"}

Thank you for your cooperation.

Best regards,
Presidency University"""

    return email_template


def create_email_templates(data_file_path, output_folder):
    """Generate email templates for all receipts in the dataset."""
    data = pd.read_csv(data_file_path)

    # Create sample template from first row
    if not data.empty:
        first_row = data.iloc[0]
        sample_template = create_email_template(first_row)
        sample_path = f"{output_folder}/sample_template.txt"
        with open(sample_path, 'w') as file:
            file.write(sample_template)
        print(f"Sample template generated at: {sample_path}")

    # Generate templates for all receipts
    for _, row in data.iterrows():
        email_template = create_email_template(row)
        file_name = f"email_template_{row['receipt_number']}.txt"
        output_path = f"{output_folder}/{file_name}"
        with open(output_path, 'w') as file:
            file.write(email_template)

    print(f"Email templates generated in: {output_folder}")
    return sample_path


def send_email(template_file, recipient_email):
    """Send email with template."""
    try:
        with open(template_file, 'rb') as f:
            template_content = f.read()

        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_email
        msg['Subject'] = "Receipt Details"

        msg.attach(MIMEText(template_content.decode('utf-8'), 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"Email sent successfully to {recipient_email}.")
    except Exception as e:
        print(f"An error occurred while sending email: {str(e)}")


if __name__ == "__main__":
    # Process receipts
    folder_path = r"C:\Users\keren\OneDrive\Downloads\capstone\receipts images"
    data_file_path = "uploaded_files/receipts_data.csv"
    output_folder = r"C:\Users\keren\OneDrive\Desktop\CAPSTONE FILES"

    # Process all receipts and create CSV
    df = process_receipts_from_folder(folder_path, data_file_path)

    # Generate email templates
    create_email_templates(data_file_path, output_folder)

    # Send emails to recipients (example usage)
    for _, row in df.iterrows():
        recipient_email = f"{row['vendor_name'].lower().replace(' ', '')}@example.com"  # Replace with actual logic
        email_file = f"{output_folder}/email_template_{row['receipt_number']}.txt"
        send_email(email_file, recipient_email)
