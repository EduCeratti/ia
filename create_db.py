import sqlite3

def initialize_database():
    connection = sqlite3.connect("test_database.db")
    cursor = connection.cursor()
    # Cria a tabela caso não exista
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS css_template (
        descricao TEXT,
        tipo TEXT,
        codigo TEXT
    )
    """)
    # Insere dados de exemplo
    cursor.execute("INSERT INTO css_template VALUES ('Mensagem de SMS', 'SMS', 'SMS_001')")
    cursor.execute("INSERT INTO css_template VALUES ('Mensagem de EMAIL', 'EMAIL', 'EMAIL_001')")
    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_database()