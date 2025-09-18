import sqlite3
from tkinter import *
from tkinter import messagebox
from reportlab.pdfgen import canvas

# Conexão com o banco de dados
conn = sqlite3.connect('repertorio.db')
cursor = conn.cursor()

# Criar tabela Musica
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Musica (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        artista TEXT,
        palavras_chave TEXT,
        album TEXT,
        genero TEXT,
        ano INTEGER,
        duracao_segundos INTEGER,
        compositor TEXT,
        gravadora TEXT,
        caminho_arquivo TEXT
    )
''')
conn.commit()

# Função para adicionar uma música
def adicionar_musica():
    dados = (titulo_entry.get(), artista_entry.get(), palavras_entry.get(), album_entry.get(), genero_entry.get(),
             int(ano_entry.get()), int(duracao_entry.get()), compositor_entry.get(), gravadora_entry.get(), caminho_entry.get())
    cursor.execute('''
        INSERT INTO Musica (titulo, artista, palavras_chave, album, genero, ano, duracao_segundos, compositor, gravadora, caminho_arquivo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', dados)
    conn.commit()
    messagebox.showinfo("Sucesso", "Música adicionada com sucesso!")

# Função para exportar PDF
def exportar_pdf():
    cursor.execute("SELECT titulo, genero, compositor FROM Musica")
    musicas = cursor.fetchall()
    
    c = canvas.Canvas("musicas_exportadas.pdf")
    c.setFont("Helvetica", 12)
    c.drawString(100, 820, "Relatório de Músicas - Título, Gênero e Compositor")
    
    y = 800
    for musica in musicas:
        c.drawString(100, y, f"Título: {musica[0]} | Gênero: {musica[1]} | Compositor: {musica[2]}")
        y -= 20
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = 820

    c.save()
    messagebox.showinfo("Exportado", "PDF gerado com sucesso!")

# Interface gráfica
root = Tk()
root.title("Cadastro de Músicas")

# Labels e entradas
Label(root, text="Título").grid(row=0, column=0)
titulo_entry = Entry(root)
titulo_entry.grid(row=0, column=1)

Label(root, text="Artista").grid(row=1, column=0)
artista_entry = Entry(root)
artista_entry.grid(row=1, column=1)

Label(root, text="Palavras-chave").grid(row=2, column=0)
palavras_entry = Entry(root)
palavras_entry.grid(row=2, column=1)

Label(root, text="Álbum").grid(row=3, column=0)
album_entry = Entry(root)
album_entry.grid(row=3, column=1)

Label(root, text="Gênero").grid(row=4, column=0)
genero_entry = Entry(root)
genero_entry.grid(row=4, column=1)

Label(root, text="Ano").grid(row=5, column=0)
ano_entry = Entry(root)
ano_entry.grid(row=5, column=1)

Label(root, text="Duração (s)").grid(row=6, column=0)
duracao_entry = Entry(root)
duracao_entry.grid(row=6, column=1)

Label(root, text="Compositor").grid(row=7, column=0)
compositor_entry = Entry(root)
compositor_entry.grid(row=7, column=1)

Label(root, text="Gravadora").grid(row=8, column=0)
gravadora_entry = Entry(root)
gravadora_entry.grid(row=8, column=1)

Label(root, text="Caminho do Arquivo").grid(row=9, column=0)
caminho_entry = Entry(root)
caminho_entry.grid(row=9, column=1)

# Botões
Button(root, text="Adicionar Música", command=adicionar_musica).grid(row=10, column=0, pady=10)
Button(root, text="Exportar para PDF", command=exportar_pdf).grid(row=10, column=1, pady=10)

root.mainloop()

# Fechar conexão ao sair
conn.close()
 