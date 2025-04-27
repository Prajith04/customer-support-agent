---
title: cutomer support
---
# 🧠 Customer Support Chatbot (FastAPI + Hugging Face + Qdrant)

This is an intelligent, conversational customer support chatbot built using:

- 🔍 **GLiNER** for named entity extraction  
- 🧠 **SentenceTransformers** + **Qdrant** for semantic search and retrieval  
- 🤖 **Groq LLM** for answer validation and response generation  
- ⚡ **FastAPI** for the web backend  
- 🖼️ **Jinja2 templates** for a simple frontend chat UI

It runs both locally and on **Hugging Face Spaces via Docker**.

---

## 🚀 Features

- Extracts key entities from support requests
- Semantic similarity search with Qdrant + SentenceTransformers
- LLM validation of results via Groq API
- Fully functional FastAPI-based web interface
- Docker-ready for Hugging Face Spaces deployment

---

## 📦 Installation

### Local Setup

```bash
git clone https://github.com/your-username/support-chatbot
cd support-chatbot

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload