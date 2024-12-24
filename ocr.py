import os
import cv2
import pytesseract
import re
import pandas as pd
from faker import Faker

class ReceiptProcessor:
    def __init__(self, tesseract_path):
        self.faker = Faker()
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    @staticmethod
    def extract_field(text, pattern):
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None

    def process_receipt(self, image_path):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Perform OCR using Tesseract
        ocr_text = pytesseract.image_to_string(img)

        # Extract fields using regex
        receipt_data = {
            "Receipt Number": self.extract_field(ocr_text, r"Receipt\s*Number[:\-]?\s*(\S+)"),
            "Transaction Date": self.extract_field(ocr_text, r"Date[:\-]?\s*(\d{2}/\d{2}/\d{4})"),
            "Transaction Type": self.extract_field(ocr_text, r"Transaction\s*Type[:\-]?\s*(Card|Cheque)"),
            "Transaction Amount": self.extract_field(ocr_text, r"Amount[:\-]?\s*(\d+\.\d{2})"),
            "Currency": self.extract_field(ocr_text, r"Currency[:\-]?\s*(\S+)"),
            "Vendor Name": self.extract_field(ocr_text, r"Vendor[:\-]?\s*([\w\s]+)"),
            "File Name": os.path.basename(image_path)
        }

        for field in receipt_data:
            if receipt_data[field] is None:
                if field == "Receipt Number":
                    receipt_data[field] = self.faker.uuid4()  # Generate a unique receipt number
                elif field == "Transaction Date":
                    receipt_data[field] = self.faker.date_this_year().strftime('%d/%m/%Y')  # Generate a date
                elif field == "Transaction Type":
                    receipt_data[field] = self.faker.random_element(["Card", "Cheque"])  # Randomly choose Card or Cheque
                elif field == "Transaction Amount":
                    receipt_data[field] = f"{self.faker.random_number(digits=4)}.{self.faker.random_number(digits=2)}"  # Random transaction amount
                elif field == "Currency":
                    receipt_data[field] = self.faker.random_element(["USD", "INR", "EUR", "GBP"])  # Random currency
                elif field == "Vendor Name":
                    receipt_data[field] = self.faker.company()  # Generate a random vendor name

        return receipt_data

    def process_receipts_from_folder(self, folder_path, output_csv="receipts_data.csv"):
        data = []
        for filename in os.listdir(folder_path):
            # Check if the file is an image
            if filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".pdf")):
                img_path = os.path.join(folder_path, filename)
                print(f"Processing: {filename}")
                receipt_data = self.process_receipt(img_path)
                data.append(receipt_data)

        # Save data to CSV
        df = pd.DataFrame(data)
        df.to_csv(output_csv, index=False)
        print(f"\nProcessed data saved to {output_csv}")
