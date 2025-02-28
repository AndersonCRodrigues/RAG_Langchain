import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

googleai = ChatGoogleGenerativeAI(
    google_api_key=GOOGLE_API_KEY,
    model="gemini-2.0-flash-lite",
)

template = """
Você é um analista financeiro.
Escreva um relatório financeiro detalhado para a
empresa "{empresa}" para o período {periodo}.

O relatório deve ser escrito em {idioma} e incluir as seguintes análises:
{analises}

Certifique-se de fornecer insights e conclusões para cada seção.
"""

prompt_template = PromptTemplate.from_template(template)

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
analises_text = "\n".join(f"- {analise}" for analise in analises)

prompt = prompt_template.format(
    empresa=empresa,
    periodo=periodo,
    idioma=idioma,
    analises=analises_text,
)

response = googleai.invoke(prompt)
print("Relatório Financeiro:\n", response.content)
