import os
from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_python_agent
from langchain_community.utilities import SerpAPIWrapper
from langchain.prompts import PromptTemplate
from langchain.tools import Tool

SERP_API_KEY = os.getenv("SERP_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
openai = OpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-3.5-turbo-instruct",
    max_tokens=500,
    temperature=0,
)

serp_search = Tool(
    name="SerpAPI",
    func=SerpAPIWrapper(serpapi_api_key=SERP_API_KEY).run,
    description="Busca informações na web usando a SerpAPI",
)

agent_executor = create_python_agent(
    llm=openai,
    tool=serp_search,
    verbose=True,
)

prompt_template = PromptTemplate(
    input_variables=["query"],
    template="""
        Pesquise na web sobre {query}
        e forneça um resumo abrangente,
        em portugês, sobre o assunto.
    """,
)

query = "Carl Sagan"
prompt = prompt_template.format(query=query)

print(prompt)

response = agent_executor.invoke(prompt)

print("Entrada do agente:", response["input"])

print("Saída do agente:", response["output"])
