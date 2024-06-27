# Setting up Google Cloud Console Project

This guide will walk you through the process of setting up a Google Cloud Console project and enabling the Gmail API for use with the Automated Invoice Email Processor.

## 1. Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click on the project drop-down and select "New Project".
3. Enter a project name (e.g., "Invoice Email Processor").
4. Click "Create".

## 2. Enable the Gmail API

1. In the Google Cloud Console, go to the [API Library](https://console.cloud.google.com/apis/library).
2. Search for "Gmail API".
3. Click on "Gmail API" in the results.
4. Click "Enable".

## 3. Create OAuth 2.0 Client ID

1. Go to the [Credentials page](https://console.cloud.google.com/apis/credentials).
2. Click "Create Credentials" and select "OAuth client ID".
3. If prompted, configure the OAuth consent screen:
   - Select "External" user type.
   - Fill in the required fields (App name, User support email, Developer contact information).
   - Add the following scopes: `../auth/gmail.readonly`, `../auth/gmail.send`, `../auth/gmail.compose`, `https://mail.google.com/`.
   - Add your email address as a test user.
4. For application type, choose "Desktop app".
5. Name your OAuth 2.0 client ID (e.g., "Invoice Email Processor Client").
6. Click "Create".

## 4. Download the Client Configuration

1. After creating the OAuth client ID, you'll see a pop-up with your client ID and client secret.
2. Click "Download" to download the client configuration file.
3. Rename the downloaded file to `client_secret.json`.
4. Move `client_secret.json` to your project directory.

## 5. Update Configuration

1. In your project's `config.py` file, ensure the `CREDENTIALS_PATH` variable points to your `client_secret.json` file:

   ```python
   CREDENTIALS_PATH = 'client_secret.json'
   ```

2. Update other configuration variables as needed.

## 6. Run the Script

1. Run the script for the first time:

   ```
   python invoice_processor.py
   ```

2. You'll be prompted to authorize the application. Follow the URL provided in the console.
3. Sign in with your Google account and grant the requested permissions.
4. After successful authorization, the script will create a `token.json` file in your project directory.

Your Google Cloud Console project is now set up and ready to use with the Automated Invoice Email Processor.
