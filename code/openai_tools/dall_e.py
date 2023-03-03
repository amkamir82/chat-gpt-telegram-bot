import openai


def request_to_dall_e(image):
    prompt = image[7::]
    response = openai.Image.create(prompt=prompt, n=1, size="1024x1024")
    return response["data"][0]["url"]
