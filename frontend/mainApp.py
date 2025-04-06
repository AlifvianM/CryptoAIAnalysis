import pandas as pd
import streamlit as st

from chat.get_resp import get_requests

st.write("""
    # Welcome to Your Smartest Bitcoin Assistant ₿!
""")

st.caption("🚀 A Streamlit chatbot powered by OpenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    response = get_requests(question="Lakukan analisis Bitcoin dan berikan rekomendasi.")
    pass
#     if not openai_api_key:
#         st.info("Please add your OpenAI API key to continue.")
#         st.stop()
