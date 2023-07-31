from pyrogram import Client
from pyrogram.handlers import MessageHandler

import config
from chat_gpt import request_to_chat_gpt
from telegram import services

app = Client(
    "dutchman-chat-gpt-bot",
    api_id=config.API_ID, api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)


async def get_all_replies(chat_id, message_id):
    replies = []

    message = await app.get_messages(chat_id=chat_id, message_ids=message_id)

    if message.reply_to_message:
        replies.append(message.reply_to_message)

    while message.reply_to_message:
        message = await app.get_messages(chat_id=chat_id, message_ids=message.reply_to_message.id)
        if message.reply_to_message:
            replies.append(message.reply_to_message)

    return replies


async def initial_responding(client, message):
    chat_id = message.chat.id
    message_id = message.id

    all_replies = await get_all_replies(chat_id, message_id)

    discussion = [{"role": "user", "content": message.text}]
    for reply in all_replies:
        discussion.append({"role": "system" if reply.from_user.id == 6656520488 else "user", "content": reply.text})

    response = await request_to_chat_gpt(discussion[::-1])

    await client.send_message(chat_id=message.chat.id, text=response, reply_to_message_id=message.id)

    await services.save_messages_from_users(
        {"First Name": f"{message.from_user.first_name}", "Username": f"@{message.from_user.username}", "Chat ID":
            f"{message.from_user.id}", "Message": f"{message.text}", "Response": f"{response}",
         "timestamp": f"{message.date}"})

    print(
        f"First Name: {message.from_user.first_name}\nUsername: @{message.from_user.username}\nChat ID: "
        f"{message.from_user.id}\nMessage: {message.text}\nResponse: {response}\n\n\n")


async def main(client, message):
    if message.text == "/start":
        await app.send_message(message.chat.id,
                               "سلام! به Dutchman Chat-GPT Bot خوش آمدید. این بات توسط @its_dutchman زده شده است. اگر سوالی داشتید یا پیشنهادی داشتید حتما پیام بدید. همچنین برای آشنایی با نحوه کارکرد بات روی /help بزنید.")

    elif message.text == "/help":
        await app.send_message(message.chat.id,
                               "برای استفاده از این بات، تنها کافی است که سوال خودتان را تایپ کرده و ارسال کنید. در صورتی که خواستید راجع به همان مکالمه فعلی سوال بپرسید، کافی است سوال جدیدتان را در ریپلای به پیام بات بپرسید.\n\n برای مثال اگر از بات پرسیدید که هوا چطور است و بات به شما جواب داد، اگر خواستید بگویید نه منظورم هوای امروز است، نیاز است که به پیام خود بات ریپلای بزنید.\n\n اگر میخواید مکالمه جدیدی شروع کنید تنها کافی است سوال‌تان را بدون ریپلای به هیچ پیامی ارسال کنید.\n\n اگر سوالی دارید به آیدی @its_dutchman پیام دهید.")

    elif str(message.chat.id) in config.BLOCK_LIST_CHATS:
        await app.send_message(message.chat.id,
                               "شما بیش از حد پیام داده‌اید و دیگر امکان سول پرسیدن تا مدتی را ندارید.")
    else:
        if await services.update_limits(message):
            await initial_responding(client, message)


def run():
    app.add_handler(MessageHandler(main))
    app.run()
