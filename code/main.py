import openai
import config
from telegram.telegram import run

if __name__ == "__main__":
    openai.api_key = config.OPEN_AI_API_KEY
    run()
