import sqlite3

class Musica:
    def __init__(self, **entries):
        self.__dict__.update(entries)

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

def add_musica(payload):
    connection = sqlite3.connect('musica.db')
    cursor = connection.cursor()
    cursor.execute(''' INSERT INTO Musica (
                   titulo,
                   artista,
                   palavras_chave,
                   album,
                   genero,
                   ano,
                   duracao_segundos,
                   compositor,
                   gravadora,
                   caminho_arquivo
                   ) VALUES (
                   ?,
                   ?,
                   ?,
                   ?,
                   ?,
                   ?,
                   ?,
                   ?,
                   ?,
                   ?
                   ) ''', (
                    payload.titulo,
                    payload.artista,
                    payload.palavras_chave,
                    payload.album,
                    payload.genero,
                    payload.ano,
                    payload.duracao_segundos,
                    payload.compositor,
                    payload.gravadora,
                    payload.caminho_arquivo
                   ))
    connection.commit()
    connection.close()

def list_musics():
    connection = sqlite3.connect('musica.db')
    cursor = connection.cursor()
    cursor.execute(''' SELECT * FROM Musica ''')
    musicas = cursor.fetchall()
    for musica in musicas:
        print(musica)
    connection.close()

def att_music(payload):
    connection = sqlite3.connect('musica.db')
    cursor = connection.cursor()
    cursor.execute(''' UPDATE Musica SET
                   titulo = ?,
                   artista = ?,
                   palavras_chave = ?,
                   album = ?,
                   genero = ?,
                   ano = ?,
                   duracao_segundos = ?,
                   compositor = ?,
                   gravadora = ?,
                   caminho_arquivo = ?
                   WHERE id = ? ''',
                   (
                       payload.titulo,
                       payload.artista,
                       payload.palavras_chave,
                       payload.album,
                       payload.genero,
                       payload.ano,
                       payload.duracao_segundos,
                       payload.compositor,
                       payload.gravadora,
                       payload.caminho_arquivo,
                       payload.id
                    ))
    connection.commit()
    connection.close()

def delete_music(id):
    connection = sqlite3.connect('musica.db')
    cursor = connection.cursor()
    cursor.execute(''' DELETE FROM Musica WHERE id = ? ''', (id,))
    connection.commit()
    connection.close()

def menu():
    print('\n' + '=' * 40)
    print('🛠️  MENU DO SISTEMA DE MÚSICAS')
    print('=' * 40)
    print('1 - Adicionar nova música')
    print('2 - Listar todas as músicas')
    print('3 - Atualizar música existente')
    print('4 - Deletar música')
    print('5 - Sair do programa')
    print('=' * 40)

create_table()
menu()

while True:
    choice = input('Escolha uma opção: ')

    if choice == '1':
        titulo = input('Digite o título da música: ')
        artista = input('Digite o artista da música: ')
        palavras_chave = input('Digite as palavras-chave da música: ')
        album = input('Digite o álbum da música: ')
        genero = input('Digite o gênero da música: ')
        ano = int(input('Digite o ano da música: '))
        duracao_segundos = int(input('Digite a duração da música em segundos: '))
        compositor = input('Digite o compositor da música: ')
        gravadora = input('Digite a gravadora da música: ')
        caminho_arquivo = input('Digite o caminho do arquivo da música: ')

        obj = {
            "titulo": titulo,
            "artista": artista,
            "palavras_chave": palavras_chave,
            "album": album,
            "genero": genero,
            "ano": ano,
            "duracao_segundos": duracao_segundos,
            "compositor": compositor,
            "gravadora": gravadora,
            "caminho_arquivo": caminho_arquivo                     
        }

        musica = Musica(**obj)
        add_musica(musica)
        print('Música adicionada com sucesso!')
    elif choice == '2':
        print('\nTodas as músicas: ')
        list_musics()
    elif choice == '3':
        id = int(input('Digite o ID da música a ser atualizada: '))

        titulo = input('Digite o título da música: ')
        artista = input('Digite o artista da música: ')
        palavras_chave = input('Digite as palavras-chave da música: ')
        album = input('Digite o álbum da música: ')
        genero = input('Digite o gênero da música: ')
        ano = int(input('Digite o ano da música: '))
        duracao_segundos = int(input('Digite a duração da música em segundos: '))
        compositor = input('Digite o compositor da música: ')
        gravadora = input('Digite a gravadora da música: ')
        caminho_arquivo = input('Digite o caminho do arquivo da música: ')

        obj = {
            "titulo": titulo,
            "artista": artista,
            "palavras_chave": palavras_chave,
            "album": album,
            "genero": genero,
            "ano": ano,
            "duracao_segundos": duracao_segundos,
            "compositor": compositor,
            "gravadora": gravadora,
            "caminho_arquivo": caminho_arquivo,
            "id": id
        }

        musica = Musica(**obj)
        att_music(musica)
        print('Música atualizada com sucesso!')
    elif choice == '4':
        id = int(input('Digite o ID da música a ser deletada: '))
        delete_music(id)
        print('Música deletada com sucesso!')
    elif choice == '5':
        print('Saindo do programa...')
        break
    else:
        print('Opção inválida. Por favor, escolha uma opção válida.')