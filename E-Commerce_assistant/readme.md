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

## 🔎 API Endpoints

Defined in: `routes/product_routes.py`

### 📌 POST `/chat`
- Accepts user query
- Retrieves relevant products using RAG
- Generates LLM-powered recommendation
- Returns AI-generated response

### 📌 GET `/history`
- Returns complete chat history from database

### 📌 DELETE `/delete-history`
- Deletes all stored chat records

---

## 🧠 RAG Pipeline Flow

Implemented in: `services/rag_service.py`

### 🚀 Processing Steps

1. Load product catalog from CSV files
2. Convert product data into embeddings using **SentenceTransformer**
3. Store embeddings in **FAISS vector index**
4. Retrieve top relevant products based on query similarity
5. Re-rank retrieved results using **CrossEncoder**
6. Fetch recent conversation memory from database
7. Generate final context-aware response using **Groq LLM (Llama 3.3 70B)**

---

## 🗄️ Database

- Chat history stored using **SQLAlchemy ORM**
- Schema defined in: `models/schema.py`
- Chat memory builder logic implemented in: `services/data_service.py`
- Database used: **SQLite**

---

## 📦 Request Model

Defined using **Pydantic** in: `models/pydantic.py`

### Example Request Body

```json
{
  "query": "Suggest laptops under ₹40000"
}
```

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

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/abisha2604/FinalProject.git
cd E-Commerce_assistant
```

---

## 2️⃣ Run Without Docker

### 🔹 Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend will run at:
- http://127.0.0.1:8000

---

### 🔹 Frontend Setup

Open a new terminal and run:

```bash
cd frontend
streamlit run app.py
```

Frontend will run at:
- http://localhost:8501

---

## 3️⃣ Run With Docker

Make sure Docker is installed, then run:

```bash
docker compose up --build
```

🚀 Key Highlights:

* Implemented end-to-end RAG pipeline

* Built FAISS vector search system

* Integrated Groq LLM (Llama 3.3 70B)

* Added conversational memory using database

* Implemented CrossEncoder re-ranking

* Dockerized full-stack application


👩‍💻 Author

S. Abisha

Aspiring GenAI Developer
