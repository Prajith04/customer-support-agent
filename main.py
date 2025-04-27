# main.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()
from gliner import GLiNER
from groq import Groq
from vectordb_utils import search_vectordb, init_qdrant_collection,populate_vectordb_from_hf
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load models
cache_dir = os.environ.get("MODEL_CACHE_DIR", "/app/cache")  # Fallback to /app/cache
os.makedirs(cache_dir, exist_ok=True)
gliner_model = GLiNER.from_pretrained("urchade/gliner_medium-v2.1",cache_dir=cache_dir)
groq_client = Groq(api_key=GROQ_API_KEY)
chat_memory=[]

def extract_entities(text):
    # Tokenize the input text first
    labels = ["PRODUCT", "ISSUE", "PROBLEM", "SERVICE"]
    
    # Predict entities
    return gliner_model.predict_entities(text, labels)

def validate_answer(user_query, retrieved_answer):
    prompt = f"""
You are a validator assistant.

Given the user query and the answer retrieved from a knowledge base, decide if the answer is relevant and correctly addresses the query.

Respond ONLY with:
- "YES" if the answer is appropriate.
- "NO" if the answer is unrelated, inaccurate, or insufficient.

User Query:
{user_query}

Retrieved Answer:
{retrieved_answer}

Is the answer appropriate?
"""
    completion = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0, max_completion_tokens=10, top_p=1
    )
    return completion.choices[0].message.content.strip()

def generate_response(user_query, validated_answer):
    prompt = f"""
You are a customer support agent.

Using the following validated support answer, respond helpfully and politely to the user's query.
warning: there should not be [],<> tags in the response

User Query:
{user_query}

Support Answer:
{validated_answer}

Compose your response:
"""
    completion = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8, max_completion_tokens=1000, top_p=1
    )
    return completion.choices[0].message.content.strip()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "chat_history": []})

@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):
    entities = extract_entities(message)
    entity_info = [(e['text'], e['label']) for e in entities]

    results = search_vectordb(message)
    if not results:
        bot_reply = "Sorry, I couldn't find anything helpful."
    else:
        answer = results[0].payload["response"]
        if validate_answer(message, answer) == "YES":
            bot_reply = generate_response(message, answer)
        else:
            bot_reply = "Sorry, I couldn't find a suitable answer. Please contact support."
    chat_memory.append({"sender": "User", "message": message})
    chat_memory.append({"sender": "Bot", "message": bot_reply})

    return templates.TemplateResponse("chat.html", {
        "request": request,
        "chat_history": chat_memory,
        "entities": entity_info
    })
