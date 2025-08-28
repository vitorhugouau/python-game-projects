import tkinter as tk
from tkinter import ttk, messagebox

# Preço base para cada destino
DESTINOS = {
    "São Paulo": 500.0,
    "Rio de Janeiro": 450.0,
    "Salvador": 700.0,
    "Manaus": 850.0
}

# Multiplicadores por tipo de assento
TIPOS_ASSENTO = {
    "Primeira Classe": 1.8,   # +80% do preço base
    "Executiva": 1.3,         # +30% do preço base
    "Econômica": 1.0          # preço base
}

def calcular_valor():
    destino = combo_destino.get()
    tipo_assento = var_assento.get()

    # Verifica se as opções foram selecionadas corretamente
    if destino not in DESTINOS:
        messagebox.showerror("Erro", "Selecione um destino válido.")
        return
    if tipo_assento not in TIPOS_ASSENTO:
        messagebox.showerror("Erro", "Selecione o tipo de assento.")
        return

    preco_base = DESTINOS[destino]
    multiplicador = TIPOS_ASSENTO[tipo_assento]
    preco_final = preco_base * multiplicador

    # Exibe o resultado formatado com duas casas decimais
    messagebox.showinfo("Valor da Passagem",
                        f"Destino: {destino}\n"
                        f"Assento: {tipo_assento}\n"
                        f"Valor: R$ {preco_final:.2f}")

# Configuração da janela principal
root = tk.Tk()
root.title("Calculadora de Valor de Passagem")
root.geometry("400x320")
root.configure(bg="#2c2f4a")

# Estilos para deixar bonito
style = ttk.Style(root)
style.theme_use("clam")
style.configure("TLabel", background="#2c2f4a", foreground="#f0f0f0", font=("Segoe UI", 13))
style.configure("TCombobox", font=("Segoe UI", 14))
style.configure("TRadiobutton", background="#2c2f4a", foreground="#f0f0f0", font=("Segoe UI", 12))
style.configure("TButton", font=("Segoe UI Semibold", 14), padding=10)
style.map("TButton", background=[('active', '#555f87')], foreground=[('active', '#ffffff')])

# Frame principal para organizar
frame = ttk.Frame(root, padding=30, style="TFrame")
frame.pack(expand=True, fill="both")

# Label e Combobox para o destino
ttk.Label(frame, text="Escolha o destino:").pack(anchor="w", pady=(0, 8))
combo_destino = ttk.Combobox(frame, values=list(DESTINOS.keys()), state="readonly")
combo_destino.pack(fill="x", pady=(0, 20))
combo_destino.set("Selecione")

# Label para o tipo de assento e botões rádio
ttk.Label(frame, text="Tipo de assento:").pack(anchor="w", pady=(0, 8))
var_assento = tk.StringVar(value="")

for tipo in TIPOS_ASSENTO.keys():
    ttk.Radiobutton(frame, text=tipo, value=tipo, variable=var_assento).pack(anchor="w", pady=4)

# Botão para calcular o valor da passagem
btn_calcular = ttk.Button(frame, text="Calcular Valor", command=calcular_valor)
btn_calcular.pack(fill="x", pady=25)

# Rodapé estiloso
footer = tk.Label(root, text="Feito com ❤ por você", bg="#2c2f4a", fg="#888aaa", font=("Segoe UI Italic", 10))
footer.pack(side="bottom", pady=10)

root.mainloop()
