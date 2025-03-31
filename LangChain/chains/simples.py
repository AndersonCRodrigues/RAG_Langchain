import os
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
openai = OpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-3.5-turbo-instruct",
    max_tokens=500,
    temperature=0,
)

prompt_template = PromptTemplate.from_template(
    "Descreva as tendências tecnológicas em {ano}."
)

runnable_sequence = prompt_template | openai
output = runnable_sequence.invoke({"ano": "2024"})
print("Output:\n", output)
