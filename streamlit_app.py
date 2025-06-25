import streamlit as st
from openai import OpenAI

st.title(":material/Neurology: Conversa con la Gobernación ")
st.write(
    "inspirado por Medicina Computacional [https://www.medicinacomputacional.com/](https://www.medicinacomputacional.com/)."
)

#st.logo("logioto77.jpg")
st.logo("Logo-gob-antioquia-ant.png")

client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])

##############################################################################################################################
#                                                 Entrenar con pdf
##############################################################################################################################




##############################################################################################################################
#                                                 listo habla normal  
##############################################################################################################################
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("preguntas sobre investigación médica?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream = True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
