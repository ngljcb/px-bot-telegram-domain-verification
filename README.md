# Telegram Domain Verification Bot

This bot restricts access to Telegram users by verifying their email address. Users must enter an email with the specified domain and verify their identity using a One-Time Password (OTP) sent via email.

## Features

- Accepts only users with emails from a predefined domain (e.g., `university.edu`).
- Sends an OTP to the provided email for verification.
- Maintains a persistent list of verified users in a JSON file.
- Allows cancellation of the verification process at any stage.

## Prerequisites

- Python 3.7 or later.
- A Telegram bot token (generated using [BotFather](https://core.telegram.org/bots#botfather)).
- An email account configured to send OTP emails.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/ngljcb/px-bot-telegram-domain-verification.git
   cd px-bot-telegram-domain-verification
   ```

2. Install dependencies:

   ```bash
   pip install python-telegram-bot
   ```

3. Update the script:

   - Replace `"YOUR_BOT_TOKEN"` in the `main()` function with your Telegram bot token.
   - Replace `"your-email@example.com"` and `"your-email-password"` in the `send_email()` function with your Gmail credentials.
   - Set your university email domain by updating the `UNIVERSITY_DOMAIN` variable.

4. Run the bot:
   ```bash
   python bot.py
   ```

## Usage

1. Start the bot by sending the `/start` command.
2. Provide your university email when prompted.
3. Enter the OTP sent to your email address.
4. Once verified, you gain access to the bot's features.

## File Structure

- `bot.py`: The main script containing bot logic and email sending functionality.
- `verified_users.json`: A JSON file to store verified users' information persistently.

## Security

- Use environment variables or a secret management tool to store sensitive credentials (e.g., bot token, email password).
- If using Gmail, consider enabling 2-Step Verification and generating an app-specific password for added security.

## Troubleshooting

- **Email not received**: Ensure the sender's Gmail account is properly configured, and verify the recipient email's spam folder.
- **Invalid OTP**: Ensure the correct OTP is entered before it expires.
