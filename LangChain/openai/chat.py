from langchain_openai import ChatOpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def chat():
    openai = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")
    messages = [
        {
            "role": "system",
            "content": (
                "Você é um assistente que fornece informações sobre figuras "
                "históricas."
            ),
        },
        {"role": "user", "content": "Quem foi Carl Sagan"},
    ]

    return openai.invoke(messages).content


print(chat())
