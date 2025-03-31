import os
import json
import hashlib
from langchain_openai import OpenAI
from langchain.globals import set_llm_cache

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
openai = OpenAI(api_key=OPENAI_API_KEY, model="gpt-3.5-turbo-instruct")


class SimpleDiskCache:
    def __init__(self, cache_dir="cache_dir"):
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_cache_path(self, key):
        hashed_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hashed_key}.json")

    def lookup(self, key, llm_string):
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            with open(cache_path, "r") as f:
                return json.load(f)
        return None

    def update(self, key, value, llm_string):
        cache_path = self._get_cache_path(key)
        with open(cache_path, "w") as f:
            json.dump(value, f)


cache = SimpleDiskCache()
set_llm_cache(cache)
prompt = "Me diga quem foi Neil Degrasse Tyson."


def invoke_with_cache(llm, prompt, cache):
    if cache_response := cache.lookup(prompt, ""):
        print("Usando cache!")
        return cache_response
    response = llm(prompt, max_tokens=100)
    cache.update(prompt, response, "")
    return response


respose1 = invoke_with_cache(openai, prompt, cache)
response_text = respose1.replace("\n", " ")
print("Primeira Chamada (API chamada):", response_text)


response2 = invoke_with_cache(openai, prompt, cache)
response_text = response2.replace("\n", " ")
print("Segunda Chamada (usando cache):", response_text)
