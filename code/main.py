import openai
from telegram.ext.updater import Updater
from telegram.ext.commandhandler import CommandHandler
import config


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hello, I'm dutchman chat bot!")


def ask_question(update, context):
    question = update.message.text
    response = request_to_chat_gpt(question)
    context.bot.send_message(chat_id=update.message.chat_id, text=response,
                             reply_to_message_id=update.message.message_id)


def request_to_chat_gpt(question):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )
    response = completion.choices[0].message.content
    return response


def set_up_bot():
    updater = Updater(config.TELEGRAM_BOT_API_KEY, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('gpt', ask_question))
    return updater


if __name__ == "__main__":
    openai.api_key = config.OPEN_AI_API_KEY
    set_up_bot().start_polling()

