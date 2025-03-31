import os
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.document_loaders import TextLoader

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
openai = OpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-3.5-turbo-instruct",
    max_tokens=500,
    temperature=0,
)

loader = TextLoader("base_conhecimento_britadeira.txt")
documents = loader.load()
historico_conversas = """
    Cliente: Minha britadeira não liga. Chatbot: Você já verificou
    se a bateria está carregada e conectada corretamente?
    """
pergunta = (
    "Minha britadeira não liga. Eu já verifiquei e a bateria está "
    "carregada e conectada corretamente"
)

inputs = {
    "context": "\n".join(doc.page_content for doc in documents),
    "question": pergunta,
    "historico": historico_conversas,
}

prompt_base_conhecimento = PromptTemplate(
    input_variables=["context", "question"],
    template="""Use o seguinte contexto para responder à pergunta.
    Responda apenas com base nas informações fornecidas.
    Não forneceça instruções de procedimento já realizados.
    Não utilize informações externas ao contexto:
    Contexto: {context}
    Pergunta: {question}""",
)

prompt_historico_conversas = PromptTemplate(
    input_variables=["historico", "question"],
    template="""Use o histórico de conversas para responder à pergunta.
    Responda apenas com base nas informações fornecidas.
    Não forneceça instruções de procedimento já realizados.
    Não utilize informações externas ao contexto:
    Histórico: {historico}
    Pergunta: {question}""",
)

prompt_final = PromptTemplate(
    input_variables=[
        "resposta_base_conhecimento",
        "resposta_historico_conversas",
    ],
    template="""Combine as seguintes respostas para gerar uma resposta final,
    mas não forneça instruções de procedimentos já realizados:
    Resposta da base de conhecimento: {resposta_base_conhecimento}
    Resposta do histórico de conversas: {resposta_historico_conversas}""",
)

chain_base_conhecimento = prompt_base_conhecimento | openai
chain_historico_conversas = prompt_historico_conversas | openai
chain_final = prompt_final | openai

print(chain_base_conhecimento)
print(chain_historico_conversas)

resultado_base_conhecimento = chain_base_conhecimento.invoke(
    {"context": inputs["context"], "question": inputs["question"]}
)
resultado_historico_conversas = chain_historico_conversas.invoke(
    {"historico": inputs["historico"], "question": inputs["question"]}
)
resultado_final = chain_final.invoke(
    {
        "resposta_base_conhecimento": resultado_base_conhecimento,
        "resposta_historico_conversas": resultado_historico_conversas,
    }
)

print("Resultado base de conhecimento:\n", resultado_base_conhecimento)
print("----")
print("Resultado histórico de conversas:\n", resultado_historico_conversas)
print("----")
print("Resultado final:\n", resultado_final)
print("----")
