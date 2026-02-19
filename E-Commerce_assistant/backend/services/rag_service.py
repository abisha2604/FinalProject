from groq import Groq
from sqlalchemy.orm import Session
from sqlalchemy import text
import re
from sentence_transformers import SentenceTransformer, CrossEncoder
import faiss
import numpy as np
import os
from services.data_service import build_memory
from sqlalchemy.orm import Session


API_KEY = " " 

client = Groq(api_key = API_KEY)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

rerank_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def load_chunks(text,source,chunk_size=200):
    chunks = []
    start = 0
    while start < len(text) :
        end = start + chunk_size
        chunk_text = text[start:end]
        chunks.append({
            "text": chunk_text,
            "source": source,
        })
        start = end
    return chunks

import pandas as pd

def load_csv_folder(folder_path):
    all_chunks = []
    folders = os.listdir(folder_path)
    for file in folders:
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            df = pd.read_csv(file_path)

            for _, row in df.iterrows():
                chunk_text = (
                f"Category:{row['category']} | "
                f"Product:{row['product_name']} | "
                f"Price:{row['price']} | "
                f"Rating:{row['rating']} | "
                f"Description:{row['description']} | ")
                all_chunks.append({
                    "text": chunk_text,
                    "product_url": row["product_url"],
                    "source": file
                })

    return all_chunks

def embedding(chunk):
    embedded_value = embed_model.encode(chunk)
    if len(embedded_value.shape)==1:
        embedded_value = embedded_value.reshape(1,-1)
    return embedded_value

def create_index(embedded_data):
    dim = embedded_data.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embedded_data))
    return index
   
def search(chunks, query, index, top_k=10):
    query_embed = embed_model.encode([query])
    if len(query_embed.shape)==1:
        query_embed = query_embed.reshape(1,-1)
    distance, indices = index.search(np.array(query_embed),top_k)
    result = []
    for i in indices[0]:
        result.append(chunks[i])
    return result
 
def rerank(query,chunks):
    pairs = []
    for chunk in chunks:
        pairs.append([query,chunk['text']])
    
    scores = rerank_model.predict(pairs)
    score_ranked = list(zip(chunks,scores)) 
    score_ranked.sort(key=lambda x:x[1],reverse=True)
    output = []
    for item in score_ranked:
        output.append(item[0])
    return output
    
def response(db:Session, query, context):
    context_data = ""
    for data in context:
        context_data += data['text'] + "\n"
        context_data = context_data + data['product_url'] +"\n"
        context_data = context_data + data["source"] + "\n\n"


    memory = build_memory(db)

    prompt = f"""
       You are a friendly, professional e-commerce sales assistant.

        Rules:
        - Answer only what the user asks.
        - Maintain the same product Category across follow-ups which is in the Product context.
        - Change Category only if the user explicitly asks.
        - If user says "other brand", "other option", "show more":Use Conversation 
          history to identify what the product is. 
        - If no additional products are available in that category, reply exactly:
          "No other products found in the category".
        - If the user greets, ask what product they want.
        - Use conversation history silently; never mention it.
        - When multiple products are shown, always identify ONE as:
          "Best option" and explain the reason briefly.


        Data rules:
        - Use only the provided product context.
        - Do not use outside knowledge or hallucinate.
        - If information is missing, reply exactly:
          "Answer not available in the provided context".

        Recommendation logic:
        - Recommend  products in a salesperson tone.
        - Explain why each product is recommended.
        - Reasons must come only from price, rating, and user query.
        - Do NOT repeat the same reason across products.
        - Do NOT mention product IDs.
        - Include the purchase link.

        Output format:

        <Product Name>
        Price: ₹<price>
        Rating:⭐<rating>
        Why recommended:
        - Price-based reason
        - Rating-based reason
        - User-intent-based reason
        Buy link: <purchase_link>

        Conversation history:
        {memory}

        Product context:
        {context_data}

        User question:
        {query}"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
        {
            "role": "user",
            "content": prompt
        }
        ]
    )
    return completion.choices[0].message.content

def filter_by_category(results, category):
    filtered = []
    for r in results:
        if f"Category:{category}" in r["text"]:
            filtered.append(r)
    return filtered



def pipeline(db:Session, query):
    chunks = load_csv_folder("docs")
    text = []
    for chunk in chunks:
        text.append(chunk['text'])
    embed = embedding(text)
    index = create_index(embed)
    search_data = search(chunks, query, index)
    rerank_data = rerank(query,search_data)
    final_output = rerank_data[:2]
    output = response(db, query, final_output)
    return(output)


