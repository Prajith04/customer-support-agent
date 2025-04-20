 🧠 Customer Support Chatbot (FastAPI + Hugging Face + Qdrant)

[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20HuggingFace-Demo-blueviolet?logo=huggingface&logoColor=white)](https://huggingface.co/spaces/Prajith04/customer-support)
 
This is an intelligent, conversational customer support chatbot built using:

- 🔍 **GLiNER** for named entity extraction
- 🧠 **SentenceTransformers** + **Qdrant** for semantic search and retrieval
- 🤖 **Groq LLM** for answer validation and response generation
- ⚡ **FastAPI** for the web backend
- 🖼️ **Jinja2 templates** for a simple frontend chat UI

It runs both locally and on **Hugging Face Spaces via Docker**.

---

## 🚀 Features

- Extracts entities from support queries using GLiNER
- Searches a semantic knowledge base using Qdrant (with sentence-transformers)
- Validates responses using a Groq LLM
- Provides accurate, polite replies using contextual response generation
- Includes a clean HTML frontend (template-based)

---

## To Do List

- [ ] Add Agent Support
- [ ] Add sentiment analysis
      
---

## 📦 Installation

### 🔧 Requirements

- Python 3.10+
- Groq API key (set as `GROQ_API_KEY` in your `.env` or Hugging Face secrets)

### 🔨 Local Setup

```bash
# Clone the repo
git clone https://github.com/your-username/support-chatbot
cd support-chatbot

# Create virtualenv
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --reload
