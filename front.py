import streamlit as st
import sqlite3
import pandas as pd

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('test_database.db')
cursor = conn.cursor()

# Ler dados da tabela
query = "SELECT * FROM css_template"
df = pd.read_sql_query(query, conn)

# Remover o índice
df = pd.DataFrame(df.to_dict())

# Mostrar os dados no Streamlit sem o índice
st.title('Dados de CSS')
st.dataframe(df, hide_index=True)

# Fechar a conexão
conn.close()