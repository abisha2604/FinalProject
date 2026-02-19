🛒 Hyper-Personalized E-Commerce Assistant

An AI-powered conversational shopping assistant built using FastAPI, RAG (Retrieval-Augmented Generation), LLMs, SQLAlchemy, and Streamlit.

This system enhances traditional e-commerce by providing intelligent, context-aware, and personalized product recommendations through natural language interaction.

📌 Problem

Generic e-commerce platforms provide static recommendations, leading to low personalization and reduced user engagement.

💡 Solution:

* A Conversational AI Assistant that

* Understands natural language queries

* Retrieves relevant products using RAG

* Re-ranks results using CrossEncoder

* Uses Groq LLM (Llama 3.3 70B) for intelligent recommendations

* Maintains short-term conversation memory

* Stores chat history in database

🏗️ System Architecture:

```bash
User → Streamlit UI
        ↓
FastAPI Backend
        ↓
RAG Pipeline
   ├── SentenceTransformer (Embeddings)
   ├── FAISS (Vector Search)
   ├── CrossEncoder (Re-ranking)
   └── Groq LLM (Response Generation)
        ↓
SQLite (Chat History)
```

📂 Project Structure:

```bash
E-Commerce_assistant/
│
├── backend/
│   ├── main.py
│   │
│   ├── routes/
│   │   └── product_routes.py
│   │
│   ├── services/
│   │   ├── rag_service.py
│   │   └── data_service.py
│   │
│   ├── models/
│   │   ├── pydantic.py
│   │   └── schema.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   └── get_db.py
│   │
│   ├── docs/
│   │   ├── products-1.csv
│   │   ├── products-2.csv
│   │   └── products-3.csv
│   │
│   ├── requirements.txt
│   └── Dockerfile
│   
│
├── frontend/
│   └── app.py
│
└── docker-compose.yml 
```

🔎 API Endpoints:

Defined in: product_routes

POST /chat

* Handles user query and returns LLM-generated recommendation.

GET /history

* Returns all previous chat history.

DELETE /delete-history

* Deletes all chat records.

🧠 RAG Pipeline Flow

Implemented in: rag_service

🚀Steps:

* Load product catalog from CSV folder

* Convert products into embeddings (SentenceTransformer)

* Store embeddings in FAISS index

* Retrieve top relevant products

* Re-rank using CrossEncoder

* Add conversation memory from database

* Generate final response using Groq LLM

🗄️ Database:

Chat history stored using SQLAlchemy.

Schema defined in  : schema

Chat memory builder: data_service

📦 Request Model:

Defined using Pydantic: pydantic

{
  "query": "Suggest laptops under ₹40000"
}


## 🛠️ Tech Stack

| Layer            | Technology                               |
|------------------|------------------------------------------|
| Backend          | FastAPI                                  |
| Vector Search    | FAISS                                    |
| Embeddings       | all-MiniLM-L6-v2                         |
| Re-ranking       | cross-encoder/ms-marco-MiniLM-L-6-v2     |
| LLM              | Groq (Llama 3.3 70B)                     |
| Database         | SQLite                                   |
| ORM              | SQLAlchemy                               |
| Frontend         | Streamlit                                |
| Containerization | Docker                                   |


⚙️ Installation:

1️⃣ Clone Project:

git clone <repo-url>
cd project

2️⃣ Run Without Docker:

Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Frontend
cd frontend
streamlit run app.py

3️⃣ Run With Docker:

docker compose up --build


🚀 Key Highlights:

Implemented end-to-end RAG pipeline

Built FAISS vector search system

Integrated Groq LLM (Llama 3.3 70B)

Added conversational memory using database

Implemented CrossEncoder re-ranking

Dockerized full-stack application


👩‍💻 Author

S. Abisha
Aspiring GenAI Developer
