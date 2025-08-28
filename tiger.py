import pygame
import random
import sys

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Roleta do Tigrinho")

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font_big = pygame.font.SysFont("Arial", 48, bold=True)
font_med = pygame.font.SysFont("Arial", 32)
font_small = pygame.font.SysFont("Arial", 22)

WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
ORANGE = (255, 140, 0)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
BLUE = (30, 144, 255)
GRAY = (180, 180, 180)

def load_image(path):
    try:
        return pygame.image.load(path).convert_alpha()
    except:
        print(f"Erro ao carregar imagem: {path}")
        sys.exit()

cards_names = ["leao", "tigre", "panda", "sapo", "macaco", "raposa"]
cards_imgs = [load_image(f"imagens/{name}.png") for name in cards_names]
tiger_img = load_image("imagens/tigre.png")

CARD_SIZE = (100, 100)
cards_imgs = [pygame.transform.smoothscale(img, CARD_SIZE) for img in cards_imgs]
tiger_img = pygame.transform.smoothscale(tiger_img, (150, 150))

roleta = [None, None, None]
result_text = ""
score = 0
spinning = False
spin_start_time = 0
SPIN_DURATION = 2000 
SPIN_SPEED = 100 

button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 100, 150, 50)

def draw_text(text, font, color, x, y, center=False):
    render = font.render(text, True, color)
    rect = render.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(render, rect)

def draw_button():
    color = GREEN if not spinning else GRAY
    pygame.draw.rect(screen, color, button_rect, border_radius=12)
    draw_text("GIRAR", font_med, WHITE, button_rect.centerx, button_rect.centery, center=True)

def draw_cards():
    start_x = WIDTH // 2 - (3 * CARD_SIZE[0] + 2 * 20) // 2
    y = HEIGHT // 2 - CARD_SIZE[1] // 2
    for i, card_idx in enumerate(roleta):
        rect = pygame.Rect(start_x + i * (CARD_SIZE[0] + 20), y, *CARD_SIZE)
        pygame.draw.rect(screen, BLUE, rect, border_radius=15)
        if card_idx is not None:
            screen.blit(cards_imgs[card_idx], rect.topleft)

def check_win():
    if roleta[0] is None:
        return False
    return roleta[0] == roleta[1] == roleta[2]

def draw_score():
    draw_text(f"Pontos: {score}", font_small, BLACK, 10, HEIGHT - 35)

def draw_tiger():
    screen.blit(tiger_img, (20, 20))
    draw_text("Tigrinho", font_med, ORANGE, 100, 60)

def main():
    global spinning, spin_start_time, result_text, score, roleta
    
    running = True
    while running:
        screen.fill(WHITE)
        draw_tiger()
        draw_cards()
        draw_button()
        draw_score()
        if result_text:
            cor = GREEN if result_text == "Você ganhou!" else RED
            draw_text(result_text, font_big, cor, WIDTH // 2, 80, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not spinning:
                if button_rect.collidepoint(event.pos):
                    spinning = True
                    spin_start_time = pygame.time.get_ticks()
                    result_text = ""

        if spinning:
            now = pygame.time.get_ticks()
            if (now - spin_start_time) % SPIN_SPEED < 30:
                roleta = [random.randint(0, len(cards_imgs) - 1) for _ in range(3)]

            if now - spin_start_time >= SPIN_DURATION:
                spinning = False
                if check_win():
                    result_text = "Você ganhou!"
                    score += 1
                else:
                    result_text = "Tente novamente!"

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
