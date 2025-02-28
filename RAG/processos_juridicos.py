import os  # Importa o módulo OS para manipulação de variáveis de ambiente e diretórios
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)  # Divide textos grandes em partes menores
from langchain.document_loaders import PyMuPDFLoader  # Carrega documentos PDF
from langchain_openai import OpenAIEmbeddings  # Gera embeddings com OpenAI
from langchain_community.vectorstores import (
    Pinecone as PineconeVectorStore,
)  # Interface com Pinecone para armazenamento vetorial
from langchain.chains import RetrievalQA  # Implementa cadeia de perguntas e respostas
from langchain_openai import ChatOpenAI  # Utiliza modelos da OpenAI para chat
from pinecone import Pinecone  # Cliente da Pinecone para manipulação de vetores
import zipfile  # Manipula arquivos ZIP

# Obtém as chaves da API a partir das variáveis de ambiente
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Inicializa o cliente da Pinecone
pinecone_client = Pinecone(api_key=PINECONE_API_KEY)

# Configura o modelo de linguagem da OpenAI
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model_name="gpt-3.5-turbo",
    temperature=0,  # Mantém respostas determinísticas
)

# Define os caminhos do arquivo ZIP e da pasta onde será extraído
zip_file_path = "documentos.zip"
extracted_folder_path = "docs"

# Extrai os arquivos do ZIP para a pasta especificada
with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
    zip_ref.extractall(extracted_folder_path)

# Lista para armazenar os documentos extraídos
documents = []
for filename in os.listdir(extracted_folder_path):
    if filename.endswith(".pdf"):  # Filtra apenas arquivos PDF
        file_path = os.path.join(extracted_folder_path, filename)
        loader = PyMuPDFLoader(file_path)  # Carrega o PDF
        documents.extend(loader.load())  # Adiciona o conteúdo à lista

# Divide os documentos em partes menores para facilitar a indexação
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Tamanho dos fragmentos
    chunk_overlap=100,  # Sobreposição entre fragmentos para manter contexto
    length_function=len,  # Função de cálculo do comprimento
)
chunks = text_splitter.create_documents(
    [doc.page_content for doc in documents],  # Extrai o texto dos documentos
)

# Cria embeddings dos textos usando o modelo da OpenAI
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# Nome do índice no Pinecone
index_name = "llm"

# Armazena os fragmentos no Pinecone para recuperação futura
vector_store = PineconeVectorStore.from_documents(
    chunks, embeddings, index_name=index_name
)

# Definição de perguntas para a IA responder com base nos documentos indexados
query_1 = (
    "Responda apenas com base no input fornecido. Qual o número do processo"
    " que trata de Violação de normas ambientais pela Empresa de Construção?"
)
query_2 = (
    "Responda apenas com base no input fornecido."
    " Qual foi a decisão no caso de fraude financeira?"
)
query_3 = (
    "Responda apenas com base no input fornecido."
    " Quais foram as alegações no caso de negligência médica?"
)
query_4 = (
    "Responda apenas com base no input fornecido."
    " Quais foram as alegações no caso de Número do Processo: 822162"
)
query_5 = (
    "Responda apenas com base no input fornecido. "
    " Qual foi a resolução no caso de Número do Processo: 822162?"
)

# Configura o mecanismo de recuperação de informações baseado em similaridade
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},  # Recupera os 3 documentos mais similares
)

# Cria a cadeia de perguntas e respostas baseada no modelo da OpenAI
chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # Estratégia de junção das respostas
    retriever=retriever,  # Utiliza o retriever configurado
)

# Imprime a configuração da cadeia de QA
print(chain)

# Obtém as respostas do modelo para as perguntas definidas
answer_1 = chain.invoke(query_1)
answer_2 = chain.invoke(query_2)
answer_3 = chain.invoke(query_3)
answer_4 = chain.invoke(query_4)
answer_5 = chain.invoke(query_5)

# Exibe as perguntas e respostas obtidas
print("Pergunta: ", answer_1["query"])
print("Resultado: ", answer_1["result"], "\n")
# ---
print("Pergunta: ", answer_2["query"])
print("Resultado: ", answer_2["result"], "\n")
# ---
print("Pergunta: ", answer_3["query"])
print("Resultado: ", answer_3["result"], "\n")
# ---
print("Pergunta: ", answer_4["query"])
print("Resultado: ", answer_4["result"], "\n")
# ---
print("Pergunta: ", answer_5["query"])
print("Resultado: ", answer_5["result"], "\n")
