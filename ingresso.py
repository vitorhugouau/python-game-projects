import tkinter as tk
from tkinter import messagebox, font

class IngressoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎟️ Calculadora de Ingressos")
        self.root.geometry("450x570")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)

        self.preco_base = 100.0

        self.title_font = font.Font(family="Segoe UI", size=22, weight="bold")
        self.label_font = font.Font(family="Segoe UI", size=12)
        self.input_font = font.Font(family="Segoe UI", size=14)
        self.button_font = font.Font(family="Segoe UI", size=14, weight="bold")
        self.result_font = font.Font(family="Consolas", size=12)

        self.title_label = tk.Label(self.root, text="🎫 Ingressos VIP - Multi Tipo",
                                    fg="#7986cb", bg="#121212", font=self.title_font)
        self.title_label.pack(pady=(20, 10))

        preco_label = tk.Label(self.root, text=f"Preço Base do Ingresso: R$ {self.preco_base:.2f}",
                               fg="#c5cae9", bg="#121212", font=self.label_font)
        preco_label.pack(pady=(0, 20))

        self.frame_inputs = tk.Frame(self.root, bg="#121212")
        self.frame_inputs.pack(pady=5)

        self.ingressos_vars = {}
        tipos = [
            ("Inteira (100%)", "inteira"),
            ("Meia (50%)", "meia"),
            ("Idoso (40%)", "idoso"),
            ("Criança < 10 anos (Grátis)", "crianca")
        ]

        for texto, key in tipos:
            frame = tk.Frame(self.frame_inputs, bg="#121212")
            frame.pack(fill="x", pady=8, padx=30)

            label = tk.Label(frame, text=texto, fg="#e8eaf6", bg="#121212", font=self.label_font)
            label.pack(side="left")

            var = tk.StringVar(value="0")
            entry = tk.Entry(frame, textvariable=var, font=self.input_font, width=6,
                             bg="#303f9f", fg="white", relief="flat", justify="center", insertbackground="white")
            entry.pack(side="right", padx=10, ipady=5)
            entry.bind("<FocusIn>", lambda e, ent=entry: ent.config(bg="#3f51b5"))
            entry.bind("<FocusOut>", lambda e, ent=entry: ent.config(bg="#303f9f"))

            self.ingressos_vars[key] = var

        self.calc_btn = tk.Button(self.root, text="Calcular Valor Total 💰",
                                  bg="#3f51b5", fg="white", font=self.button_font,
                                  relief="flat", cursor="hand2", activebackground="#5c6bc0",
                                  command=self.calcular)
        self.calc_btn.pack(pady=30, ipadx=15, ipady=8)
        self.calc_btn.bind("<Enter>", lambda e: self.calc_btn.config(bg="#5c6bc0"))
        self.calc_btn.bind("<Leave>", lambda e: self.calc_btn.config(bg="#3f51b5"))

        self.frame_result = tk.Frame(self.root, bg="#121212")
        self.frame_result.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.result_text = tk.Text(self.frame_result, height=14, font=self.result_font,
                                   bg="#263238", fg="#80cbc4", relief="flat", padx=10, pady=10,
                                   state="disabled", wrap="word")
        self.result_text.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.frame_result, command=self.result_text.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.result_text.config(yscrollcommand=self.scrollbar.set)

    def calcular(self):
        try:
            inteira = int(self.ingressos_vars["inteira"].get())
            meia = int(self.ingressos_vars["meia"].get())
            idoso = int(self.ingressos_vars["idoso"].get())
            crianca = int(self.ingressos_vars["crianca"].get())
            if any(x < 0 for x in [inteira, meia, idoso, crianca]):
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira números inteiros não negativos.")
            return

        total_ingressos = inteira + meia + idoso + crianca
        if total_ingressos == 0:
            messagebox.showwarning("Aviso", "Informe ao menos um ingresso.")
            return

        preco_total = (inteira * self.preco_base +
                       meia * self.preco_base * 0.5 +
                       idoso * self.preco_base * 0.4 +
                       crianca * 0)

        texto = (
            f"Detalhes da Compra:\n"
            f"------------------------------------\n"
            f"Inteira  x{inteira}: R$ {inteira * self.preco_base:.2f}\n"
            f"Meia     x{meia}: R$ {meia * self.preco_base * 0.5:.2f}\n"
            f"Idoso    x{idoso}: R$ {idoso * self.preco_base * 0.4:.2f}\n"
            f"Criança  x{crianca}: R$ 0.00\n"
            f"------------------------------------\n"
            f"Total de Ingressos: {total_ingressos}\n"
            f"VALOR TOTAL: R$ {preco_total:.2f}"
        )

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, texto)
        self.result_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = IngressoApp(root)
    root.mainloop()
