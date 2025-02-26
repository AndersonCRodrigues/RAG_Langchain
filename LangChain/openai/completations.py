from langchain_openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def completatios():
    openai = OpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo-instruct")
    temperature = 0.1
    frequency_penalty = 1
    presence_penalty = 1
    max_tokens = 500
    n = 1
    seed = 123

    return openai.invoke(
        input="Quem foi Carl Sagan?",
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        max_tokens=max_tokens,
        n=n,
        seed=seed,
    )


print(completatios())
