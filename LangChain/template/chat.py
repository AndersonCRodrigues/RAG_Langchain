import os
from langchain_openai import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
openai = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-3.5-turbo",
    max_tokens=500,
)

# equivalência aos roles: system: system, Human: user, AI: assistant
chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "Você deve estruturar suas respostas de acordo com o método de "
                "análise de negócios, garantindo clareza e concisão."
            )
        ),
        HumanMessagePromptTemplate.from_template(
            (
                "Por favor, gere um relatório detalhado sobre a indústria de "
                'tecnologia na região "{regiao}".'
            )
        ),
        AIMessage(
            content=(
                "Claro, vou começar coletando informações sobre a região "
                "e analisando os dados disponíveis."
            )
        ),
        HumanMessage(
            content=(
                "Certifique-se de incluir uma análise SWOT e uma previsão de "
                "crescimento para os próximos 5 anos."
            )
        ),
        AIMessage(content="Entendido. Aqui está o relatório completo:"),
    ]
)

prompt_gerado = chat_template.format(regiao="Améria Latina")
response = openai.invoke(prompt_gerado)
print("Saída do LLM:\n", response.content)
