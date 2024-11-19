import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
from pathlib import Path
import logging
import json


class ReceiptOCR:
    def __init__(self, tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        """
        Initialize the OCR processor
        Args:
            tesseract_path: Path to tesseract executable
        """
        # Configure tesseract path
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def preprocess_image(self, image):
        """
        Preprocess the image for better OCR accuracy
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply thresholding to preprocess the image
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Apply dilation to connect text components
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        gray = cv2.dilate(gray, kernel, iterations=1)

        # Apply erosion to remove noise
        gray = cv2.erode(gray, kernel, iterations=1)

        # Apply median blur to remove noise while preserving edges
        gray = cv2.medianBlur(gray, 3)

        return gray

    def deskew_image(self, image):
        """
        Deskew the image if it's rotated
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Calculate skew angle
            coords = np.column_stack(np.where(gray > 0))
            angle = cv2.minAreaRect(coords)[-1]

            if angle < -45:
                angle = 90 + angle

            # Rotate the image
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

            return rotated
        except Exception as e:
            self.logger.error(f"Error in deskewing image: {str(e)}")
            return image

    def extract_text(self, image_path):
        """
        Extract text from image using OCR
        """
        try:
            # Read image
            image = cv2.imread(str(image_path))
            if image is None:
                raise ValueError(f"Could not read image at {image_path}")

            # Deskew image
            image = self.deskew_image(image)

            # Preprocess image
            processed_image = self.preprocess_image(image)

            # Perform OCR
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(processed_image, config=custom_config)

            return text.strip()

        except Exception as e:
            self.logger.error(f"Error processing image {image_path}: {str(e)}")
            return None

    def extract_receipt_data(self, text):
        """
        Extract structured data from OCR text
        """
        data = {
            'receipt_number': None,
            'date': None,
            'amount': None,
            'vendor': None,
            'items': []
        }

        try:
            # Extract receipt number (assuming format: Receipt #XXXXX)
            receipt_match = re.search(r'Receipt\s*#?\s*([A-Z0-9-]+)', text, re.IGNORECASE)
            if receipt_match:
                data['receipt_number'] = receipt_match.group(1)

            # Extract date (common formats)
            date_match = re.search(r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}', text)
            if date_match:
                data['date'] = date_match.group(0)

            # Extract amount (assuming format: $XX.XX or XX.XX)
            amount_match = re.search(r'\$?\s*(\d+\.\d{2})', text)
            if amount_match:
                data['amount'] = float(amount_match.group(1))

            # Extract vendor name (assuming it's at the top of receipt)
            lines = text.split('\n')
            if lines:
                data['vendor'] = lines[0].strip()

            # Extract items (assuming format: Item $XX.XX)
            items = re.findall(r'(.*?)\$?\s*(\d+\.\d{2})', text)
            for item in items:
                if len(item[0].strip()) > 0:
                    data['items'].append({
                        'description': item[0].strip(),
                        'amount': float(item[1])
                    })

            return data

        except Exception as e:
            self.logger.error(f"Error extracting structured data: {str(e)}")
            return data

    def process_receipt_batch(self, input_directory, output_directory):
        """
        Process a batch of receipt images
        """
        input_path = Path(input_directory)
        output_path = Path(output_directory)
        output_path.mkdir(parents=True, exist_ok=True)

        results = []
        for image_file in input_path.glob('*.{jpg,jpeg,png,tiff}'):
            try:
                # Extract text from image
                text = self.extract_text(image_file)
                if text:
                    # Extract structured data
                    data = self.extract_receipt_data(text)
                    data['source_image'] = str(image_file)

                    # Save extracted data
                    output_file = output_path / f"{image_file.stem}.json"
                    with open(output_file, 'w') as f:
                        json.dump(data, f, indent=4)

                    results.append({
                        'filename': image_file.name,
                        'status': 'success',
                        'data': data
                    })
                    self.logger.info(f"Successfully processed {image_file.name}")
                else:
                    results.append({
                        'filename': image_file.name,
                        'status': 'failed',
                        'error': 'No text extracted'
                    })
                    self.logger.error(f"Failed to extract text from {image_file.name}")

            except Exception as e:
                results.append({
                    'filename': image_file.name,
                    'status': 'failed',
                    'error': str(e)
                })
                self.logger.error(f"Error processing {image_file.name}: {str(e)}")

        return results
