import sqlite3

def create_table():
    connection = sqlite3.connect('musica.db')
    cursor = connection.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS Musica (
                   id INTEGER PRIMARY KEY,
                   titulo TEXT NOT NULL,
                   artista TEXT NOT NULL,
                   palavras_chave TEXT NOT NULL,
                   album TEXT NOT NULL,
                   genero TEXT NOT NULL,
                   ano INTEGER NOT NULL,
                   duracao_segundos INTEGER NOT NULL,
                   compositor TEXT NOT NULL,
                   gravadora TEXT NOT NULL,
                   caminho_arquivo TEXT NOT NULL) ''')
    connection.commit()
    connection.close()