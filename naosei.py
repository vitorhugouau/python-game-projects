import os
import math
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas

W, H = 1200, 675
OUT_FILE = "modelos_servico_nuvem_ultra_perfeito.pdf"
LOGO_FILE = "aws-logo.png"

slides = [
    {"title": "IaaS", "subtitle": "Infraestrutura como Serviço",
     "desc": "Mais controle sobre servidores, redes e armazenamento de TI.",
     "color": (15,23,42), "icon":"server"},
    {"title": "PaaS", "subtitle": "Plataforma como Serviço",
     "desc": "Equilíbrio: desenvolve apps sem gerenciar a infra subjacente.",
     "color": (6,95,70), "icon":"gear"},
    {"title": "SaaS", "subtitle": "Software como Serviço",
     "desc": "Menos controle: aplicações prontas, acessíveis via navegador.",
     "color": (180,83,9), "icon":"mobile"},
]

FONT_BOLD = ImageFont.truetype("arialbd.ttf", 60)
FONT_SUB = ImageFont.truetype("arialbd.ttf", 36)
FONT_DESC = ImageFont.truetype("arial.ttf", 24)
FONT_ARROW = ImageFont.truetype("arialbd.ttf", 28)

def draw_gradient(draw, w, h, start, end):
    for i in range(h):
        ratio = i / h
        r = int(start[0] + (end[0]-start[0])*ratio)
        g = int(start[1] + (end[1]-start[1])*ratio)
        b = int(start[2] + (end[2]-start[2])*ratio)
        draw.line([(0,i),(w,i)], fill=(r,g,b))

def draw_rounded_card(draw, xy, size, radius, fill):
    x0, y0 = xy
    w, h = size
    draw.rounded_rectangle([x0,y0,x0+w,y0+h], radius, fill=fill)

def draw_icon(draw, icon, center, size):
    cx, cy = center
    if icon=="server":
        for i in range(3):
            draw.rectangle([cx-60, cy-30+i*30, cx+60, cy-20+i*30], fill="white")
    elif icon=="gear":
        draw.ellipse([cx-30, cy-30, cx+30, cy+30], fill="white")
        for angle in range(0,360,45):
            rad = math.radians(angle)
            x = cx + 50*math.cos(rad)
            y = cy + 50*math.sin(rad)
            draw.rectangle([x-8, y-8, x+8, y+8], fill="white")
    elif icon=="mobile":
        draw.rounded_rectangle([cx-30, cy-60, cx+30, cy+60], radius=10, fill="white")
        draw.ellipse([cx-6, cy+50, cx+6, cy+62], fill=(224,232,240))

def draw_arrow(draw, y, w):
    draw.line([(w*0.1,y),(w*0.9,y)], fill=(255,153,0), width=8)
    draw.polygon([(w*0.9,y),(w*0.88,y-10),(w*0.88,y+10)], fill=(255,153,0))
    draw.text((w*0.05,y-20), "Mais controle", fill="white", font=FONT_ARROW)
    draw.text((w*0.95-180,y-20), "Menos controle", fill="white", font=FONT_ARROW)

def create_slide(slide):
    img = Image.new("RGB", (W,H), (0,0,0))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, W, H, (5,10,22), (6,28,56))
    card_w, card_h = W*0.7, H*0.6
    card_x, card_y = (W-card_w)//2, (H-card_h)//2
    draw_rounded_card(draw, (card_x, card_y), (card_w, card_h), 30, slide["color"])
    draw_icon(draw, slide["icon"], (W//2, card_y + 150), 72)
    draw.text((W//2, card_y + card_h - 180), slide["title"], fill="white", font=FONT_BOLD, anchor="ms")
    draw.text((W//2, card_y + card_h - 240), slide["subtitle"], fill="white", font=FONT_SUB, anchor="ms")
    draw.text((W//2, card_y + card_h - 300), slide["desc"], fill="white", font=FONT_DESC, anchor="ms")
    draw_arrow(draw, 80, W)
    if os.path.isfile(LOGO_FILE):
        logo = Image.open(LOGO_FILE).convert("RGBA")
        logo.thumbnail((120,120))
        img.paste(logo, (W-150,H-150), logo)
    return img

def main():
    slides_imgs = [create_slide(s) for s in slides]
    c = canvas.Canvas(OUT_FILE, pagesize=(W,H))
    for im in slides_imgs:
        tmp = "tmp_slide.png"
        im.save(tmp)
        c.drawImage(tmp,0,0,width=W,height=H)
        c.showPage()
        os.remove(tmp)
    c.save()
    print("PDF ULTRA PREMIUM CRIADO:", OUT_FILE)

if __name__=="__main__":
    main()
