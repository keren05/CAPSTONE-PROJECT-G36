import pandas as pd

class EmailTemplateGenerator:
    def __init__(self, data_file_path, output_folder):
        """
        Initialize the EmailTemplateGenerator with file paths.

        Args:
            data_file_path (str): Path to the input dataset.
            output_folder (str): Path to the folder where email templates will be saved.
        """
        self.data_file_path = data_file_path
        self.output_folder = output_folder

    def create_email_templates(self):
        """
        Generate email templates from the dataset and save them to the output folder.

        Returns:
            str: Path to the sample template.
        """
        # Read the CSV file
        data = pd.read_csv(self.data_file_path)
        data = data.head(100)

        # Verify required columns
        required_columns = ['receipt_number', 'transaction_type', 'client_name', 'vendor_name',
                            'amount', 'date', 'is_exception', 'is_paper']
        for col in required_columns:
            if col not in data.columns:
                raise ValueError(f"The dataset is missing the required column: {col}")

        # Add a new column for template names
        data['template_name'] = ''

        # Create sample template from first row
        if not data.empty:
            first_row = data.iloc[0]
            sample_template = f"""Subject: Receipt Details - {first_row['receipt_number']}

Dear {first_row['vendor_name']},

Please find the details of your receipt below:

Receipt Number: {first_row['receipt_number']}
Transaction Type: {first_row['transaction_type']}
Client Name: {first_row['client_name']}
Amount: {first_row['amount']}
Date: {first_row['date']}
Exception Status: {"Yes" if first_row['is_exception'] else "No"}
Paper Receipt: {"Yes" if first_row['is_paper'] else "No"}

Thank you for your cooperation.

Best regards,
[Your Company Name]"""

            # Save sample template
            sample_path = f"{self.output_folder}/sample_template.txt"
            with open(sample_path, 'w') as file:
                file.write(sample_template)
            print(f"Sample template generated at: {sample_path}")

        # Process each row for regular templates
        for index, row in data.iterrows():
            email_template = f"""Subject: Receipt Details - {row['receipt_number']}

Dear {row['vendor_name']},

Please find the details of your receipt below:

Receipt Number: {row['receipt_number']}
Transaction Type: {row['transaction_type']}
Client Name: {row['client_name']}
Amount: {row['amount']}
Date: {row['date']}
Exception Status: {"Yes" if row['is_exception'] else "No"}
Paper Receipt: {"Yes" if row['is_paper'] else "No"}

Thank you for your cooperation.

Best regards,
[Presidency University]"""

            # Save to file
            file_name = f"email_template_{row['receipt_number']}.txt"
            output_path = f"{self.output_folder}/{file_name}"
            with open(output_path, 'w') as file:
                file.write(email_template)

            # Update the DataFrame with the template name
            data.at[index, 'template_name'] = file_name

        # Save the updated DataFrame to the same CSV file or a new one
        updated_csv_path = self.data_file_path
        data.to_csv(updated_csv_path, index=False)
        print(f"Updated CSV file with template names saved at: {updated_csv_path}")

        print(f"Email templates successfully generated in: {self.output_folder}")

        return sample_path  # Return the path of the sample template

# Example usage:
# data_file_path = r"C:\Users\keren\OneDrive\Downloads\capstone\synthetic_receipt_data.csv"
# output_folder = r"C:\Users\keren\OneDrive\Desktop\CAPSTONE FILES"
# generator = EmailTemplateGenerator(data_file_path, output_folder)
# sample_template_path = generator.create_email_templates()

# Display the sample template content
# try:
#     with open(sample_template_path, 'r') as file:
#         print("\nSample Template Contents:")
#         print("-" * 50)
#         print(file.read())
#         print("-" * 50)
# except Exception as e:
#     print(f"Error reading sample template: {str(e)}")
