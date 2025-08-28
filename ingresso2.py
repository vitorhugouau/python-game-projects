import tkinter as tk
from tkinter import ttk, messagebox

PRECO_BASE = 100.0
TIPOS_INGRESSO = {
    "Inteira": 1.0,
    "Meia": 0.5,
    "Idoso": 0.4,
    "Criança (menos de 10 anos)": 0.0
}

def calcular_preco():
    try:
        quantidade = int(entry_quantidade.get())
        if quantidade < 0:
            raise ValueError
        
        tipo = combo_tipo.get()
        if tipo not in TIPOS_INGRESSO:
            messagebox.showerror("Erro", "Selecione um tipo válido de ingresso.")
            return
        
        desconto = TIPOS_INGRESSO[tipo]
        preco_total = PRECO_BASE * desconto * quantidade
        
        messagebox.showinfo("Preço Total", 
                            f"Quantidade: {quantidade}\n"
                            f"Tipo: {tipo}\n"
                            f"Preço unitário: R$ {PRECO_BASE * desconto:.2f}\n"
                            f"Preço total: R$ {preco_total:.2f}")
    except ValueError:
        messagebox.showerror("Erro", "Informe uma quantidade válida (número inteiro positivo).")

root = tk.Tk()
root.title("Calculadora de Preço de Ingressos")
root.geometry("400x280")
root.configure(bg="#1f1f2e")

style = ttk.Style(root)
style.theme_use("clam")

style.configure("TLabel",
                background="#1f1f2e",
                foreground="#e0e0e0",
                font=("Segoe UI", 13))
style.configure("TEntry",
                font=("Segoe UI", 14),
                foreground="#333")
style.configure("TCombobox",
                font=("Segoe UI", 14),
                foreground="#333")
style.configure("TButton",
                font=("Segoe UI Semibold", 15),
                padding=10,
                background="#3a3f58",
                foreground="#e0e0e0")
style.map("TButton",
          background=[('active', '#575f85')],
          foreground=[('active', '#ffffff')])

frame = ttk.Frame(root, padding=30, style="TFrame")
frame.pack(expand=True, fill="both")

label_qtd = ttk.Label(frame, text="Quantidade de ingressos:")
label_qtd.pack(anchor="w", pady=(0, 8))

entry_quantidade = ttk.Entry(frame, width=20)
entry_quantidade.pack(fill="x", pady=(0, 20))

label_tipo = ttk.Label(frame, text="Tipo de ingresso:")
label_tipo.pack(anchor="w", pady=(0, 8))

combo_tipo = ttk.Combobox(frame, values=list(TIPOS_INGRESSO.keys()))
combo_tipo.pack(fill="x", pady=(0, 25))
combo_tipo.set("Selecione")

botao = ttk.Button(frame, text="Calcular Preço", command=calcular_preco)
botao.pack(fill="x")

footer = tk.Label(root, text="Feito com ❤ por você", bg="#1f1f2e", fg="#555a70", font=("Segoe UI Italic", 10))
footer.pack(side="bottom", pady=10)

root.mainloop()
