import os
from langchain.prompts import PromptTemplate
from langchain import hub
from langchain.agents import (
    Tool,
    AgentExecutor,
    create_react_agent,
)
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SerpAPIWrapper


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SERP_API_KEY = os.getenv("SERP_API_KEY")

openai = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-3.5-turbo",
    temperature=0,
)

prompt = """
Como assistente financeiro pessoal,
ajude a responder as seguintes perguntas com ajuda da internet.
Perguntas: {q}
"""

prompt_template = PromptTemplate.from_template(prompt)
print(prompt_template)

react_instructions = hub.pull("hwchase17/react")
print(react_instructions)

python_repl = PythonREPLTool()
python_repl_tool = Tool(
    name="Python REPL",
    func=python_repl.run,
    description="""
    Qualquer tipo de cálculo deve usar esta ferramenta.
    Você não deve realizar o cálculo diretamente.
    Você deve inserir código Python.
    """,
)

serp_search = Tool(
    name="SerpAPI",
    func=SerpAPIWrapper(serpapi_api_key=SERP_API_KEY).run,
    description="""
    Útil para encontrar informações e dicas de economia
    e opções de investimento.
    Você sempre deve pesquisar na internet
    as melhores dicas usando esta ferramenta, não
    responda diretamente.
    Sua resposta deve informar que há elementos pesquisados na internet
    """,
)

tools = [python_repl_tool, serp_search]
agent = create_react_agent(openai, tools, react_instructions)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10,
)

print(agent_executor)

question1 = """
Eu ganho R$4000 por mês mas o total de minhas despesas
é de R$3800 mais 500 de aluguel.
Como posso ajustar meu orçamento para economizar dinheiro?
"""

question2 = """
Minha renda é de R$6000 por mês,
o total de minhas despesas é de R$2500 mais 1000 de aluguel.
Quais dicas de investimento você me dá?
"""

output = agent_executor.invoke(
    {"input": prompt_template.format(q=question1)},
)

print(output["input"])
print(output["output"])

output = agent_executor.invoke(
    {"input": prompt_template.format(q=question2)},
)

print(output["input"])
print(output["output"])
