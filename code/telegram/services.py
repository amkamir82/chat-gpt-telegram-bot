import json
import config
import aiofiles
from collections import defaultdict
from datetime import date

user_messages = defaultdict(lambda: {"messages_sent": 0, "last_update": date.today()})


async def save_messages_from_users(data):
    async with aiofiles.open(config.JSON_FILE_PATH, "a") as file:
        await file.write(json.dumps(data) + "\n")


async def update_limits(message):
    user_id = message.from_user.id

    user_data = user_messages[user_id]

    messages_sent = user_data["messages_sent"]
    last_update = user_data["last_update"]

    today = date.today()
    if last_update != today:
        messages_sent = 0
        user_data["last_update"] = today

    if messages_sent >= 20:
        await message.reply(
            "شما به حد مجاز استفاده از بات در روز رسیده‌اید. در هر روز امکان ارسال ۲۰ پیام به بات دارید.\n\nدرصورتی که نیاز دارید این لیمیت برای شما بیشتر شود، به آیدی @its_dutchman پیام دهید.")
        return False

    messages_sent += 1
    user_data["messages_sent"] = messages_sent
    return True


async def decrease_limit_for_user(message):
    user_id = message.from_user.id

    user_data = user_messages[user_id]

    messages_sent = user_data["messages_sent"]

    messages_sent -= 1
    user_data["messages_sent"] = messages_sent
