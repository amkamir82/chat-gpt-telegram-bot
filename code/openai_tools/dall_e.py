import openai


def request_to_dall_e():
    response = openai.Image.create(prompt="A rabbit eating carrot sandwich", n=1, size="1024x1024")
    print(response)
    print()
    print(response["data"][0]["url"])
    return response["data"][0]["url"]
