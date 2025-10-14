import tkinter as tk
from tkinter import ttk, messagebox

DESTINOS = {
    "São Paulo": 500.0,
    "Rio de Janeiro": 450.0,
    "Salvador": 700.0,
    "Manaus": 850.0
}

TIPOS_ASSENTO = {
    "Primeira Classe": 1.8,
    "Executiva": 1.3,
    "Econômica": 1.0
}

def calcular_valor():
    destino = combo_destino.get()
    assento = var_assento.get()

    if destino not in DESTINOS:
        messagebox.showerror("Erro", "Selecione um destino válido.")
        return
    if assento not in TIPOS_ASSENTO:
        messagebox.showerror("Erro", "Selecione um tipo de assento.")
        return

    preco_base = DESTINOS[destino]
    multiplicador = TIPOS_ASSENTO[assento]
    preco_final = preco_base * multiplicador

    messagebox.showinfo("Valor da Passagem",
                        f"Destino: {destino}\n"
                        f"Assento: {assento}\n"
                        f"Valor: R$ {preco_final:.2f}")

root = tk.Tk()
root.title("Calculadora de Passagem")
root.geometry("400x350")
root.configure(bg="#282c34")

style = ttk.Style(root)
style.theme_use("clam")
style.configure("TLabel", background="#282c34", foreground="#ffffff", font=("Segoe UI", 13))
style.configure("TCombobox", font=("Segoe UI", 14))
style.configure("TRadiobutton", background="#282c34", foreground="#ffffff", font=("Segoe UI", 12))
style.configure("TButton", font=("Segoe UI Semibold", 16), padding=12)
style.map("TButton",
          background=[('active', '#61afef')],
          foreground=[('active', '#282c34')])

frame = ttk.Frame(root, padding=25, style="TFrame")
frame.pack(expand=True, fill="both")

ttk.Label(frame, text="Escolha o destino:").pack(anchor="w", pady=(0, 10))
combo_destino = ttk.Combobox(frame, values=list(DESTINOS.keys()), state="readonly")
combo_destino.pack(fill="x", pady=(0, 20))
combo_destino.set("Selecione")

ttk.Label(frame, text="Tipo de assento:").pack(anchor="w", pady=(0, 10))
var_assento = tk.StringVar(value="")

for tipo in TIPOS_ASSENTO:
    ttk.Radiobutton(frame, text=tipo, value=tipo, variable=var_assento).pack(anchor="w", pady=5)

botao_calcular = ttk.Button(frame, text="Calcular Valor", command=calcular_valor)
botao_calcular.pack(fill="x", pady=30)

footer = tk.Label(root, text="Feito com ❤ por você", bg="#282c34", fg="#7f848e", font=("Segoe UI Italic", 10))
footer.pack(side="bottom", pady=10)

root.mainloop()
