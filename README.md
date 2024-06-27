# Automated Invoice Email Processor
This project automates the process of fetching, identifying, and forwarding invoice emails using the Gmail API. It's designed to run daily, processing new emails and forwarding relevant invoices to a specified email address.

## Features

- Fetches emails from Gmail inbox

- Identifies invoices in email attachments and body content

- Forwards identified invoices to a specified email address

- Marks processed emails with a custom label

- Logs activities for easy monitoring and debugging

## Prerequisites

- Python 3.7+

- Google Cloud Console project with Gmail API enabled

- OAuth 2.0 Client ID credentials

## Installation

Clone this repository:
```bash
git clone https://github.com/yourusername/elena_project.git
cd elena_project
```

Install required Python packages:
```bash
pip install -r requirements.txt
```

## Set up OAuth 2.0 Client ID and download the JSON file:

a. Go to the Google Cloud Console.

b. Create a new project or select an existing one.

c. Enable the Gmail API for your project:
  In the sidebar, click on "APIs & Services" > "Library"
  Search for "Gmail API" and click on it
  Click "Enable"

d. Create OAuth 2.0 Client ID credentials:

  In the sidebar, click on "APIs & Services" > "Credentials"
  Click "Create Credentials" and select "OAuth client ID"
  Choose "Desktop app" as the application type
  Give your OAuth 2.0 client a name (e.g., "Elena Project")
  Click "Create"

e. Download the Client ID JSON file:

  In the OAuth 2.0 Client IDs section, find the client you just created
  Click the download icon (down arrow) to download the JSON file

f. Place the downloaded JSON file in your project directory and rename it to client_secret.json.

## Configuration
Update the following variables in the script

- CREDENTIALS_PATH: Path to your OAuth 2.0 Client ID JSON file (should be 'client_secret.json' if you followed the steps above)

- RECEIVER_EMAIL: Email address to forward invoices to

- ATTACHMENTS_DIR: Directory to temporarily store attachments (default is './attachments')


Run the script once to authorize it with your Google account:
```bash
python invoice_processor.py
```
This will open a browser window asking you to log in to your Google account and grant the necessary permissions to the application.

## Usage
The script is designed to be run daily. You can set it up to run automatically using Task Scheduler on Windows or cron on Unix-based systems.

### Setting up Task Scheduler (Windows)

 1. Open Task Scheduler

      Press the Windows key and type "Task Scheduler"
 
      Click on "Task Scheduler" in the search results


2. Create a New Task

      In the Task Scheduler window, click on "Create Basic Task" in the right-hand Actions panel


3. Name Your Task

      Enter a name for your task (e.g., "Elena Invoice Processor")
 
      Optionally, enter a description
    
      Click "Next"


4. Set the Trigger

      Select "Daily" as the trigger

      Click "Next"


5. Configure the Trigger

      Set the start date and time you want the task to first run
 
      Ensure "Recur every" is set to 1 day
  
      Click "Next"


6. Choose the Action

      Select "Start a program"
 
      Click "Next"


7. Set Up the Program

      In the "Program/script" field, browse to and select your Python executable
      (e.g., C:\Python39\python.exe)
 
      In the "Add arguments" field, enter the full path to your script in quotes
      (e.g., "C:\path\to\elena_project\invoice_processor.py")
  
      In the "Start in" field, enter the path to your project directory
      (e.g., C:\path\to\elena_project)
      Click "Next"


8. Review and Finish

      Review your settings
 
      Click "Finish"


9. Note - Modify Task Settings (Optional but Recommended)

      Find your new task in the Task Scheduler Library
 
      Right-click on it and select "Properties"
  
      In the "General" tab, check "Run whether user is logged on or not" for the task to run even if you're not logged in
  
      Check "Run with highest privileges" to ensure the script has necessary permissions
  
      In the "Conditions" tab, uncheck "Start the task only if the computer is on AC power" if you want the task to run even on battery power
  
      In the "Settings" tab, check "Run task as soon as possible after a scheduled start is missed" to ensure the task runs if the computer was off at the scheduled time
  
      Click "OK" to save these changes


10. Test the Task

      Right-click on your task in the Task Scheduler Library
  
      Select "Run" to test if it works correctly
  
      Check the script's log file to confirm it ran successfully
  
## Troubleshooting

Check the log file (invoice_processor.log) for detailed information about each run.

Ensure your Google Cloud Console project has the Gmail API enabled.

Verify that your OAuth 2.0 Client ID has the correct scopes (https://www.googleapis.com/auth/gmail.readonly, https://www.googleapis.com/auth/gmail.send, https://www.googleapis.com/auth/gmail.compose, https://mail.google.com/).

If you encounter authentication errors, try deleting the token.json file (if it exists) and run the script again to re-authenticate.


## Logging
The script logs its activities to the console and can be configured to log to a file if needed. Check the logs for information about the script's operation and any errors that occur.
