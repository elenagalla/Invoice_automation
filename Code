from __future__ import print_function
import re
import os
import base64
import time
import pdfplumber
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from transformers import DonutProcessor, VisionEncoderDecoderModel
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email import encoders
from PIL import Image
import logging
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from io import BytesIO
import email

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Scopes and credentials
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.compose', 'https://mail.google.com/']
CREDENTIALS_PATH = 'C:\\Users\\User\\Documents\\GitHub\\elena_project\\autogen\\jsonclient_secret_864676982851-49gtof7lldbis507iao7r0f0r6v95jvl.apps.googleusercontent.com.json'
PROCESSED_LABEL = 'processed'
ATTACHMENTS_DIR = './attachments'
RECEIVER_EMAIL = "elena@jarccel.com"
LAST_TIMESTAMP_FILE = 'last_timestamp.json'

# Ensure attachments directory exists
if not os.path.exists(ATTACHMENTS_DIR):
    os.makedirs(ATTACHMENTS_DIR)

# Initialize the invoice classification model
model = VisionEncoderDecoderModel.from_pretrained(
    "to-be/donut-base-finetuned-invoices")
processor = DonutProcessor.from_pretrained(
    "to-be/donut-base-finetuned-invoices")


def get_last_timestamp():
    if os.path.exists(LAST_TIMESTAMP_FILE):
        with open(LAST_TIMESTAMP_FILE, 'r') as file:
            return json.load(file).get('last_timestamp')
    return None


def update_last_timestamp(timestamp):
    with open(LAST_TIMESTAMP_FILE, 'w') as file:
        json.dump({'last_timestamp': timestamp}, file)


def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        logging.info("Loaded credentials from token.json")
    else:
        logging.info("token.json not found, need to authorize")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                logging.info("Refreshed credentials")
            except Exception as e:
                logging.error(f"Error refreshing credentials: {e}")
                creds = None
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            logging.info("Completed authorization flow")
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            logging.info("Saved credentials to token.json")

    logging.info("Building Gmail service")
    service = build('gmail', 'v1', credentials=creds)
    logging.info("Gmail service built successfully")
    return service


