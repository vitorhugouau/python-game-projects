import mysql.connector
import customtkinter as ctk
from tkinter import ttk, messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def create_table():
    conn = mysql.connector.connect(host="localhost", user="root", password="")
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS Repertorio")
    cursor.execute("USE Repertorio")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Musica (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            artista VARCHAR(255) NOT NULL,
            palavras_chave VARCHAR(255),
            album VARCHAR(255),
            genero VARCHAR(50),
            ano INT,
            duracao_segundos INT,
            compositor VARCHAR(255),
            gravadora VARCHAR(255),
            caminho_arquivo VARCHAR(255)
        )
    ''')
    conn.commit()
    conn.close()

create_table()

def adicionar_musica():
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="Repertorio")
    cursor = conn.cursor()
    sql = """INSERT INTO Musica 
             (titulo, artista, palavras_chave, album, genero, ano, duracao_segundos, compositor, gravadora, caminho_arquivo)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    valores = (
        entry_titulo.get(),
        entry_artista.get(),
        entry_palavras.get(),
        entry_album.get(),
        entry_genero.get(),
        entry_ano.get(),
        entry_duracao.get(),
        entry_compositor.get(),
        entry_gravadora.get(),
        entry_caminho.get()
    )
    cursor.execute(sql, valores)
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Música adicionada!")
    listar_musicas()
    limpar_campos()

def listar_musicas():
    for i in tree.get_children():
        tree.delete(i)
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="Repertorio")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Musica")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

def atualizar_musica():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Erro", "Selecione uma música na tabela")
        return
    values = tree.item(selected, 'values')
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="Repertorio")
    cursor = conn.cursor()
    sql = """UPDATE Musica SET titulo=%s, artista=%s, palavras_chave=%s, album=%s, genero=%s,
             ano=%s, duracao_segundos=%s, compositor=%s, gravadora=%s, caminho_arquivo=%s WHERE id=%s"""
    dados = (
        entry_titulo.get(),
        entry_artista.get(),
        entry_palavras.get(),
        entry_album.get(),
        entry_genero.get(),
        entry_ano.get(),
        entry_duracao.get(),
        entry_compositor.get(),
        entry_gravadora.get(),
        entry_caminho.get(),
        values[0]
    )
    cursor.execute(sql, dados)
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Música atualizada!")
    listar_musicas()
    limpar_campos()

def deletar_musica():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Erro", "Selecione uma música na tabela")
        return
    values = tree.item(selected, 'values')
    conn = mysql.connector.connect(host="localhost", user="root", password="", database="Repertorio")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Musica WHERE id=%s", (values[0],))
    conn.commit()
    conn.close()
    messagebox.showinfo("Sucesso", "Música deletada!")
    listar_musicas()
    limpar_campos()

def preencher_campos(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, 'values')
        campos = [entry_titulo, entry_artista, entry_palavras, entry_album, entry_genero,
                  entry_ano, entry_duracao, entry_compositor, entry_gravadora, entry_caminho]
        for i, entry in enumerate(campos):
            entry.delete(0, "end")
            entry.insert(0, values[i+1])

def limpar_campos():
    for entry in [entry_titulo, entry_artista, entry_palavras, entry_album, entry_genero,
                  entry_ano, entry_duracao, entry_compositor, entry_gravadora, entry_caminho]:
        entry.delete(0, "end")

root = ctk.CTk()
root.title("🎵 Sistema de Músicas - Moderno")
root.geometry("1200x600")
root.resizable(False, False)

frame_form = ctk.CTkFrame(root, width=400, height=560)
frame_form.place(x=20, y=20)

frame_table = ctk.CTkFrame(root, width=740, height=560, corner_radius=15)
frame_table.place(x=440, y=20)

labels = ["Título", "Artista", "Palavras-chave", "Álbum", "Gênero", "Ano", "Duração", "Compositor", "Gravadora", "Caminho"]
entries = {}
y = 20
for label in labels:
    ctk.CTkLabel(frame_form, text=label, anchor="w", width=120).place(x=10, y=y)
    entry = ctk.CTkEntry(frame_form, width=240)
    entry.place(x=140, y=y)
    entries[label] = entry
    y += 40

entry_titulo = entries["Título"]
entry_artista = entries["Artista"]
entry_palavras = entries["Palavras-chave"]
entry_album = entries["Álbum"]
entry_genero = entries["Gênero"]
entry_ano = entries["Ano"]
entry_duracao = entries["Duração"]
entry_compositor = entries["Compositor"]
entry_gravadora = entries["Gravadora"]
entry_caminho = entries["Caminho"]

ctk.CTkButton(frame_form, text="Adicionar", command=adicionar_musica, width=160, height=40).place(x=20, y=450)
ctk.CTkButton(frame_form, text="Atualizar", command=atualizar_musica, width=160, height=40).place(x=200, y=450)
ctk.CTkButton(frame_form, text="Deletar", command=deletar_musica, width=160, height=40).place(x=20, y=500)
ctk.CTkButton(frame_form, text="Limpar Campos", command=limpar_campos, width=160, height=40).place(x=200, y=500)

columns = ("ID","Título","Artista","Palavras","Álbum","Gênero","Ano","Duração","Compositor","Gravadora","Caminho")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor="center")
tree.place(x=10, y=10, width=720, height=540)
tree.bind("<ButtonRelease-1>", preencher_campos)

listar_musicas()
root.mainloop()
