import streamlit as st
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import ChatOpenAI
import os
import speech_recognition as sr
from io import BytesIO
from openai import OpenAI
#from pydub import AudioSegment

# Configure sua chave de API da OpenAI
os.environ["OPENAI_API_KEY"] = pessoal

# Configurar o banco SQLite
db = SQLDatabase.from_uri("sqlite:///test_database.db")

llm = ChatOpenAI(temperature=0, model="gpt-4", max_retries=2)

db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# Interface do Streamlit
st.title("Consulta GPT-4 Interação com SQLite")

# Inicializa estados necessários
if "text_area_query" not in st.session_state:
    st.session_state["text_area_query"] = ""

if "btn_Confirmar" not in st.session_state:
    st.session_state["btn_Confirmar"] = False

if "clear_text_area" not in st.session_state:
    st.session_state["clear_text_area"] = False  # Controla a limpeza do campo

# Limpa o conteúdo do campo se necessário
if st.session_state["clear_text_area"]:
    st.session_state["text_area_query"] = ""
    st.session_state["clear_text_area"] = False

# Gravar a instrução
audio_value = st.audio_input("Clique para realizar uma instrução por voz...")

if audio_value:
    
    transcription = client.audio.transcriptions.create(
        model='whisper-1',
        file = audio_value,
        prompt = 'Descreva a transcrição para o audio em questão'
    )

    st.session_state["text_area_query"] = transcription.text

# Entrada de texto
query = st.text_area("Questão", key="text_area_query", placeholder="Exemplo: Digite o que você deseja fazer com relação a massa de teste.")
context = "Voce deve responder sempre em portugues essas questões."

@st.dialog("Confirmar sentença")
def choice(item):
    st.write(f"Essa ação será irreversível e afetará os itens no banco de dados, deseja prosseguir?")
    if st.button("Confirmar"):
        clear_data()

def clear_data():
    st.session_state["clear_text_area"] = True
    st.session_state["btn_Confirmar"] = False
    st.rerun()

# Controle para exibir ou não os botões
if st.button("Enviar") and query:
    response = db_chain.invoke(query, context=context)
    st.write(response['result'])
    st.session_state["btn_Confirmar"] = True

# if st.session_state["btn_Confirmar"]:
#     st.write("Você deseja executar essa ação?")
#     if st.button("Sim"):
#         choice("Sim")
#     if st.button("Não"):
#         clear_data()
#     else:
#         pass