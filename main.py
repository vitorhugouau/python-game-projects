import sqlite3

def create_table():
    connection = sqlite3.connect('exemplo.db')
    cursor = connection.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS usuarios (
                   id INTEGER PRIMARY KEY,
                   nome TEXT NOT NULL,
                   idade INTEGER) ''')
    connection.commit()
    connection.close()

def add_user(name, age):
    connection = sqlite3.connect('exemplo.db')
    cursor = connection.cursor()
    cursor.execute(''' INSERT INTO usuarios (nome, idade) VALUES (?, ?) ''', (name, age))
    connection.commit()
    connection.close()

def list_users():
    connection = sqlite3.connect('exemplo.db')
    cursor = connection.cursor()
    cursor.execute(''' SELECT * FROM usuarios ''')
    usuarios = cursor.fetchall()
    for usuario in usuarios:
        print(usuario)
    connection.close()

def att_user(id, name, age):
    connection = sqlite3.connect('exemplo.db')
    cursor = connection.cursor()
    cursor.execute(''' UPDATE usuarios SET nome = ?, idade = ? WHERE id = ? ''', (name, age, id))
    connection.commit()
    connection.close()

def delete_user(id):
    connection = sqlite3.connect('exemplo.db')
    cursor = connection.cursor()
    cursor.execute(''' DELETE FROM usuarios WHERE id = ? ''', (id,))
    connection.commit()
    connection.close()

def list_user_with_filter(idade):
    connection = sqlite3.connect('exemplo.db')
    cursor = connection.cursor()
    cursor.execute(''' SELECT * FROM usuarios WHERE idade <= ? ''', (idade,))
    usuarios = cursor.fetchall()
    for usuario in usuarios:
        print(usuario)
    connection.close()


def menu():
    print('\n' + '=' * 40)
    print('🛠️  MENU DO SISTEMA DE USUÁRIOS')
    print('=' * 40)
    print('1 - Adicionar novo usuário')
    print('2 - Listar todos os usuários')
    print('3 - Atualizar usuário existente')
    print('4 - Deletar usuário')
    print('5 - Listar usuários com idade menor que a idade inserida')
    print('6 - Sair do programa')
    print('=' * 40)

create_table()
menu()


while True:
    choice = input('Escolha uma opção: ')

    if choice == '1':
        name = input('Digite o nome do usuário: ')
        age = int(input('Digite a idade do usuário: '))
        add_user(name, age)
    elif choice == '2':
        print('\nTodos os usuários: ')
        list_users()
    elif choice == '3':
        id = int(input('Digite o ID do usuário a ser atualizado: '))

        name = input('Digite o novo nome do usuário')
        age = int(input('Digite a nova idade do usuário: '))

        att_user(id, name, age)
    elif choice == '4':
        id = int(input('Digite o ID do usuário a ser deletado: '))
        delete_user(id)
        print('Usuário deletado com sucesso!')
    elif choice == '5':
        idade = int(input('Insira a idade desejada para buscar todos os usuários que tem idade menor que a inserida: '))
        list_user_with_filter(idade)
        print('Filtragem feita com sucesso!')
    elif choice == '6':
        print('Saindo do programa...')
        break
    else:
        print('Opção inválida. Por favor, escolha uma opção válida.')