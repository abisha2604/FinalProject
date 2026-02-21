import streamlit as st
import requests

st.title("🛒 Hyper-Personalized E-Commerce Assistant")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.chat_input("Ask your question")

if query:
    with st.spinner("Thinking..."):
        response = requests.post("http://127.0.0.1:8000/chat",json={"query": query})

        if response.status_code == 200:
            answer = response.json()

            st.session_state.history.append({
                "user": query,
                "bot": answer
            })
        else:
            st.error("Something went wrong")

for chat in st.session_state.history:
    st.write("👤 You:", chat["user"])
    st.write("🧠 Assistant:", chat["bot"])


with st.sidebar:

    if st.button("Load History", use_container_width=True):
        history_response = requests.get("http://127.0.0.1:8000/history")

        if history_response.status_code == 200:
            data = history_response.json()

            st.session_state.history = []

            if not data:
                st.info("📭 No chat history available")
            else:
                for h in data:
                    st.session_state.history.append({
                        "user": h.get("user_question", ""),
                        "bot": h.get("llm_reply", "")
                    })
        else:
            st.error("Failed to load history")

    
    if st.button("Clear History",use_container_width=True):

        if not st.session_state.history:
            st.info("📭 No history available")
        else:
            delete_response = requests.delete("http://127.0.0.1:8000/delete-history")

            if delete_response.status_code == 200:
                st.session_state.history = []
                st.success("History cleared")
            else:
                st.error("Failed to delete history")

