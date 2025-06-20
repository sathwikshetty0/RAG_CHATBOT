# 📚 Clap AI – Student Chatbot using LangChain, Ollama & Flask

Clap AI is an intelligent educational assistant designed for students. It uses Retrieval-Augmented Generation (RAG) powered by **LangChain**, **Ollama**, and **ChromaDB** to answer student questions using course material (PDFs).

---

## 🚀 Features

* 💬 Chatbot for student learning
* 🔍 RAG-based answers from uploaded PDFs
* 🧠 Local LLM with Ollama (e.g., LLaMA3)
* 🗂️ PDF ingestion into Chroma vector DB
* 🖥️ Flask API for interaction

---

## 🛠️ Installation

### 1. Clone the Repo

```bash
git clone https://github.com/sathwikshetty0/RAG_CHATBOT.git
cd RAG_CHATBOT
```

---

### 2. Set up Python Virtual Environment

```bash
python3 -m venv .chatbot
source .chatbot/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure you also install:

```bash
pip install langchain-ollama langchain-community
```

---

### 4. Install & Start Ollama

Install [Ollama](https://ollama.com/download) and pull the embedding + chat models:

```bash
ollama pull nomic-embed-text
ollama pull llama3
```

---

### 5. Populate Chroma Vector DB with PDFs

Put your study PDFs in a folder like `./pdfs/` and run:

```bash
python populate_database.py --reset
```

---
