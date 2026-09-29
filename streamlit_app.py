"""Streamlit demo using exactly the same chat engine as the terminal."""
import os

import streamlit as st

from app import answer_question

st.set_page_config(page_title="Speedlink CRM Assistant", page_icon="💬")
st.title("Speedlink CRM Assistant")
st.caption("Workspace · Internet · Training · Pearson VUE · Research support")

def setting(name, default=""):
    return os.getenv(name) or (str(st.secrets[name]) if name in st.secrets else default)

# Accessing absent secrets can raise even when testing without a secrets file.
try:
    api_key = setting("GROQ_API_KEY")
    model = setting("GROQ_MODEL", "openai/gpt-oss-120b")
except FileNotFoundError:
    api_key = os.getenv("GROQ_API_KEY", "")
    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Try the assistant")
    st.write("Ask about a service, then ask a follow-up such as “How much?”")
    show_sources = st.checkbox("Show supporting information", value=False)
    if st.button("Start a new conversation"):
        st.session_state.messages = []
        st.rerun()
    st.caption("Coverage, payments and bookings require confirmation by the Speedlink team.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if show_sources and message.get("sources"):
            with st.expander("Supporting information"):
                for source in message["sources"]:
                    st.markdown(source)
        if message.get("warning"):
            st.warning(message["warning"])

if not api_key:
    st.info("To enable chat, add GROQ_API_KEY to your local .env file or Streamlit app secrets.")

if question := st.chat_input("How can Speedlink help you?", disabled=not bool(api_key), max_chars=4000):
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        try:
            with st.spinner("Checking Speedlink's information…"):
                answer, result = answer_question(
                    question, st.session_state.messages, api_key=api_key, model=model
                )
        except Exception as exc:
            st.error(f"Unable to get a response ({type(exc).__name__}). Please try again. "
                     "If it persists, check the API key, model and connection.")
        else:
            st.markdown(answer)
            sources = [doc.page_content for doc in result.documents]
            if result.warning:
                st.warning(result.warning)
            if show_sources:
                with st.expander("Supporting information"):
                    for source in sources:
                        st.markdown(source)
            st.session_state.messages.extend([
                {"role": "user", "content": question},
                {"role": "assistant", "content": answer, "sources": sources, "warning": result.warning},
            ])
