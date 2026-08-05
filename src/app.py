import streamlit as st
from llm import generate_chat_response

st.set_page_config(page_title="English Assistant", page_icon="🤖", layout="centered")

st.title("🤖 Personal English Chatbot")
st.markdown("Type English words, chat, make practice and so on!")


if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "Hello! I am your personal English teacher. If you ask me a word, I can explain to you more comprehensively and permanently stay in your mind. How can I help you today?"
        }
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


if prompt := st.chat_input("Type something..."):
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )
    with st.chat_message("user"):
        st.markdown(prompt)


        system_rules = f"""
        You are a highly engaging, expert English teacher. 
        User's input: "{prompt}"
        RULE 1 - CONVERSATION & FEEDBACK: If the user is pointing out a mistake, giving feedback, or just chatting, RESPOND NATURALLY. Do not treat it as a vocabulary request.
        RULE 2 - TEACHING (CRITICAL): If the user asks about a word, YOU MUST EXPLAIN IT YOURSELF directly(if user ask another language rather than English then you must stop). DO NOT ask the user what they think it means. DO NOT ask the user to define it. Give an IMPRESSIVE explanation (core nuance, memory hook, striking example).
        RULE 3 - THE QUIZ: ONLY AFTER your explanation, add a fill-in-the-blank question to test them.
        CRITICAL QUIZ FORMAT:
        Question: [Write a sentence demonstrating the word, but YOU MUST REPLACE the target word with '_____'. The target word MUST NOT appear in the sentence!]
        A) [Distractor]
        B) [Distractor]
        C) [Distractor]
        D) [Correct Word]
        """
        api_messages = [
            {
                "role": "system", 
                "content": system_rules
             }] + st.session_state.messages

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                bot_reply = generate_chat_response(api_messages)
                st.markdown(bot_reply)

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content": bot_reply
            }
        )



        
        