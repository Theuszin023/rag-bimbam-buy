__import__("pysqlite3")
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import os
import gradio as gr
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate

# A chave é lida da variável de ambiente GOOGLE_API_KEY.
if not os.environ.get("GOOGLE_API_KEY"):
    raise ValueError(
        "GOOGLE_API_KEY não encontrada. Configure-a como variável de ambiente antes de rodar."
    )

# --- 1. Carregar o PDF e dividir em chunks ---
NOME_DO_PDF = "perguntas_frequentes.pdf"

loader = PyPDFLoader(NOME_DO_PDF)
documentos = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documentos)

# --- 2. Criar embeddings e o ChromaDB ---
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="/tmp/chroma_db"
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# --- 3. Conectar o Gemini (modelo de chat) ---
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0.3
)

prompt = ChatPromptTemplate.from_template("""
Você é um assistente que responde perguntas com base no contexto fornecido.
Use apenas as informações do contexto abaixo para responder. Se não souber a resposta
com base no contexto, diga que não encontrou essa informação no documento.

Contexto:
{context}

Pergunta: {input}

Resposta:
""")


def formatar_contexto(documentos):
    return "\n\n".join(doc.page_content for doc in documentos)


def fazer_pergunta(pergunta):
    documentos_relevantes = retriever.invoke(pergunta)
    contexto = formatar_contexto(documentos_relevantes)

    prompt_formatado = prompt.format(context=contexto, input=pergunta)
    resposta = llm.invoke(prompt_formatado)

    if isinstance(resposta.content, str):
        texto_resposta = resposta.content
    else:
        texto_resposta = "".join(
            bloco.get("text", "")
            for bloco in resposta.content
            if isinstance(bloco, dict) and bloco.get("type") == "text"
        )

    return texto_resposta


# --- 4. Interface Gradio ---
def responder_chat(mensagem, historico):
    return fazer_pergunta(mensagem)


interface = gr.ChatInterface(
    fn=responder_chat,
    title="Assistente BimBam Buy",
    description="Tire suas dúvidas sobre métodos de pagamento, reembolsos e mais, com base no documento oficial.",
    examples=[
        "Quais métodos de pagamento estão disponíveis?",
        "Como funciona o reembolso?",
        "É possível parcelar a compra?",
    ],
)

if __name__ == "__main__":
    interface.launch(server_name="0.0.0.0", server_port=7860)