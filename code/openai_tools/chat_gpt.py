import openai


def request_to_chat_gpt(question):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )
    response = completion.choices[0].message.content
    return response
