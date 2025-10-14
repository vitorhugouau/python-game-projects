import pandas as pd
import sqlite3
import os

DB_FILE = 'empresa.db'
TABLE_NAME = 'usuarios'
EXCEL_FILE = 'usuarios_exportados.xlsx'

def create_users_table():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Usuarios (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL,
            idade INTEGER,
            pais TEXT
        )
    ''')

    usuarios_ficticios = [
        ('Alice Silva', 'alice@email.com', 'senha123', 25, 'Brasil'),
        ('Bruno Souza', 'bruno@email.com', 'abc123', 30, 'Portugal'),
        ('Carla Mendes', 'carla@email.com', 'xyz789', 22, 'Brasil'),
        ('Daniel Costa', 'daniel@email.com', 'pass456', 28, 'Espanha')
    ]

    cursor.executemany('''
        INSERT INTO Usuarios (nome, email, senha, idade, pais)
        VALUES (?, ?, ?, ?, ?)
    ''', usuarios_ficticios)

    connection.commit()
    connection.close()
    print("Tabela Usuarios criada e dados inseridos com sucesso!")

def export():
    if not os.path.exists(DB_FILE):
        print(f"Erro: O arquivo de banco de dados '{DB_FILE} não foi encontrado.")
        return
    
    try:
        conn = sqlite3.connect(DB_FILE)
        query = f"SELECT * FROM {TABLE_NAME}"    
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
        
        print(f"Sucesso! Os dados da tabel '{TABLE_NAME}' foram exportados para '{EXCEL_FILE}")
    except sqlite3.OperationalError as e:
        print(f"Erro de SQL. Verifique se a tabela {TABLE_NAME} existe. {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
        
if __name__ == "__main__":
    export()