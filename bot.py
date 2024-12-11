from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import smtplib
import random
import json

# Constants
UNIVERSITY_DOMAIN = "university.edu"
VERIFIED_USERS_FILE = "verified_users.json"
OTP = {}

# Load verified users
try:
    with open(VERIFIED_USERS_FILE, "r") as file:
        verified_users = json.load(file)
except FileNotFoundError:
    verified_users = {}

# Save verified users
def save_verified_users():
    with open(VERIFIED_USERS_FILE, "w") as file:
        json.dump(verified_users, file)

# Email function
def send_email(to_email, otp):
    sender_email = "your-email@gmail.com"
    sender_password = "your-email-password"

    subject = "Your Verification Code"
    message = f"Your verification code is: {otp}"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, f"Subject: {subject}\n\n{message}")

# States for ConversationHandler
ASK_EMAIL, ASK_OTP = range(2)

# Start command
def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    if str(user.id) in verified_users:
        update.message.reply_text("You are already verified!")
        return ConversationHandler.END

    update.message.reply_text(
        "Welcome! Please provide your university email address to verify your identity."
    )
    return ASK_EMAIL

# Handle email input
def ask_email(update: Update, context: CallbackContext) -> int:
    email = update.message.text

    if not email.endswith(f"@{UNIVERSITY_DOMAIN}"):
        update.message.reply_text(
            f"Invalid email. Please provide an email ending with @{UNIVERSITY_DOMAIN}."
        )
        return ASK_EMAIL

    otp = random.randint(100000, 999999)
    OTP[update.effective_user.id] = otp
    try:
        send_email(email, otp)
        context.user_data['email'] = email
        update.message.reply_text("An OTP has been sent to your email. Please enter it here.")
        return ASK_OTP
    except Exception as e:
        update.message.reply_text(f"Failed to send email: {e}")
        return ConversationHandler.END

# Handle OTP input
def ask_otp(update: Update, context: CallbackContext) -> int:
    user_id = update.effective_user.id
    user_otp = update.message.text

    if user_id in OTP and str(OTP[user_id]) == user_otp:
        email = context.user_data['email']
        verified_users[str(user_id)] = email
        save_verified_users()
        del OTP[user_id]
        update.message.reply_text("Verification successful! You now have access.")
        return ConversationHandler.END

    update.message.reply_text("Invalid OTP. Please try again.")
    return ASK_OTP

# Cancel command
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Verification process cancelled.")
    return ConversationHandler.END

# Main function
def main():
    updater = Updater("YOUR_BOT_TOKEN")

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_EMAIL: [MessageHandler(Filters.text & ~Filters.command, ask_email)],
            ASK_OTP: [MessageHandler(Filters.text & ~Filters.command, ask_otp)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