def extract_invoice_data(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        pixel_values = processor(image, return_tensors="pt").pixel_values
        outputs = model.generate(pixel_values)
        result = processor.decode(outputs[0], skip_special_tokens=True)
        logging.info(f"Extracted invoice data from {image_path}: {result}")
        return result
    except Exception as e:
        logging.error(f"Error extracting invoice data from {image_path}: {e}")
        return None


def is_invoice(text):
    invoice_keywords = ["invoice", "bill", "invoice number", "invoice date", "due date", "payment terms", "ordrenr",
                        "leveringsdato", "referanse", "bankgiro", "vat", "mva", "total due", "amount due", "balance due", "net amount"]
    patterns = [r"\d{2}/\d{2}/\d{4}", r"\$\d+\.\d{2}", r"invoice\s+no\.\s*\d+"]

    text_lower = text.lower()
    keyword_found = any(
        keyword.lower() in text_lower for keyword in invoice_keywords)
    pattern_found = any(re.search(pattern, text_lower) for pattern in patterns)

    if keyword_found or pattern_found:
        logging.info(f"Detected invoice content in text: {text[:100]}...")
        return True
    return False


def fetch_emails(service, last_timestamp):
    try:
        query = f'in:inbox after:{last_timestamp}'
        logging.info(f"Querying emails with: {query}")
        results = service.users().messages().list(userId='me', q=query).execute()
        messages = results.get('messages', [])
        logging.info(f"Full API response: {results}")
        logging.info(f"Number of messages fetched: {len(messages)}")
        return messages
    except HttpError as error:
        logging.error(f'An error occurred: {error}')
        return []


def add_label_to_email(service, message_id, label_name):
    try:
        label_id = None
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        for label in labels:
            if label['name'] == label_name:
                label_id = label['id']
                break

        if not label_id:
            logging.warning(f"Label '{label_name}' not found")
            return

        service.users().messages().modify(userId='me', id=message_id,
                                          body={'addLabelIds': [label_id]}).execute()
        logging.info(f"Label '{label_name}' added to email ID {message_id}")
    except HttpError as error:
        logging.error(f'An error occurred while adding label: {error}')


def extract_invoice_info(pdf_path):
    try:
        if not pdf_path.lower().endswith('.pdf'):
            logging.info(f"Skipping non-PDF file: {pdf_path}")
            return None, None
        with pdfplumber.open(pdf_path) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            logging.info(f"Extracted text from {pdf_path}: {text[:500]}...")
            if is_invoice(text):
                return text, None
            else:
                logging.info(f"File {pdf_path} is not an invoice.")
                return None, None
    except Exception as e:
        logging.error(f"Error processing PDF {pdf_path}: {e}")
        return None, None


def create_pdf_from_text(text):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica", 10)
    x_margin = 0.5 * inch
    y_margin = height - 0.5 * inch
    line_height = 12

    lines = text.split('\n')
    y_position = y_margin

    for line in lines:
        if not line.strip():
            y_position -= line_height  # Add space for empty lines
        else:
            if "Invoice #" in line or "Date:" in line:
                c.setFont("Helvetica-Bold", 12)
            elif "From:" in line or "To:" in line:
                c.setFont("Helvetica-Bold", 10)
                y_position -= line_height  # Add space before these lines
            elif "Description of Services:" in line:
                c.setFont("Helvetica-Bold", 10)
                y_position -= line_height  # Add space before these lines
            else:
                c.setFont("Helvetica", 10)

            c.drawString(x_margin, y_position, line.strip())
            y_position -= line_height

    c.save()
    buffer.seek(0)
    return buffer


def clean_email_body(body):
    # Remove unwanted HTML tags
    body = re.sub(r'<div dir="ltr">', '', body)
    body = re.sub(r'Sender Information:<br>', '', body)
    body = re.sub(r'</div>', '', body)
    return body


def forward_email(service, message_id, receiver_email, invoice_in_body=False):
    try:
        msg = service.users().messages().get(
            userId='me', id=message_id, format='raw').execute()

        raw_msg = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
        email_message = email.message_from_bytes(raw_msg)

        forward = MIMEMultipart()
        forward['to'] = receiver_email
        forward['from'] = 'me'
        forward['subject'] = "Fwd: " + email_message['subject']

        body = ""
        attached_filenames = set()
        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get_content_type() == 'text/plain':
                body += part.get_payload(decode=True).decode('utf-8')
            if part.get('Content-Disposition') is not None:
                if 'attachment' in part.get('Content-Disposition'):
                    if part.get_filename() not in attached_filenames:
                        forward.attach(part)
                        attached_filenames.add(part.get_filename())

        # Clean the email body
        body = clean_email_body(body)
        forward.attach(MIMEText(body, 'plain'))

        # If invoice is in the body, create and attach PDF
        if invoice_in_body:
            pdf_buffer = create_pdf_from_text(body)
            pdf_attachment = MIMEApplication(
                pdf_buffer.getvalue(), _subtype="pdf")
            pdf_attachment.add_header(
                'Content-Disposition', 'attachment', filename="invoice.pdf")
            forward.attach(pdf_attachment)

        # Send the email
        raw_forward = {'raw': base64.urlsafe_b64encode(
            forward.as_bytes()).decode('UTF-8')}
        sent_message = service.users().messages().send(
            userId='me', body=raw_forward).execute()
        logging.info(
            f"Email forwarded successfully to {receiver_email}. Sent message ID: {sent_message['id']}")

        # Mark original email as read and add processed label
        service.users().messages().modify(userId='me', id=message_id,
                                          body={'removeLabelIds': ['UNREAD']}).execute()
        add_label_to_email(service, message_id, PROCESSED_LABEL)

    except HttpError as error:
        logging.error(f"Error forwarding email: {error}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


def process_email(service, message):
    msg = service.users().messages().get(
        userId='me', id=message['id']).execute()

    # Get the full email body
    full_body = ""
    if 'parts' in msg['payload']:
        for part in msg['payload']['parts']:
            if part['mimeType'] == 'text/plain':
                full_body += base64.urlsafe_b64decode(
                    part['body']['data']).decode('utf-8')
    else:
        full_body = base64.urlsafe_b64decode(
            msg['payload']['body']['data']).decode('utf-8')

    logging.info(f"Processing message ID {message['id']}")
    # Log the first 500 characters of the email body
    logging.debug(f"Email body: {full_body[:500]}...")

    invoice_in_attachment = False
    invoice_in_body = False

    # Check attachments for invoice
    if 'parts' in msg['payload']:
        for part in msg['payload']['parts']:
            if part['filename'] and part['filename'].lower().endswith('.pdf'):
                attachment = service.users().messages().attachments().get(
                    userId='me', messageId=message['id'], id=part['body']['attachmentId']
                ).execute()
                data = base64.urlsafe_b64decode(
                    attachment['data'].encode('UTF-8'))

                # Save attachment temporarily
                temp_path = os.path.join(ATTACHMENTS_DIR, part['filename'])
                with open(temp_path, 'wb') as f:
                    f.write(data)

                # Check if it's an invoice
                invoice_data, _ = extract_invoice_info(temp_path)
                if invoice_data:
                    invoice_in_attachment = True
                    logging.info(
                        f"Invoice detected in attachment: {part['filename']}")
                    break

                # Remove temporary file if not an invoice
                os.remove(temp_path)

    # If no invoice in attachment, check body
    if not invoice_in_attachment:
        invoice_in_body = is_invoice(full_body)
        if invoice_in_body:
            logging.info("Invoice detected in email body")

    # Forward the email with the body and any detected invoice attachment
    forward_email(service, message['id'], RECEIVER_EMAIL, invoice_in_body)
    logging.info(
        f"Email forwarded for message ID {message['id']}")

    # Mark the email as read and add processed label
    service.users().messages().modify(userId='me', id=message['id'], body={
        'removeLabelIds': ['UNREAD']}).execute()
    add_label_to_email(service, message['id'], PROCESSED_LABEL)


def main():
    logging.info("Starting email fetching process")
    service = get_gmail_service()
    # Get the timestamp for 48 hours ago
    last_timestamp = (datetime.utcnow() - timedelta(hours=24)
                      ).strftime('%Y/%m/%d')
    logging.info(
        f"Fetching emails received in the last 24 hours (after timestamp: {last_timestamp})")

    new_timestamp = datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S')
    messages = fetch_emails(service, last_timestamp)
    logging.info(f"Fetched {len(messages)} messages")

    if messages:
        for message in messages:
            process_email(service, message)
        update_last_timestamp(new_timestamp)
    else:
        logging.info("No new emails found")

    logging.info("Email fetching process completed")


if __name__ == "__main__":
    main()
