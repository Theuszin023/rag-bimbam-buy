# RAG BimBam Buy

Assistente de perguntas e respostas baseado em RAG (Retrieval-Augmented Generation), construído sobre o documento de FAQ de métodos de pagamento da BimBam Buy. O sistema busca os trechos mais relevantes do documento e usa um modelo de linguagem para gerar respostas contextualizadas, em vez de depender apenas do conhecimento geral do modelo.

## Como funciona

1. O PDF do FAQ é carregado e dividido em pedaços menores (chunks).
2. Cada chunk é transformado em um vetor numérico (embedding) que representa seu significado semântico.
3. Os vetores são armazenados em um banco de dados vetorial (ChromaDB).
4. Quando o usuário faz uma pergunta, o sistema busca os chunks mais parecidos semanticamente com a pergunta.
5. Esses chunks são enviados como contexto para o modelo de linguagem (Gemini), que gera uma resposta baseada apenas nessas informações.
6. Uma interface de chat (Gradio) permite conversar com o assistente pelo navegador.

## Tecnologias utilizadas

- **LangChain** — orquestração do pipeline de RAG
- **Google Gemini** (`gemini-3.6-flash`) — geração das respostas
- **Google Generative AI Embeddings** (`gemini-embedding-001`) — geração dos vetores semânticos
- **ChromaDB** — banco de dados vetorial
- **Gradio** — interface web de chat
- **PyPDF** — leitura do documento PDF

## Como rodar

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/rag-bimbam-buy.git
cd rag-bimbam-buy
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure sua API key do Google

Este projeto usa a API do Google Gemini. Você precisa de uma chave gratuita, obtida em [Google AI Studio](https://aistudio.google.com/apikey).

Configure a variável de ambiente `GOOGLE_API_KEY` antes de rodar:

```bash
export GOOGLE_API_KEY="sua_chave_aqui"
```

No Google Colab, use o recurso de **Secrets** (ícone de chave 🔑 no menu lateral) em vez de colar a chave diretamente no código.

### 4. Adicione o documento PDF

Coloque o arquivo PDF do FAQ na pasta do projeto (ou ajuste o caminho no notebook para apontar para o local correto).

### 5. Execute o notebook

Abra o arquivo `.ipynb` no Jupyter, Colab ou VS Code e execute as células em ordem. Ao final, uma interface Gradio será iniciada, com um link local e um link público temporário.

## Estrutura do projeto

```
rag-bimbam-buy/
├── README.md
├── requirements.txt
├── .gitignore
└── notebook.ipynb
```

## Aviso de segurança

Nunca cole sua API key diretamente no código ou no notebook. Use sempre variáveis de ambiente ou o gerenciador de secrets da plataforma que você estiver usando (Colab, GitHub Actions, etc.). O arquivo `.gitignore` deste projeto já está configurado para evitar o envio acidental de arquivos `.env` e chaves sensíveis ao repositório.

## Próximos passos

- [ ] Implantação em produção (OCI)
- [ ] Melhorias na interface de usuário
- [ ] Suporte a múltiplos documentos
