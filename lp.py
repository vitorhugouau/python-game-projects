import tkinter as tk
from tkinter import font
from urllib.request import urlopen
from io import BytesIO
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Landing Page Completa Tkinter")
root.geometry("900x700")
root.configure(bg="#f0f2f5")

# Centralizar janela na tela
window_width = 900
window_height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

# Fonts
title_font = font.Font(family="Helvetica", size=32, weight="bold")
subtitle_font = font.Font(family="Helvetica", size=14)
section_title_font = font.Font(family="Helvetica", size=20, weight="bold")
text_font = font.Font(family="Helvetica", size=12)
button_font = font.Font(family="Helvetica", size=14, weight="bold")
footer_font = font.Font(family="Helvetica", size=10)

# Cores
bg_color = "#f0f2f5"
primary_color = "#0078d7"
secondary_color = "#333"
text_color = "#222"
button_color = "#00aaff"
button_hover_color = "#0088cc"
section_bg_color = "#fff"
footer_bg_color = "#222"
footer_text_color = "#eee"

# --- HEADER ---
header_frame = tk.Frame(root, bg=bg_color, height=60)
header_frame.pack(fill="x", side="top")

logo = tk.Label(header_frame, text="MyBrand", font=title_font, fg=primary_color, bg=bg_color)
logo.pack(side="left", padx=20)

# Menu
menu_frame = tk.Frame(header_frame, bg=bg_color)
menu_frame.pack(side="right", padx=20)

for item in ["Home", "Serviços", "Depoimentos", "Contato"]:
    lbl = tk.Label(menu_frame, text=item, font=text_font, fg=secondary_color, bg=bg_color, cursor="hand2")
    lbl.pack(side="left", padx=15)

# --- SEÇÃO PRINCIPAL ---
main_section = tk.Frame(root, bg=section_bg_color, pady=40)
main_section.pack(fill="x")

left_text = tk.Frame(main_section, bg=section_bg_color)
left_text.pack(side="left", expand=True, padx=40)

title_label = tk.Label(left_text, text="Transforme seu negócio\ncom tecnologia de ponta", 
                       font=title_font, fg=text_color, bg=section_bg_color, justify="left")
title_label.pack(anchor="w")

subtitle_label = tk.Label(left_text, text="Ajudamos empresas a crescer e inovar com soluções digitais personalizadas.\n"
                                          "Simples, eficaz e com design excepcional.", 
                          font=subtitle_font, fg="#555", bg=section_bg_color, justify="left")
subtitle_label.pack(anchor="w", pady=15)

def cta_hover_enter(e):
    cta_button.config(bg=button_hover_color)

def cta_hover_leave(e):
    cta_button.config(bg=button_color)

cta_button = tk.Button(left_text, text="Comece Agora", font=button_font, bg=button_color, fg="white", bd=0,
                       padx=20, pady=10, cursor="hand2")
cta_button.pack(anchor="w")
cta_button.bind("<Enter>", cta_hover_enter)
cta_button.bind("<Leave>", cta_hover_leave)

# Imagem lado direito
right_image = tk.Frame(main_section, bg=section_bg_color)
right_image.pack(side="right", padx=40)

url = "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=500&q=80"
with urlopen(url) as u:
    raw_data = u.read()
im = Image.open(BytesIO(raw_data))
im = im.resize((400, 300), Image.LANCZOS)
photo = ImageTk.PhotoImage(im)

img_label = tk.Label(right_image, image=photo, bg=section_bg_color)
img_label.image = photo
img_label.pack()

# --- SEÇÃO DE SERVIÇOS ---
services_section = tk.Frame(root, bg=bg_color, pady=40)
services_section.pack(fill="x")

services_title = tk.Label(services_section, text="Nossos Serviços", font=section_title_font, fg=secondary_color, bg=bg_color)
services_title.pack(pady=(0, 30))

# Container de serviços
services_container = tk.Frame(services_section, bg=bg_color)
services_container.pack()

services = [
    ("🚀", "Desenvolvimento Ágil", "Projetos entregues rápido e com alta qualidade."),
    ("🎨", "Design Criativo", "Interfaces que encantam e facilitam a vida do usuário."),
    ("🔒", "Segurança", "Protegemos seus dados e sua privacidade acima de tudo."),
]

for icon, title, desc in services:
    card = tk.Frame(services_container, bg=section_bg_color, bd=1, relief="solid", padx=20, pady=20)
    card.pack(side="left", padx=15, ipadx=10, ipady=10)
    
    icon_label = tk.Label(card, text=icon, font=("Helvetica", 40), bg=section_bg_color)
    icon_label.pack()
    
    title_label = tk.Label(card, text=title, font=button_font, bg=section_bg_color, fg=text_color)
    title_label.pack(pady=(10,5))
    
    desc_label = tk.Label(card, text=desc, font=text_font, bg=section_bg_color, fg="#555", wraplength=200, justify="center")
    desc_label.pack()

# --- SEÇÃO DE DEPOIMENTOS ---
testimonials_section = tk.Frame(root, bg=section_bg_color, pady=40)
testimonials_section.pack(fill="x")

testimonials_title = tk.Label(testimonials_section, text="O que nossos clientes dizem", font=section_title_font, fg=secondary_color, bg=section_bg_color)
testimonials_title.pack(pady=(0,30))

testimonials = [
    ("João Silva", "⭐⭐⭐⭐⭐", "O time foi excepcional! Meu projeto saiu do papel e impactou o mercado rapidamente."),
    ("Maria Oliveira", "⭐⭐⭐⭐⭐", "Design impecável e funcionalidade que superou minhas expectativas."),
    ("Carlos Souza", "⭐⭐⭐⭐⭐", "Segurança total. Me sinto tranquilo sabendo que meus dados estão protegidos."),
]

for name, stars, text in testimonials:
    card = tk.Frame(testimonials_section, bg=bg_color, bd=1, relief="groove", padx=20, pady=15)
    card.pack(pady=5, padx=50, fill="x")
    
    name_label = tk.Label(card, text=f"{name} {stars}", font=button_font, bg=bg_color, fg=primary_color, anchor="w")
    name_label.pack(fill="x")
    
    text_label = tk.Label(card, text=text, font=text_font, bg=bg_color, fg="#444", wraplength=700, justify="left")
    text_label.pack()

# --- SEÇÃO CTA FINAL ---
final_cta = tk.Frame(root, bg=button_color, pady=40)
final_cta.pack(fill="x")

final_label = tk.Label(final_cta, text="Pronto para transformar seu negócio?\nVamos conversar!",
                       font=title_font, bg=button_color, fg="white", justify="center")
final_label.pack()

def final_cta_hover_enter(e):
    final_cta_button.config(bg=button_hover_color)

def final_cta_hover_leave(e):
    final_cta_button.config(bg="white", fg=button_color)

final_cta_button = tk.Button(final_cta, text="Entre em Contato", font=button_font, bg="white", fg=button_color, bd=0,
                             padx=30, pady=15, cursor="hand2")
final_cta_button.pack(pady=20)
final_cta_button.bind("<Enter>", final_cta_hover_enter)
final_cta_button.bind("<Leave>", final_cta_hover_leave)

# --- FOOTER ---
footer = tk.Frame(root, bg=footer_bg_color, height=60)
footer.pack(fill="x", side="bottom")

footer_label = tk.Label(footer, text="© 2025 MyBrand - Todos os direitos reservados",
                        font=footer_font, fg=footer_text_color, bg=footer_bg_color)
footer_label.pack(pady=20)

root.mainloop()
