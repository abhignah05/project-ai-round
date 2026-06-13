import streamlit as st
import requests

st.title("AI Chat App")

thread_id = st.sidebar.text_input(
    "Thread Name",
    "thread1"
)

message = st.text_input(
    "Message"
)

if st.button("Send"):

    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json={
            "thread_id": thread_id,
            "message": message
        }
    )

    st.write(response.json()["reply"])

if st.sidebar.button("Load History"):

    response = requests.get(
        f"http://127.0.0.1:8000/threads/{thread_id}"
    )

    data = response.json()

    for msg in data:
        st.write(
            f"{msg['role']} : {msg['content']}"
        )