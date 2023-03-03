import openai
from telegram.ext.updater import Updater
from telegram.ext.commandhandler import CommandHandler
import config
from openai_tools import chat_gpt, dall_e


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hello, I'm dutchman chat bot!")


def ask_question(update, context):
    question = update.message.text
    response = chat_gpt.request_to_chat_gpt(question)
    context.bot.send_message(chat_id=update.message.chat_id, text=response,
                             reply_to_message_id=update.message.message_id)


def ask_image(update, context):
    image = update.message.text
    response = dall_e.request_to_dall_e(image)
    print(response)
    context.bot.send_photo(chat_id=update.message.chat_id, photo=response,
                           reply_to_message_id=update.message.message_id)


def set_up_bot():
    updater = Updater(config.TELEGRAM_BOT_API_KEY, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('gpt', ask_question))
    dispatcher.add_handler(CommandHandler('dalle', ask_image))

    return updater


if __name__ == "__main__":
    openai.api_key = config.OPEN_AI_API_KEY
    set_up_bot().start_polling()
    # ask_image.request_to_dall_e()


