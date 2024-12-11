import sqlite3

# Conectar ao banco de dados SQLite3
conn = sqlite3.connect('test_database.db')
cursor = conn.cursor()

# Verificar se a tabela css_template existe
table_check_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='css_template';"
cursor.execute(table_check_query)

if cursor.fetchone():
    # Atualizar a tabela css_template
    update_query = """
    UPDATE css_template
    SET descricao = 'Exemplo 1'
    WHERE codigo = 'EMAIL_001';
    """
    
    cursor.execute(update_query)
    
    # Confirmar as alterações e fechar a conexão
    conn.commit()
    print("Atualização concluída com sucesso.")
else:
    print("A tabela css_template não existe no banco de dados.")

conn.close()