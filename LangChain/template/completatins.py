import os
from langchain_openai import OpenAI
from langchain.prompts import (
    PromptTemplate,
)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
openai = OpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-3.5-turbo-instruct",
    max_tokens=500,
)

template = """
Você é um analista financeiro.
Escreva um relatório financeiro detalhado para a empresa "{empresa}"
para o período {periodo}.

O relatório deve ser escrito em {idioma} e incluir as seguintes análises:
{analises}

Certifique-se de fornecer insights e conclusões para cada seção.
"""

prompt_tempate = PromptTemplate.from_template(template=template)
empresa = "ACME Corp"
periodo = "Q1 2024"
idioma = "Português"
analises = [
    "Análise do Balanço Patrimonial",
    "Análise do Fluxo de Caixa",
    "Análise de Tendências",
    "Análise de Receita e Lucro",
    "Análise de Posição de Mercado",
]
analises_text = "\n".join([f"- {analise}" for analise in analises])
print(analises_text)

prompt = prompt_tempate.format(
    empresa=empresa, periodo=periodo, idioma=idioma, analises=analises_text
)

print("Prompt Gerado:\n", prompt)
response = openai.invoke(prompt)
print("Saída do LLM:\n", response)
