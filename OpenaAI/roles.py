import os
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
openai.api_key = OPENAI_API_KEY


def roles():
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": "Você é um assistente de investimentos fictício."},
            {"role": "user",
             "content": (
                 "Qual é o melhor investimento de baixo risco recomendado "
                 "para este ano?"
             )}
        ],
        max_tokens=60,
    )

    return response.choices[0].message.content


print(roles())
