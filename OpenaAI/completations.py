import os
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
openai.api_key = OPENAI_API_KEY


def completion():
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt="Crie uma canção contendo apenas uma estrofe.",
        max_tokens=60,
    )
    return response.choices[0].text.strip()


print(completion())
