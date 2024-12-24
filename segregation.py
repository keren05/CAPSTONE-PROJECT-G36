import pandas as pd

class DataSegregator:
    def __init__(self, data_file_path, output_folder):
        """
        Initialize the DataSegregator with file paths.

        Args:
            data_file_path (str): Path to the input dataset.
            output_folder (str): Path to the folder where segregated files will be saved.
        """
        self.data_file_path = data_file_path
        self.output_folder = output_folder

    def segregate_data(self):
        """
        Segregate data into Card and Cheque categories and save the results into separate CSV files.

        Returns:
            dict: Paths to the segregated files (Card and Cheque).
        """
        # Load the dataset
        data = pd.read_csv(self.data_file_path)

        if 'transaction_type' not in data.columns:
            raise ValueError("The dataset must contain a 'transaction_type' column.")

        card_data = data[data['transaction_type'].str.strip().str.lower() == 'card']
        cheque_data = data[data['transaction_type'].str.strip().str.lower() == 'cheque']

        # Define file paths for output
        card_file_path = f"{self.output_folder}/card_data.csv"
        cheque_file_path = f"{self.output_folder}/cheque_data.csv"

        # Save the segregated data to CSV files
        card_data.to_csv(card_file_path, index=False)
        cheque_data.to_csv(cheque_file_path, index=False)

        print(f"Card data saved to: {card_file_path}")
        print(f"Cheque data saved to: {cheque_file_path}")

        return {
            "card_file": card_file_path,
            "cheque_file": cheque_file_path
        }

# Example usage:
# data_file_path = r"C:\Users\keren\OneDrive\Downloads\capstone\synthetic_receipt_data.csv"
# output_folder = r"C:\Users\keren\OneDrive\Downloads\capstone\segregated_output"
# segregator = DataSegregator(data_file_path, output_folder)
# segregator.segregate_data()
