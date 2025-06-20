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

## 📁 Project Structure

```bash
├── data/(files pdf)
├── app.py                     # Teacher chatbot with SMTP support
├── studentapp.py              # Student chatbot (no SMTP/email logic)
├── populate_database.py       # Script to ingest PDFs into Chroma vector database
├── get_embedding_function.py  # Common embedding function used by both versions
├── requirements.txt           # Python dependencies
├── .env                       # SMTP credentials and config (only for teacher version)
└── chroma/                    # Persisted Chroma vector store (auto-generated)
```

## 👩‍🏫 Teacher vs 🎓 Student

* `app.py` is designed for teachers and supports a **contact form via email** (SMTP setup required).
* `studentapp.py` is simplified for student use — **no email/contact support is included**.

## ✉️ SMTP Support (Teacher Only)

To enable support requests from the chatbot, add a `.env` file:

```env
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SUPPORT_EMAIL=recipient_email@gmail.com
```

> ⚠️ Not required for `studentapp.py`

## 🧠 Embeddings & Model

* Embeddings by `nomic-embed-text` (Ollama)
* LLM powered by `llama3` (Ollama)
* Vector search using `Chroma`

## ✨ Technologies Used

* **Flask** for API
* **LangChain** for prompt handling and chaining
* **Ollama** for local LLM execution
* **ChromaDB** as vector store
* **PDF parsing** via `PyMuPDF`, `pdfminer.six`, or `pypdf`

