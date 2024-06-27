# Example Configuration File (config.py)

# Path to your OAuth 2.0 Client ID JSON file
CREDENTIALS_PATH = 'client_secret.json'

# Email address to forward invoices to
RECEIVER_EMAIL = "accounting@yourcompany.com"

# Directory to temporarily store attachments
ATTACHMENTS_DIR = './attachments'

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.compose',
          'https://mail.google.com/']

# Label to add to processed emails
PROCESSED_LABEL = 'processed'

# File to store the timestamp of the last processed email
LAST_TIMESTAMP_FILE = 'last_timestamp.json'

# Logging configuration
LOG_FILE = 'invoice_processor.log'
LOG_LEVEL = 'INFO'

# Invoice keywords for detection
INVOICE_KEYWORDS = ["invoice", "bill", "invoice number", "invoice date", "due date",
                    "payment terms", "ordrenr", "leveringsdato", "referanse", "bankgiro",
                    "vat", "mva", "total due", "amount due", "balance due", "net amount"]

# Invoice patterns for detection (regular expressions)
INVOICE_PATTERNS = [r"\d{2}/\d{2}/\d{4}", r"\$\d+\.\d{2}", r"invoice\s+no\.\s*\d+"]

# Time range for fetching emails (in hours)
EMAIL_FETCH_TIMERANGE = 24
