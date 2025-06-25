import streamlit as st
from openai import OpenAI
import json

# Cargar ejemplos desde archivo externo
with open("ejemplos_fiducia.json", "r", encoding="utf-8") as f:
    ejemplos_fiducia = json.load(f)

# Centrar logo
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("Logo-gob-antioquia-ant.png", width=200)

# Título en tres renglones
st.title(":material/Neurology: Hola,")
st.markdown(
    """
    <h1 style='line-height: 1.5;'>
        ¿En qué puedo ayudarte hoy<br>
        ?
    </h1>
    """,
    unsafe_allow_html=True
)

# Logo institucional
st.logo("Logo-gob-antioquia-ant.png")

# Cliente OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Inicializar modelo
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# Inicializar historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Pregunta del usuario
if prompt := st.chat_input("preguntas sobre la gobernación?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            temperature=0,  # <<< MUY IMPORTANTE: creatividad mínima
            messages=ejemplos_fiducia + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
