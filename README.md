# Invoice Email Processor

## Overview
This project is an automated system that processes emails to detect and forward invoices. It uses the Gmail API to fetch unread emails, analyzes their content and attachments for invoice-related information, and forwards potential invoices to a specified email address.

## Features

- Fetches unread emails from a Gmail account

- Analyzes email content and attachments (PDFs) for invoice-related information

- Uses AI-powered invoice detection for image attachments

- Forwards detected invoices to a specified email address

- Marks processed emails as read and adds a custom label

- Runs on a scheduled basis to continuously check for new emails

## Prerequisites

- Python 3.7+

- Google Cloud Project with Gmail API enabled

- OAuth 2.0 Client ID credentials

## Installation

Clone this repository:
```bash
git clone https://github.com/your-username/invoice-email-processor.git
cd invoice-email-processor
```
Install required packages:
```bash
pip install -r requirements.txt
```

## Set up your Google Cloud Project and obtain OAuth 2.0 credentials:

- Go to the Google Cloud Console

- Create a new project or select an existing one

- Enable the Gmail API for your project

- Create OAuth 2.0 Client ID credentials

- Download the client configuration and save it as client_secret.json in the project directory


## Configuration

- Update the following variables in the script:

- CREDENTIALS_PATH: Path to your client_secret.json file

- RECEIVER_EMAIL: Email address to forward detected invoices

- ATTACHMENTS_DIR: Directory to save email attachments (default is './attachments')


(Optional) Adjust the SCOPES if you need different Gmail API permissions

## Usage
Run the script:
```python
python invoice_processor.py
```

The script will:

- Authenticate with the Gmail API (you'll need to authorize it in your browser the first time)

- Check for new unread emails every minute

- Process emails and attachments for invoice detection

- Forward detected invoices to the specified email address

Mark processed emails as read and add a custom label

## Logging
The script logs its activities to the console and can be configured to log to a file if needed. Check the logs for information about the script's operation and any errors that occur.
