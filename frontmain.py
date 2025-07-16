from main import run_llm
import streamlit as st

st.header("Langchain Udemy Course- Documentation Helper Bots")


prompt = st.text_input("Prompt", placeholder="Enter your Prompt here...")

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_answer_history" not in st.session_state:
    st.session_state["chat_answer_history"] = []


if prompt:
    with st.spinner("Generating Response..."):
        generated_response = run_llm(query=prompt)

        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )
        formatted_response = (
            f"{generated_response["result"]}  \n\n {sources}"
        )
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answer_history"].append(formatted_response)

if st.session_state["chat_answer_history"]:
    for user_query, generated_response in zip(st.session_state["user_prompt_history"], st.session_state["chat_answer_history"]):
        st.chat_message("user").write(user_query)
        st.chat_message("assistant").write(generated_response)