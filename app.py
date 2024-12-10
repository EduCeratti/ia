import streamlit as st
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import ChatOpenAI
import os

# Configure sua chave de API da OpenAI
os.environ["OPENAI_API_KEY"] = pessoal

# Configurar o banco SQLite
db = SQLDatabase.from_uri("sqlite:///test_database.db")
llm = ChatOpenAI(temperature=0, model="gpt-4", max_retries=2)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# Interface do Streamlit
st.title("Consulta GPT-4 com SQLite")

# Entrada de texto
query = st.text_area("", placeholder="Exemplo: Digite o que você deseja fazer com relação a massa de teste.")

@st.dialog("Confirmar sentença")
def choice(item):
    st.write(f"Essa ação será irreversível e afetará os itens no banco de dados, deseja prosseguir?")
    if st.button("Confirmar"):
        st.rerun()

if "btn_Confirmar" not in st.session_state:
    st.session_state["btn_Confirmar"] = False

# Controle para exibir ou não os botões
if st.button("Enviar") and query:
    print(query)
    st.session_state["btn_Confirmar"] = True

if st.session_state["btn_Confirmar"]:
    st.write("Você deseja executar essa ação?")    
    if st.button("Sim"):
        print("Teste")
        choice("Sim")
    if st.button("Não"):
        st.write("Que pena!")
    else:
        pass
