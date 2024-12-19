import os
import io
import openai
from openai.error import OpenAIError
from telegram import Update, InputFile
from telegram.ext import (ApplicationBuilder, CommandHandler,
                          MessageHandler, ConversationHandler, ContextTypes, filters)
from PyPDF2 import PdfReader
from docx import Document
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not openai.api_key or not TELEGRAM_BOT_TOKEN:
    raise ValueError("API keys not set properly. Please check your .env file.")

# States for conversation
CHOOSING, PROCESS_DOCUMENT, LEARNING_MODE = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Do you want to 'generate a quiz' or 'learn about a topic'? \nPlease type 'quiz' or 'learn'."
    )
    return CHOOSING

async def choose_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.lower()
    
    # Handle quiz confirmation after summarization
    if context.user_data.get("waiting_for_quiz_confirmation"):
        if user_input == "yes":
            topic = context.user_data.get("topic")
            await update.message.reply_text("Generating quiz on the topic... Please wait.")
            quiz = generate_quiz(topic)
            await update.message.reply_text(quiz)
        elif user_input == "no":
            await update.message.reply_text("Okay! If you need anything else, just type 'quiz' or 'learn'.")
        else:
            await update.message.reply_text("Invalid option. Please type 'yes' or 'no'.")
        
        # Reset the flag
        context.user_data["waiting_for_quiz_confirmation"] = False
        context.user_data.pop("topic", None)
        return CHOOSING

    # Handle the initial choice
    if user_input == "quiz":
        await update.message.reply_text("Please upload a document (.txt, .docx, or .pdf) to generate a quiz.")
        return PROCESS_DOCUMENT
    elif user_input == "learn":
        await update.message.reply_text("Please send me the topic you want to learn about.")
        return LEARNING_MODE
    else:
        await update.message.reply_text("Invalid option. Please type 'quiz' or 'learn'.")
        return CHOOSING


async def process_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.document.get_file()
    file_name = update.message.document.file_name.lower()
    file_stream = io.BytesIO(await file.download_as_bytearray())

    if file_name.endswith(".txt"):
        content = file_stream.read().decode("utf-8")
    elif file_name.endswith(".docx"):
        content = process_docx(file_stream)
    elif file_name.endswith(".pdf"):
        content = process_pdf(file_stream)
    else:
        await update.message.reply_text("Unsupported file type. Please upload a .txt, .docx, or .pdf file.")
        return CHOOSING

    await update.message.reply_text("Generating quiz... This may take a moment.")
    quiz = generate_quiz(content)
    await update.message.reply_text(quiz)

    return CHOOSING

def process_docx(file_stream):
    document = Document(file_stream)
    content = "\n".join([p.text for p in document.paragraphs])
    return content

def process_pdf(file_stream):
    reader = PdfReader(file_stream)
    content = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return content

async def learning_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = update.message.text
    await update.message.reply_text("Summarizing the topic... Please wait.")
    summary = summarize_topic(topic)
    await update.message.reply_text(summary)
    
    await update.message.reply_text("Would you like to generate a quiz on this topic? (yes/no)")
    context.user_data["waiting_for_quiz_confirmation"] = True
    context.user_data["topic"] = topic
    return CHOOSING



def generate_quiz(content):
    prompt = f"Generate a multiple-choice quiz with answers based on the following content:\n{content}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates quizzes."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        return response['choices'][0]['message']['content'].strip()
    except OpenAIError as e:
        return f"An error occurred while generating the quiz: {e}"

def summarize_topic(topic):
    prompt = f"Summarize the key points about the following topic:\n{topic}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes topics."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        return response['choices'][0]['message']['content'].strip()
    except OpenAIError as e:
        return f"An error occurred while summarizing the topic: {e}"


async def handle_quiz_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.lower()
    topic = context.user_data.get("topic")
    
    if user_input == "yes" and topic:
        await update.message.reply_text("Generating quiz on the topic... Please wait.")
        quiz = generate_quiz(topic)
        await update.message.reply_text(quiz)
    else:
        await update.message.reply_text("Okay! If you need anything else, just type 'quiz' or 'learn'.")
    
    return CHOOSING

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Goodbye!")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, choose_option),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_quiz_confirmation),
            ],
            PROCESS_DOCUMENT: [
                MessageHandler(filters.Document.ALL, process_document),
            ],
            LEARNING_MODE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, learning_mode),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
