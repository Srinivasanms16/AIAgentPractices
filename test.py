from dotenv import load_dotenv
from openai import OpenAI
import os

class Me:
    def __init__(self):
        load_dotenv(override=True)
        self.apikey = os.getenv("OPENROUTER_API_KEY")

    def print(self):
        print(self.apikey)

if __name__ == "__main__":
    print("hi")
    me = Me()
    me.print()