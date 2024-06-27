# Example Script Output

This document provides examples of what you might see in the console and log file when running the Automated Invoice Email Processor.

## Console Output

When you run the script, you might see output similar to this in your console:

```
2023-06-27 10:00:01 - INFO - Starting email fetching process
2023-06-27 10:00:02 - INFO - Gmail service built successfully
2023-06-27 10:00:02 - INFO - Fetching emails received in the last 24 hours (after timestamp: 2023/06/26)
2023-06-27 10:00:03 - INFO - Fetched 5 messages
2023-06-27 10:00:03 - INFO - Processing message ID 1234abcd
2023-06-27 10:00:04 - INFO - Invoice detected in attachment: invoice_123.pdf
2023-06-27 10:00:05 - INFO - Email forwarded for message ID 1234abcd
2023-06-27 10:00:05 - INFO - Processing message ID 5678efgh
2023-06-27 10:00:06 - INFO - Invoice detected in email body
2023-06-27 10:00:07 - INFO - Email forwarded for message ID 5678efgh
2023-06-27 10:00:07 - INFO - Processing message ID 91011ijkl
2023-06-27 10:00:08 - INFO - No invoice detected
2023-06-27 10:00:08 - INFO - Processing message ID 121314mnop
2023-06-27 10:00:09 - INFO - Invoice detected in attachment: bill_456.pdf
2023-06-27 10:00:10 - INFO - Email forwarded for message ID 121314mnop
2023-06-27 10:00:10 - INFO - Processing message ID 151617qrst
2023-06-27 10:00:11 - INFO - No invoice detected
2023-06-27 10:00:11 - INFO - Email fetching process completed
```

This output shows the script starting, fetching emails, processing each email, detecting invoices, and forwarding relevant emails.

## Log File Example

The log file (`invoice_processor.log`) will contain more detailed information. Here's an example of what it might look like:

```
2023-06-27 10:00:01,123 - INFO - Starting email fetching process
2023-06-27 10:00:01,234 - INFO - Loaded credentials from token.json
2023-06-27 10:00:01,345 - INFO - Building Gmail service
2023-06-27 10:00:02,456 - INFO - Gmail service built successfully
2023-06-27 10:00:02,567 - INFO - Fetching emails received in the last 24 hours (after timestamp: 2023/06/26)
2023-06-27 10:00:02,678 - INFO - Querying emails with: in:inbox after:2023/06/26
2023-06-27 10:00:03,789 - INFO - Number of messages fetched: 5
2023-06-27 10:00:03,890 - INFO - Processing message ID 1234abcd
2023-06-27 10:00:04,001 - DEBUG - Email body: Subject: Invoice for June Services...
2023-06-27 10:00:04,112 - INFO - Invoice detected in attachment: invoice_123.pdf
2023-06-27 10:00:05,223 - INFO - Email forwarded successfully to accounting@yourcompany.com. Sent message ID: 1234abcd_fwd
2023-06-27 10:00:05,334 - INFO - Processing message ID 5678efgh
2023-06-27 10:00:05,445 - DEBUG - Email body: Dear client, Please find attached the invoice for...
2023-06-27 10:00:06,556 - INFO - Invoice detected in email body
2023-06-27 10:00:07,667 - INFO - Email forwarded successfully to accounting@yourcompany.com. Sent message ID: 5678efgh_fwd
...
2023-06-27 10:00:11,111 - INFO - Email fetching process completed
```

This log file provides more detailed information about each step of the process, including debug information showing snippets of email content (be careful not to log sensitive information in production environments).
