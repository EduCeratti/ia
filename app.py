import os
import re
import sqlite3
import streamlit as st

from langchain_community.utilities.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain_openai import ChatOpenAI
from openai import OpenAI
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent

# Configure sua chave de API da OpenAI
os.environ["OPENAI_API_KEY"] = pessoal
client = OpenAI()

# Configurar o banco SQLite
db = SQLDatabase.from_uri("sqlite:///test_database.db")
llm = ChatOpenAI(temperature=0, model="gpt-4", max_retries=2)
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

def execute_query(query):
    conexao = sqlite3.connect('test_database.db')
    cursor = conexao.cursor()
    cursor.execute(query)
    conexao.commit()
    conexao.close()

# Interface do Streamlit
st.title("Consulta GPT-4 Interação com SQLite")

# Controla a limpeza dos campos
if "query" not in st.session_state:
    st.session_state["query"] = ""

if "text_area_query" not in st.session_state:
    st.session_state["text_area_query"] = ""

if "btn_Confirmar" not in st.session_state:
    st.session_state["btn_Confirmar"] = False

if "clear_text_area" not in st.session_state:
    st.session_state["clear_text_area"] = False  

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

context = """. Você é um especialista em banco de dados. Você deve retornar sempre a resposta final escrita em lingua portuguesa falada comumente no Brasil.
Mesmo que alguma interpretação você entender que a resposta ou pergunta esteja em outra linguagem, me responda em portugues.
Você deve retornar sempre na parte final de sua resposta uma variavel com o nome QUERY= seguido de tres aspas simples conforme o exemplo a seguir, 
e nessa variavel você deve me devolver a instrução SQL que seria executada no banco de dados, considerando que esse banco é um SqlLite.
QUERY=''' INSERT INTO css_template  values ('Nome de Teste', 'SMS', 'SMS_000')''', esse é apenas um exemplo, a query deve ser a que será executada baseada na pergunta
inicial, poderá ser de DELETE, de INSERT, de UPDATE, ou de SELECT.
Antes da variavel QUERY você deve descrever apenas no que consiste o comando SQL que você está gerando. E no seu retorno não deve retornar mensagens como, 
aqui está, ou então, segue a seguir a instrução, ou ainda A instrução utilizada foi a seguinte. 
Você deve retornar apenas duas frases. Uma contendo toda explicação do que a instrução inicial faz, e depois somente uma outra com a variavel QUERY.
E coloque cada instrução SQL retornada sempre dentro de parenteses
"""

query = query + context

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=SQLDatabaseToolkit(db=db, llm=llm),
    verbose=True
)

@st.dialog("Confirmar sentença")
def choice(item):
    st.write(f"Essa ação será irreversível e afetará os itens no banco de dados, deseja prosseguir?")
    if st.button("Confirmar"):
        print('dentro')
        print(st.session_state["query"])
        clear_data()

def clear_data():
    st.session_state["clear_text_area"] = True
    st.session_state["btn_Confirmar"] = False
    st.rerun()

# Controle para exibir ou não os botões
if st.button("Enviar") and query:
    response = agent_executor.invoke(query)

    # Remover tudo após e incluindo 'QUERY='
    texto_limpo = re.sub(r"QUERY=.*", "", response['output']) 
    query_match = re.search(r"QUERY='''(.*)'''", response['output'], re.DOTALL)
    query_valor = query_match.group(1) if query_match else None  
    st.session_state["query"] = query_valor
    st.write(texto_limpo)    
    st.session_state["btn_Confirmar"] = True

if st.session_state["btn_Confirmar"]:
    st.write("Você deseja executar essa ação?")
    if st.button("Sim"):        
        execute_query(st.session_state["query"])
        choice("Sim")
    if st.button("Não"):
        clear_data()
    else:
        pass