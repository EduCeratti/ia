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
st.markdown("Digite uma instrução na caixa abaixo para consultar o banco de dados.")

# Entrada de texto
query = st.text_area("Instrução para o GPT-4", placeholder="Exemplo: Digite o que você deseja fazer com relação a massa de teste.")

# Botão de envio
if st.button("Enviar"):
    if query.strip():
        #try:
          
        result = db_chain.invoke(query)
        st.success("Consulta realizada com sucesso!")
        st.write("**Resultado:**")
        st.code(result, language="sql")
        # except Exception as e:
        #     st.error(f"Erro ao processar a consulta: {e}")
    else:
        st.warning("Por favor, digite uma instrução antes de enviar.")
