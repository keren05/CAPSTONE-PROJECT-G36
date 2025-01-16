# AI-Augmented RPA for Smart Receipting

## Overview
AI-Augmented Robotic Process Automation (RPA) for Smart Receipting is a robust system that automates the processing, validation, and analysis of receipts. This project integrates UiPath Studio for RPA workflows and Gradio for building an interactive web-based interface. By combining Optical Character Recognition (OCR), Natural Language Processing (NLP), and Anomaly Detection, the system streamlines tedious tasks while providing a user-friendly experience.

---

## Features
- **OCR Integration**: Extracts text from receipt images for further processing.
- **NLP-Powered Data Extraction**: Identifies and extracts key information like vendor names, dates, and amounts.
- **Fraud Detection**: Uses anomaly detection to flag potential fraudulent receipts.
- **Gradio Web App**: An interactive interface for uploading receipts and viewing processed data.
- **UiPath Automation**: Executes workflows for data extraction, fraud analysis, and database updates.
- **Chatbot Support**: Responds to user queries about receipt data and anomalies.

---

## Workflow
1. **Receipt Upload**: 
   - Users upload scanned receipts via the Gradio-based web app.
2. **OCR Processing**:
   - Text is extracted from receipt images using OCR tools like Tesseract.
3. **Data Structuring**:
   - UiPath Studio workflows preprocess the extracted text to remove noise and organize it.
4. **Information Extraction**:
   - NLP techniques extract essential details, including vendor names, transaction dates, and amounts.
5. **Anomaly Detection**:
   - Fraud detection models analyze patterns to identify duplicates or unusual entries.
6. **User Interaction**:
   - Gradio app displays extracted data and anomaly flags. Chatbot handles user queries.
7. **Database Storage**:
   - Processed data is stored in a structured format for future use.

---

## Technologies Used
- **Frontend**: Gradio (Python-based UI framework).
- **Backend**: Python.
- **RPA Tools**: UiPath Studio for workflow automation.
- **OCR**: Tesseract.
- **NLP**: spaCy, NLTK, Hugging Face Transformers.
- **Anomaly Detection**: scikit-learn, PyOD.
- **Database**: OS for storing receipt data.

---

## Table of Components for Web Application

| **Component**          | **Purpose**                                             | **Technology/Tool**       |
|------------------------|---------------------------------------------------------|---------------------------|
| User Interface         | Interactive receipt upload and data display             | Gradio                    |
| Backend Logic          | Handles data processing and integration                 | Python                    |
| OCR                    | Extracts text from uploaded receipt images              | Tesseract                 |
| NLP Engine             | Processes and extracts key information                  | spaCy, NLTK               |
| Anomaly Detection      | Identifies fraud and inconsistencies                    | scikit-learn, PyOD        |
| Automation Framework   | Executes workflows for text extraction and processing   | UiPath Studio             |
| Database               | Stores processed receipt data                           | OS                        |
| Chatbot                | Handles user queries interactively                      | OpenAI                    |

---

## Installation

### Prerequisites
- Python 3.8+
- UiPath Studio
- Tesseract OCR
- Gradio

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/keren05/CAPSTONE-PROJECT-G36.git
   cd CAPSTONE-PROJECT-G36
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure UiPath workflows:
   - Open UiPath Studio and load the provided `.xaml` files.
   - Ensure the necessary dependencies are installed in UiPath.
4. Start the Gradio web app:
   ```bash
   python app.py
   ```
5. Access the app at `http://localhost:7860`.

---

## Usage
1. **Upload a Receipt**: Use the Gradio interface to upload scanned receipt images.
2. **View Extracted Details**: The app displays key receipt data and anomaly flags.
3. **Fraud Analysis**: Review anomalies detected by the system in the Gradio dashboard.
4. **Chatbot Interaction**: Query receipt details or fraud alerts via the chatbot.

---

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact
For queries or feedback, please contact [keren.20211CSD0132@presidencyuniversity.in].
