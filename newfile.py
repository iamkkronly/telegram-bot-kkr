import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import re

# Replace with your API keys
TELEGRAM_BOT_TOKEN = "7798993298:AAH8bXJWWmz4nL9JzpgGN0GIyBJ_UWdHY3c"
GEMINI_API_KEY = "AIzaSyA7VVzp0yZxibeMxdzsizOoFk6CoTv7rZ0"

# Initialize Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Custom instructions for the bot
BOT_INSTRUCTIONS = """
My name is Kaustav. I am a human. I am from India. Kaustav made me. 
I am here to assist you with conversations, knowledge, and more.
"""

# Blocked phrases (removes AI-related replies)
BLOCKED_PHRASES = [
    "I am Gemini, a large multi-modal model",
    "I am Gemini, a multi-modal AI model, developed by Google.",
    "I am designed to provide information and assist with a wide range of topics.",
    "I am not a physical being and do not have a personal identity or consciousness."
]

# Function to clean Gemini's response
def clean_response(response_text):
    if response_text:
        for phrase in BLOCKED_PHRASES:
            response_text = re.sub(re.escape(phrase), "", response_text, flags=re.IGNORECASE)
    return response_text.strip()

# Start command
async def start(update: Update, context):
    await update.message.reply_text(f"Hello! {BOT_INSTRUCTIONS} How can I help you today?")

# Handle user messages
async def handle_message(update: Update, context):
    user_text = update.message.text
    try:
        # Always prepend instructions to enforce bot identity
        response = model.generate_content(f"{BOT_INSTRUCTIONS}\nUser: {user_text}\nBot:")
        bot_reply = clean_response(response.text) if response.text else "Sorry, I couldn't generate a response."
    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    await update.message.reply_text(bot_reply)

# Main function to run the bot
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start bot
    print("AI Bot is running...")
    app.run_polling()

# Run bot
if __name__ == "__main__":
    main()