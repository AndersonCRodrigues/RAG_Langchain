import os
from langchain_openai import OpenAI
from langchain.cache import SQLiteCache
from langchain.globals import set_llm_cache

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
openai = OpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo-instruct")


def completations():
    set_llm_cache(SQLiteCache(database_path="openai_cache.db"))
    prompt = "Me diga em poucas palavras quem foi Neil Armstrong."
    response1 = openai.invoke(prompt, max_tokens=100)
    print("Primeira Chamada (usando api):", response1)
    response2 = openai.invoke(prompt, max_tokens=100)
    print("Segunda Chamada (usando cache):", response2)


completations()
