import mysql.connector
from tkinter import *
from tkinter import messagebox

# =======================
# CONFIGURAÇÃO DO BANCO
# =======================

def conectar_banco():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",           # ALTERE SE NECESSÁRIO
        password="",           # ALTERE SE NECESSÁRIO
    )
    return conn

def criar_banco_e_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS Repertorio")
    conn.database = "Repertorio"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Musica (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(255),
            artista VARCHAR(255),
            palavras_chave TEXT,
            album VARCHAR(255),
            genero VARCHAR(100),
            ano INT,
            duracao_segundos INT,
            compositor VARCHAR(255),
            gravadora VARCHAR(255),
            caminho_arquivo VARCHAR(500)
        )
    """)
    conn.commit()
    cursor.close()
    return conn

# =======================
# FUNÇÕES CRUD
# =======================

conn = criar_banco_e_tabela()
cursor = conn.cursor()

def inserir():
    try:
        sql = "INSERT INTO Musica (titulo, artista, palavras_chave, album, genero, ano, duracao_segundos, compositor, gravadora, caminho_arquivo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        valores = (
            titulo.get(), artista.get(), palavras_chave.get(), album.get(),
            genero.get(), int(ano.get()), int(duracao.get()),
            compositor.get(), gravadora.get(), caminho.get()
        )
        cursor.execute(sql, valores)
        conn.commit()
        messagebox.showinfo("Sucesso", "Música inserida com sucesso!")
        limpar_campos()
        visualizar()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def visualizar():
    try:
        cursor.execute("SELECT * FROM Musica")
        registros = cursor.fetchall()
        resultado.delete(0, END)
        for linha in registros:
            linha_formatada = f"ID: {linha[0]:<3} | Título: {linha[1]:<20} | Artista: {linha[2]:<15} | Álbum: {linha[4]:<15} | Gênero: {linha[5]:<10} | Ano: {linha[6]:<4}"
            resultado.insert(END, linha_formatada)
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def atualizar():
    if not id_musica.get().strip():
        messagebox.showwarning("Atenção", "Selecione uma música para atualizar.")
        return
    try:
        sql = """UPDATE Musica SET 
                    titulo=%s, artista=%s, palavras_chave=%s, album=%s,
                    genero=%s, ano=%s, duracao_segundos=%s,
                    compositor=%s, gravadora=%s, caminho_arquivo=%s
                 WHERE id=%s"""
        valores = (
            titulo.get(), artista.get(), palavras_chave.get(), album.get(),
            genero.get(), int(ano.get()), int(duracao.get()),
            compositor.get(), gravadora.get(), caminho.get(), int(id_musica.get())
        )
        cursor.execute(sql, valores)
        conn.commit()
        messagebox.showinfo("Sucesso", "Música atualizada com sucesso!")
        limpar_campos()
        visualizar()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def deletar():
    if not id_musica.get().strip():
        messagebox.showwarning("Atenção", "Selecione uma música para deletar.")
        return
    try:
        cursor.execute("DELETE FROM Musica WHERE id = %s", (int(id_musica.get()),))
        conn.commit()
        messagebox.showinfo("Sucesso", "Música deletada com sucesso!")
        limpar_campos()
        visualizar()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def limpar_campos():
    id_musica.delete(0, END)
    titulo.delete(0, END)
    artista.delete(0, END)
    palavras_chave.delete(0, END)
    album.delete(0, END)
    genero.delete(0, END)
    ano.delete(0, END)
    duracao.delete(0, END)
    compositor.delete(0, END)
    gravadora.delete(0, END)
    caminho.delete(0, END)

def preencher_campos(event):
    # Quando seleciona um item na lista
    selecionado = resultado.curselection()
    if not selecionado:
        return
    linha_texto = resultado.get(selecionado[0])
    # Extrair o ID da linha "ID: 123 | ..."
    try:
        id_str = linha_texto.split('|')[0].strip()  # "ID: 123"
        id_valor = int(id_str.split(':')[1].strip())
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao extrair ID: {e}")
        return
    
    # Buscar os dados completos no banco pelo id
    try:
        cursor.execute("SELECT * FROM Musica WHERE id=%s", (id_valor,))
        musica = cursor.fetchone()
        if musica:
            # Preencher os campos
            id_musica.delete(0, END)
            id_musica.insert(END, musica[0])
            titulo.delete(0, END)
            titulo.insert(END, musica[1])
            artista.delete(0, END)
            artista.insert(END, musica[2])
            palavras_chave.delete(0, END)
            palavras_chave.insert(END, musica[3])
            album.delete(0, END)
            album.insert(END, musica[4])
            genero.delete(0, END)
            genero.insert(END, musica[5])
            ano.delete(0, END)
            ano.insert(END, musica[6])
            duracao.delete(0, END)
            duracao.insert(END, musica[7])
            compositor.delete(0, END)
            compositor.insert(END, musica[8])
            gravadora.delete(0, END)
            gravadora.insert(END, musica[9])
            caminho.delete(0, END)
            caminho.insert(END, musica[10])
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao buscar dados: {e}")

# =======================
# INTERFACE GRÁFICA COMPLETA
# =======================

janela = Tk()
janela.title("CRUD - Repertório Musical")
janela.geometry("1100x750")
janela.configure(bg="#2E4053")

# Fontes
fonte_label = ("Calibri", 11, "bold")
fonte_entry = ("Calibri", 11)
fonte_botao = ("Calibri", 11, "bold")
fonte_lista = ("Consolas", 10)

# Container principal com padding
frame_principal = Frame(janela, bg="#34495E", padx=20, pady=20)
frame_principal.pack(fill=BOTH, expand=True, padx=20, pady=20)

# Título
titulo_label = Label(frame_principal, text="Cadastro de Músicas - Repertório", bg="#34495E", fg="#ECF0F1", font=("Calibri", 18, "bold"))
titulo_label.pack(pady=(0, 15))

# Frame formulário (2 colunas: label e entry)
frame_form = Frame(frame_principal, bg="#34495E")
frame_form.pack(side=TOP, fill=X, padx=5, pady=5)

def criar_campo_linha(parent, texto, largura=40):
    container = Frame(parent, bg="#34495E")
    container.pack(fill=X, pady=4)
    label = Label(container, text=texto+":", bg="#34495E", fg="#ECF0F1", font=fonte_label, width=18, anchor=W)
    label.pack(side=LEFT)
    entry = Entry(container, font=fonte_entry, width=largura, relief=FLAT)
    entry.pack(side=LEFT, fill=X, expand=True)
    return entry

# Criando todos os campos
id_musica = criar_campo_linha(frame_form, "ID", 10)
titulo = criar_campo_linha(frame_form, "Título")
artista = criar_campo_linha(frame_form, "Artista")
palavras_chave = criar_campo_linha(frame_form, "Palavras-chave")
album = criar_campo_linha(frame_form, "Álbum")
genero = criar_campo_linha(frame_form, "Gênero", 15)
ano = criar_campo_linha(frame_form, "Ano", 10)
duracao = criar_campo_linha(frame_form, "Duração (segundos)", 15)
compositor = criar_campo_linha(frame_form, "Compositor")
gravadora = criar_campo_linha(frame_form, "Gravadora")
caminho = criar_campo_linha(frame_form, "Caminho do arquivo", 45)

# Frame dos botões
frame_botoes = Frame(frame_principal, bg="#34495E")
frame_botoes.pack(pady=15)

btn_bg = "#2980B9"
btn_fg = "#ECF0F1"
btn_hover_bg = "#3498DB"

def on_enter(e):
    e.widget['background'] = btn_hover_bg

def on_leave(e):
    e.widget['background'] = btn_bg

btn_inserir = Button(frame_botoes, text="Inserir", bg=btn_bg, fg=btn_fg, font=fonte_botao, relief=FLAT, command=inserir, cursor="hand2", width=12)
btn_inserir.grid(row=0, column=0, padx=8, ipadx=10, ipady=5)

btn_visualizar = Button(frame_botoes, text="Visualizar", bg=btn_bg, fg=btn_fg, font=fonte_botao, relief=FLAT, command=visualizar, cursor="hand2", width=12)
btn_visualizar.grid(row=0, column=1, padx=8, ipadx=10, ipady=5)

btn_atualizar = Button(frame_botoes, text="Atualizar", bg=btn_bg, fg=btn_fg, font=fonte_botao, relief=FLAT, command=atualizar, cursor="hand2", width=12)
btn_atualizar.grid(row=0, column=2, padx=8, ipadx=10, ipady=5)

btn_deletar = Button(frame_botoes, text="Deletar", bg=btn_bg, fg=btn_fg, font=fonte_botao, relief=FLAT, command=deletar, cursor="hand2", width=12)
btn_deletar.grid(row=0, column=3, padx=8, ipadx=10, ipady=5)

btn_limpar = Button(frame_botoes, text="Limpar Campos", bg=btn_bg, fg=btn_fg, font=fonte_botao, relief=FLAT, command=limpar_campos, cursor="hand2", width=14)
btn_limpar.grid(row=0, column=4, padx=8, ipadx=10, ipady=5)

for b in [btn_inserir, btn_visualizar, btn_atualizar, btn_deletar, btn_limpar]:
    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)

# Título da tabela/listbox
titulo_lista = Label(frame_principal, text="Lista de Músicas Cadastradas", bg="#34495E", fg="#ECF0F1", font=("Calibri", 14, "bold"))
titulo_lista.pack(pady=(10, 5))

# Frame para listbox e scrollbar
frame_lista = Frame(frame_principal, bg="#34495E")
frame_lista.pack(fill=BOTH, expand=True)

scrollbar = Scrollbar(frame_lista)
scrollbar.pack(side=RIGHT, fill=Y)

resultado = Listbox(frame_lista, yscrollcommand=scrollbar.set, font=fonte_lista, bg="#ECF0F1", fg="#2C3E50", selectbackground="#2980B9", selectforeground="white", bd=2, relief=GROOVE)
resultado.pack(fill=BOTH, expand=True)

scrollbar.config(command=resultado.yview)

# Evento ao selecionar item na lista
resultado.bind("<<ListboxSelect>>", preencher_campos)

# Inicializa a lista
visualizar()

janela.mainloop()
