import tkinter as tk

janela = tk.Tk()
janela.title("Calculadora")
janela.configure(bg="#000000")
janela.resizable(False, False)

entrada = tk.Entry(janela, width=16, font=("Helvetica", 32), justify="right",
                   bd=0, bg="#000000", fg="white", insertbackground="white")
entrada.grid(row=0, column=0, columnspan=4, padx=10, pady=20, ipady=20)

def calc():
    try:
        resultado = eval(entrada.get())
        entrada.delete(0, tk.END)
        entrada.insert(0, str(resultado))
    except:
        entrada.delete(0, tk.END)
        entrada.insert(0, "Erro")

def limpar():
    entrada.delete(0, tk.END)

def apagar():
    entrada.delete(len(entrada.get()) - 1, tk.END)

def tecla_pressionada(event):
    tecla = event.keysym
    if tecla in "0123456789":
        entrada.insert(tk.END, tecla)
    elif tecla in ["plus", "minus", "slash", "asterisk", "period"]:
        entrada.insert(tk.END, event.char)
    elif tecla == "Return":
        calc()
    elif tecla == "BackSpace":
        apagar()
    elif tecla == "Escape":
        limpar()

janela.bind("<Key>", tecla_pressionada)

COR_NUM = "#333333"
COR_FUNCAO = "#ff9500"
COR_AUX = "#a5a5a5"
COR_TEXTO_CLARO = "white"
COR_TEXTO_ESCURO = "black"

botoes = [
    ('C', limpar, COR_AUX, COR_TEXTO_ESCURO),
    ('⌫', apagar, COR_AUX, COR_TEXTO_ESCURO),
    ('%', lambda: entrada.insert(tk.END, '%'), COR_AUX, COR_TEXTO_ESCURO),
    ('/', lambda: entrada.insert(tk.END, '/'), COR_FUNCAO, COR_TEXTO_CLARO),
    
    ('7', lambda: entrada.insert(tk.END, '7'), COR_NUM, COR_TEXTO_CLARO),
    ('8', lambda: entrada.insert(tk.END, '8'), COR_NUM, COR_TEXTO_CLARO),
    ('9', lambda: entrada.insert(tk.END, '9'), COR_NUM, COR_TEXTO_CLARO),
    ('*', lambda: entrada.insert(tk.END, '*'), COR_FUNCAO, COR_TEXTO_CLARO),
    
    ('4', lambda: entrada.insert(tk.END, '4'), COR_NUM, COR_TEXTO_CLARO),
    ('5', lambda: entrada.insert(tk.END, '5'), COR_NUM, COR_TEXTO_CLARO),
    ('6', lambda: entrada.insert(tk.END, '6'), COR_NUM, COR_TEXTO_CLARO),
    ('-', lambda: entrada.insert(tk.END, '-'), COR_FUNCAO, COR_TEXTO_CLARO),
    
    ('1', lambda: entrada.insert(tk.END, '1'), COR_NUM, COR_TEXTO_CLARO),
    ('2', lambda: entrada.insert(tk.END, '2'), COR_NUM, COR_TEXTO_CLARO),
    ('3', lambda: entrada.insert(tk.END, '3'), COR_NUM, COR_TEXTO_CLARO),
    ('+', lambda: entrada.insert(tk.END, '+'), COR_FUNCAO, COR_TEXTO_CLARO),
    
    ('0', lambda: entrada.insert(tk.END, '0'), COR_NUM, COR_TEXTO_CLARO),
    ('.', lambda: entrada.insert(tk.END, '.'), COR_NUM, COR_TEXTO_CLARO),
    ('=', calc, COR_FUNCAO, COR_TEXTO_CLARO)
]

r = 1
c = 0
for item in botoes:
    texto, comando, cor_fundo, cor_texto = item
    colspan = 2 if texto == '0' else 1
    largura = 10 if texto == '0' else 5

    btn = tk.Button(janela, text=texto, command=comando,
                    font=("Helvetica", 20), width=largura, height=2,
                    bg=cor_fundo, fg=cor_texto, bd=0,
                    highlightthickness=0, relief="flat")
    btn.grid(row=r, column=c, columnspan=colspan, padx=5, pady=5, sticky="nsew")

    c += colspan
    if c > 3:
        c = 0
        r += 1

janela.mainloop()
