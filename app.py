import streamlit as st
from chatbot import app

st.set_page_config(
    page_title="College AI Assistant",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------
st.title("🎓 College AI Assistant")
st.caption("Ask anything about academics, fees or general topics.")

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "programme" not in st.session_state:
    st.session_state.programme = "B.Tech.(H)"

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.header("Student Details")

    programme = st.selectbox(
        "Select your Programme",
        [
            "B.Tech.(H)",
            "BCA",
            "BBA"
        ],
        index=0
    )

    st.session_state.programme = programme

    st.divider()

    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# Display Chat History
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat Input
# -----------------------------
prompt = st.chat_input("Ask your question...")

if prompt:

    # User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            result = app.invoke(
                {
                    "programme": st.session_state.programme,
                    "messages": [("human", prompt)]
                }
            )

            answer = result["messages"][-1].content

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )