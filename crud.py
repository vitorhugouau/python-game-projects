import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import platform
import os

def create_table():
    conexao = sqlite3.connect("Repertorio.db")
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS musica (
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
    conexao.commit()
    conexao.close()
    

def add_user(titulo, artista, palavras_chave, album, genero, ano, duracao_segundos, compositor, gravadora, caminho_arquivo):
    conexao = sqlite3.connect("Repertorio.db")
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO musica (titulo, artista, palavras_chave, album, genero, ano, duracao_segundos, compositor, gravadora, caminho_arquivo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (titulo, artista, palavras_chave, album, genero, int(ano), int(duracao_segundos), compositor, gravadora, caminho_arquivo))
    conexao.commit()
    conexao.close()

def list_user():
    conexao = sqlite3.connect("Repertorio.db")
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM musica')
    usuarios = cursor.fetchall()
    conexao.close()
    return usuarios

def delete_user(id):
    conexao = sqlite3.connect("Repertorio.db")
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM musica WHERE id = ?', (id,))
    conexao.commit()
    conexao.close()

def refresh(id, titulo, artista, palavras_chave, album, genero, ano, duracao_segundos, compositor, gravadora, caminho_arquivo):
    conexao = sqlite3.connect("Repertorio.db")
    cursor = conexao.cursor()
    cursor.execute('''
        UPDATE musica
        SET titulo = ?, artista = ?, palavras_chave = ?, album = ?, genero = ?, ano = ?, duracao_segundos = ?, compositor = ?, gravadora = ?, caminho_arquivo = ?
        WHERE id = ?
    ''', (titulo, artista, palavras_chave, album, genero, int(ano), int(duracao_segundos), compositor, gravadora, caminho_arquivo, id))
    conexao.commit()
    conexao.close()

def desligar_pc():
    sistema = platform.system()
    if sistema == 'Windows':
        os.system("shutdown /s /t 1")
    elif sistema in ['Linux', 'Darwin']:
        os.system("shutdown -h now")
    else:
        messagebox.showerror("Erro", "Sistema não suportado para desligamento.")

def inserir_musica():
    def salvar():
        try:
            add_user(
                titulo.get(),
                artista.get(),
                palavras_chave.get(),
                album.get(),
                genero.get(),
                int(ano.get()),
                int(duracao.get()),
                compositor.get(),
                gravadora.get(),
                caminho.get()
            )
            messagebox.showinfo("Sucesso", "Música adicionada!")
            janela.destroy()
            atualizar_lista()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    janela = tk.Toplevel(root)
    janela.title("Adicionar Música")
    janela.configure(bg="#f0f2f5")
    campos = ["Título", "Artista", "Palavras-chave", "Álbum", "Gênero", "Ano", "Duração (seg)", "Compositor", "Gravadora", "Caminho do Arquivo"]
    entradas = []
    for i, campo in enumerate(campos):
        tk.Label(janela, text=campo, bg="#f0f2f5", font=("Segoe UI", 10)).grid(row=i, column=0, sticky="w", padx=10, pady=5)
    titulo = tk.Entry(janela, font=("Segoe UI", 10))
    artista = tk.Entry(janela, font=("Segoe UI", 10))
    palavras_chave = tk.Entry(janela, font=("Segoe UI", 10))
    album = tk.Entry(janela, font=("Segoe UI", 10))
    genero = tk.Entry(janela, font=("Segoe UI", 10))
    ano = tk.Entry(janela, font=("Segoe UI", 10))
    duracao = tk.Entry(janela, font=("Segoe UI", 10))
    compositor = tk.Entry(janela, font=("Segoe UI", 10))
    gravadora = tk.Entry(janela, font=("Segoe UI", 10))
    caminho = tk.Entry(janela, font=("Segoe UI", 10))
    entradas = [titulo, artista, palavras_chave, album, genero, ano, duracao, compositor, gravadora, caminho]
    for i, entrada in enumerate(entradas):
        entrada.grid(row=i, column=1, padx=10, pady=5)
    bot_salvar = tk.Button(janela, text="Salvar", command=salvar, font=("Segoe UI", 10, "bold"), bg="#4a90e2", fg="white", activebackground="#357ABD", activeforeground="white", relief=tk.FLAT, padx=10, pady=5, cursor="hand2")
    bot_salvar.grid(row=len(campos), columnspan=2, pady=10)
    bot_salvar.bind("<Enter>", lambda e: bot_salvar.config(bg="#357ABD"))
    bot_salvar.bind("<Leave>", lambda e: bot_salvar.config(bg="#4a90e2"))

def atualizar_lista():
    for item in tree.get_children():
        tree.delete(item)
    for row in list_user():
        tree.insert("", "end", values=row)

def deletar_musica():
    item = tree.selection()
    if item:
        id = tree.item(item[0])['values'][0]
        delete_user(id)
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Música deletada.")
    else:
        messagebox.showwarning("Atenção", "Selecione uma música.")

def atualizar_musica():
    item = tree.selection()
    if not item:
        messagebox.showwarning("Atenção", "Selecione uma música.")
        return
    dados = tree.item(item[0])['values']
    id = dados[0]
    def salvar():
        try:
            refresh(
                id,
                titulo.get(),
                artista.get(),
                palavras_chave.get(),
                album.get(),
                genero.get(),
                int(ano.get()),
                int(duracao.get()),
                compositor.get(),
                gravadora.get(),
                caminho.get()
            )
            messagebox.showinfo("Sucesso", "Música atualizada!")
            janela.destroy()
            atualizar_lista()
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    janela = tk.Toplevel(root)
    janela.title("Atualizar Música")
    janela.configure(bg="#f0f2f5")
    campos = ["Título", "Artista", "Palavras-chave", "Álbum", "Gênero", "Ano", "Duração (seg)", "Compositor", "Gravadora", "Caminho do Arquivo"]
    valores = dados[1:]
    entradas = []
    for i, campo in enumerate(campos):
        tk.Label(janela, text=campo, bg="#f0f2f5", font=("Segoe UI", 10)).grid(row=i, column=0, sticky="w", padx=10, pady=5)
    titulo = tk.Entry(janela, font=("Segoe UI", 10))
    artista = tk.Entry(janela, font=("Segoe UI", 10))
    palavras_chave = tk.Entry(janela, font=("Segoe UI", 10))
    album = tk.Entry(janela, font=("Segoe UI", 10))
    genero = tk.Entry(janela, font=("Segoe UI", 10))
    ano = tk.Entry(janela, font=("Segoe UI", 10))
    duracao = tk.Entry(janela, font=("Segoe UI", 10))
    compositor = tk.Entry(janela, font=("Segoe UI", 10))
    gravadora = tk.Entry(janela, font=("Segoe UI", 10))
    caminho = tk.Entry(janela, font=("Segoe UI", 10))
    entradas = [titulo, artista, palavras_chave, album, genero, ano, duracao, compositor, gravadora, caminho]
    for i, (entrada, valor) in enumerate(zip(entradas, valores)):
        entrada.insert(0, valor)
        entrada.grid(row=i, column=1, padx=10, pady=5)
    bot_salvar = tk.Button(janela, text="Salvar Alterações", command=salvar, font=("Segoe UI", 10, "bold"), bg="#4a90e2", fg="white", activebackground="#357ABD", activeforeground="white", relief=tk.FLAT, padx=10, pady=5, cursor="hand2")
    bot_salvar.grid(row=len(campos), columnspan=2, pady=10)
    bot_salvar.bind("<Enter>", lambda e: bot_salvar.config(bg="#357ABD"))
    bot_salvar.bind("<Leave>", lambda e: bot_salvar.config(bg="#4a90e2"))

create_table()

root = tk.Tk()
root.title("Gerenciador de Músicas")
root.geometry("1100x600")
root.configure(bg="#f0f2f5")

FONT_NORMAL = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")
FONT_TITLE = ("Segoe UI", 14, "bold")

titulo_app = tk.Label(root, text="Gerenciador de Músicas", font=FONT_TITLE, bg="#f0f2f5", fg="#333")
titulo_app.pack(pady=(10, 5))

frame_tree = tk.Frame(root, bg="#f0f2f5", bd=2, relief=tk.GROOVE)
frame_tree.pack(padx=15, pady=5, fill=tk.BOTH, expand=True)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=FONT_BOLD, foreground="#222", background="#d1d9e6")
style.configure("Treeview", font=FONT_NORMAL, rowheight=25, background="white", fieldbackground="white")
style.map('Treeview', background=[('selected', '#347083')], foreground=[('selected', 'white')])

tree = ttk.Treeview(frame_tree, columns=('ID', 'Título', 'Artista', 'Palavras-chave', 'Álbum', 'Gênero', 'Ano', 'Duração', 'Compositor', 'Gravadora', 'Caminho'), show='headings')

col_widths = [40, 150, 120, 120, 120, 80, 60, 80, 120, 120, 180]
for col, width in zip(tree["columns"], col_widths):
    tree.heading(col, text=col)
    tree.column(col, width=width, anchor="w")

tree.pack(fill=tk.BOTH, expand=True)

frame_botoes = tk.Frame(root, bg="#f0f2f5")
frame_botoes.pack(pady=15)

def criar_botao(master, texto, comando):
    btn = tk.Button(master, text=texto, command=comando, font=FONT_BOLD,
                    bg="#4a90e2", fg="white", activebackground="#357ABD", activeforeground="white",
                    relief=tk.FLAT, padx=15, pady=6, cursor="hand2")
    btn.bind("<Enter>", lambda e: btn.config(bg="#357ABD"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#4a90e2"))
    return btn

btn_adicionar = criar_botao(frame_botoes, "Adicionar", inserir_musica)
btn_atualizar = criar_botao(frame_botoes, "Atualizar", atualizar_musica)
btn_deletar = criar_botao(frame_botoes, "Deletar", deletar_musica)
btn_sair = criar_botao(frame_botoes, "Sair", root.destroy)
btn_desligar = criar_botao(frame_botoes, "Desligar PC", desligar_pc)

btn_adicionar.grid(row=0, column=0, padx=8)
btn_atualizar.grid(row=0, column=1, padx=8)
btn_deletar.grid(row=0, column=2, padx=8)
btn_sair.grid(row=0, column=3, padx=8)
btn_desligar.grid(row=0, column=4, padx=8)

atualizar_lista()

root.mainloop()
