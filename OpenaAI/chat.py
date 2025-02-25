import os
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
openai.api_key = OPENAI_API_KEY


def chat():
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Conte uma piada"},
        ]
    )
    return response.choices[0].message.content


print(chat())
