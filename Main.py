import gradio as gr
import openai
import os
import subprocess  # For running the script
from openai import OpenAI
import re
import shutil
from ocr import ReceiptProcessor
import pandas as pd
from segregation import DataSegregator
from emailtemplate import EmailTemplateGenerator
from emailautomation import EmailSender

# Initialize the OpenAI client
client = OpenAI()
folder_path = r"C:\\Users\\keren\\OneDrive\\Downloads\\capstone\\receipts images"

# Create Open an assistant
assistant = client.beta.assistants.create(
    name="Finance Chatbot",
    instructions="""
        You are a query bot who answers all the questions related to the provided data (Excel or CSV files).
        Respond professionally to queries such as 'fetch data,' 'provide information,' or similar requests.
        Ensure all answers are derived from the provided file data. Don't provide any unnecessary details.
        Please provide the response without any metadata or reference tags.
        Always greet users with 'How can I help you?' at the start of the conversation.
        Understand the context of previous queries and answer it accordingly.
    """,
    model='gpt-4-turbo',
    tools=[{'type': "file_search"}],
)

ASSISTANT_ID = assistant.id


# Create a vector store for file data
vector_store = client.beta.vector_stores.create(name="Financial Statements")

file_path = r"C:\Users\keren\PycharmProjects\FinanceReceipting\synthetic_data.json"

with open(file_path,  "rb") as file_stream:
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,
        files = [file_stream]
    )

assistant = client.beta.assistants.update(
    assistant_id = ASSISTANT_ID,
    tool_resources={"file_search":{"vector_store_ids":[vector_store.id]}},
)
# Conversation logic
def chatbot_conversation(user_input, history=None):
    if history is None:
        history = []

    # Create a thread for conversation
    thread = client.beta.threads.create(
        messages=[
            {
                'role': 'user',
                "content": user_input
            }
        ]
    )
    thread_id = thread.id

    # Generate a response from the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=ASSISTANT_ID,
    )

    try:
        while True:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run.completed_at:
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                response = re.sub(r'【.*?】', '', response)

                # Append the user and bot responses to the chat history
                history.append((user_input, response))
                return history, ""  # Clear the input box after sending
    except Exception as e:
        error_message = "An error occurred while retrieving data. Please try again."
        history.append((user_input, error_message))
        return history, ""  # Clear the input box after an error

# Upload and store files
UPLOAD_DIRECTORY = r"C:\Users\keren\PycharmProjects\FinanceReceipting\uploaded_files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


def upload_and_store(files):
    if files:
        uploaded_files = []
        for file in files:
            temp_path = file
            save_path = os.path.join(UPLOAD_DIRECTORY, os.path.basename(file.name))
            shutil.move(temp_path, save_path)
            uploaded_files.append(os.path.basename(file.name))
        return f"Files uploaded successfully: {', '.join(uploaded_files)}"
    return "No files uploaded."

# Function to process files by running the Python script
def process_files():
    ocr = ReceiptProcessor(r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe')

    ocr.process_receipts_from_folder(folder_path)



    seg = DataSegregator(r"C:\Users\keren\PycharmProjects\FinanceReceipting\uploaded_files\synthetic_receipt_data.csv",
                         r"C:\Users\keren\PycharmProjects\FinanceReceipting\uploaded_files")

    seg.segregate_data()

    templ = EmailTemplateGenerator(r"C:\Users\keren\PycharmProjects\FinanceReceipting\uploaded_files\synthetic_receipt_data.csv", r"C:\Users\keren\PycharmProjects\FinanceReceipting\uploaded_files\templates")
    sample_template_path = templ.create_email_templates()

    email_auto = EmailSender("smtp.gmail.com", 587,"chiragtrytest@gmail.com", "krucsivapyxuzhvo")
    email_auto.send_email_with_templates(r"C:\Users\keren\PycharmProjects\FinanceReceipting\uploaded_files\synthetic_receipt_data.csv",r"C:\Users\keren\PycharmProjects\FinanceReceipting\uploaded_files\templates", )


# Build the Gradio interface
with gr.Blocks() as app:
    gr.Markdown("# File Upload and Finance Chatbot App")

    with gr.Row():
        file_upload = gr.File(label="Upload your files", file_types=None, file_count="multiple")
        upload_button = gr.Button("Upload")

    with gr.Row():
        process_button = gr.Button("Process")
        process_output = gr.Textbox(label="Processing Output")

    with gr.Row():
        chatbot = gr.Chatbot(label="Chat History")
        state = gr.State()

        user_input = gr.Textbox(
            placeholder="Type your message here...",
            label="Your Message",
            show_label=False
        )
        send_button = gr.Button("Send", variant="primary")

    # Actions
    upload_button.click(upload_and_store, inputs=file_upload, outputs=process_output)
    process_button.click(process_files,   outputs=process_output)
    send_button.click(
        chatbot_conversation,
        inputs=[user_input, state],
        outputs=[chatbot, user_input]  # Clear the Textbox
    )

# Launch the app
if __name__ == "__main__":
    app.launch(share=True)
