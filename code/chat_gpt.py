import openai


async def request_to_chat_gpt(messages):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        response = completion.choices[0].message.content
        return response
    except Exception as e:
        raise e
