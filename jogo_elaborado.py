import pygame
import sys

pygame.init()
pygame.mixer.init()

LARGURA, ALTURA = 900, 600
FPS = 60

BG_COLOR = (12, 12, 30)
BRANCO = (245, 245, 245)
VERDE = (65, 220, 130)
VERMELHO = (220, 80, 80)
AZUL = (70, 130, 220)
CINZA_CLARO = (180, 180, 200)
AMARELO = (230, 210, 90)

font_title = pygame.font.SysFont('Segoe UI Black', 72)
font_menu = pygame.font.SysFont('Segoe UI', 36)
font_score = pygame.font.SysFont('Segoe UI', 64, bold=True)
font_info = pygame.font.SysFont('Segoe UI', 24)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("PING PONG PRO - 2025 Edition")
clock = pygame.time.Clock()

class Raquete:
    def __init__(self, x, y, cor):
        self.width, self.height = 20, 120
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.color = cor
        self.speed = 7
        self.energy = 100

    def mover(self, cima, baixo):
        keys = pygame.key.get_pressed()
        if keys[cima] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[baixo] and self.rect.bottom < ALTURA:
            self.rect.y += self.speed

    def mover_ia(self, bola, dificuldade):
        if self.rect.centery < bola.rect.centery:
            self.rect.y += self.speed * dificuldade * 0.75
        elif self.rect.centery > bola.rect.centery:
            self.rect.y -= self.speed * dificuldade * 0.75
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > ALTURA:
            self.rect.bottom = ALTURA

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=15)
        energy_height = int((self.energy / 100) * self.height)
        energy_rect = pygame.Rect(self.rect.x - 12 if self.color == VERDE else self.rect.right + 2,
                                  self.rect.bottom - energy_height, 8, energy_height)
        pygame.draw.rect(surface, AMARELO, energy_rect, border_radius=4)

class Bola:
    def __init__(self):
        self.size = 25
        self.rect = pygame.Rect(LARGURA//2 - self.size//2, ALTURA//2 - self.size//2, self.size, self.size)
        self.speed_x = 7
        self.speed_y = 7
        self.max_speed = 14
        self.speed_increase = 0.3

    def mover(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= ALTURA:
            self.speed_y *= -1

    def draw(self, surface):
        pygame.draw.ellipse(surface, BRANCO, self.rect)
        glow = pygame.Surface((self.size + 10, self.size + 10), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (255, 255, 255, 50), glow.get_rect())
        surface.blit(glow, (self.rect.x - 5, self.rect.y - 5), special_flags=pygame.BLEND_RGBA_ADD)

    def reset(self, direction=1):
        self.rect.center = (LARGURA//2, ALTURA//2)
        self.speed_x = 7 * direction
        self.speed_y = 7 * (1 if direction > 0 else -1)

    def aumentar_velocidade(self):
        if abs(self.speed_x) < self.max_speed:
            self.speed_x += self.speed_increase * (1 if self.speed_x > 0 else -1)
        if abs(self.speed_y) < self.max_speed:
            self.speed_y += self.speed_increase * (1 if self.speed_y > 0 else -1)

def desenha_texto(surface, texto, fonte, cor, pos):
    render = fonte.render(texto, True, cor)
    rect = render.get_rect(center=pos)
    surface.blit(render, rect)

def desenha_linha_central(surface):
    for y in range(0, ALTURA, 35):
        if y % 70 == 0:
            pygame.draw.rect(surface, CINZA_CLARO, (LARGURA//2 - 5, y, 10, 30), border_radius=8)

def menu_principal():
    opcoes = ["Iniciar Jogo", "Dificuldade: Fácil", "Sair"]
    selecionado = 0
    dificuldade = 1

    while True:
        clock.tick(FPS)
        tela.fill(BG_COLOR)
        desenha_texto(tela, "PING PONG PRO", font_title, BRANCO, (LARGURA//2, 150))
        desenha_texto(tela, "Use ↑↓ e ENTER para escolher", font_info, CINZA_CLARO, (LARGURA//2, 200))

        for i, opcao in enumerate(opcoes):
            cor = AMARELO if i == selecionado else CINZA_CLARO
            desenha_texto(tela, opcao, font_menu, cor, (LARGURA//2, 300 + i * 60))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                elif evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                elif evento.key == pygame.K_RETURN:
                    if selecionado == 0:
                        return dificuldade
                    elif selecionado == 1:
                        dificuldade = (dificuldade % 3) + 1
                        dif_text = {1: "Fácil", 2: "Médio", 3: "Difícil"}
                        opcoes[1] = f"Dificuldade: {dif_text[dificuldade]}"
                    elif selecionado == 2:
                        pygame.quit()
                        sys.exit()

def tela_vitoria(vencedor):
    rodando = True
    while rodando:
        clock.tick(FPS)
        tela.fill(BG_COLOR)
        msg = "Jogador Verde Venceu!" if vencedor == "verde" else "Jogador Vermelho Venceu!"
        desenha_texto(tela, "FIM DE JOGO", font_title, AMARELO, (LARGURA//2, ALTURA//3))
        desenha_texto(tela, msg, font_score, BRANCO, (LARGURA//2, ALTURA//2))
        desenha_texto(tela, "Pressione ENTER para voltar ao menu", font_info, CINZA_CLARO, (LARGURA//2, ALTURA * 2//3))
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                rodando = False

def main():
    dificuldade = menu_principal()

    raquete_esq = Raquete(30, ALTURA//2 - 60, VERDE)
    raquete_dir = Raquete(LARGURA - 50, ALTURA//2 - 60, VERMELHO)
    bola = Bola()

    placar_esq = 0
    placar_dir = 0

    rodando = True
    while rodando:
        clock.tick(FPS)
        tela.fill(BG_COLOR)
        desenha_linha_central(tela)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        raquete_esq.mover(pygame.K_w, pygame.K_s)

        raquete_dir.mover_ia(bola, dificuldade)

        bola.mover()

        if bola.rect.colliderect(raquete_esq.rect) and bola.speed_x < 0:
            bola.speed_x *= -1
            bola.aumentar_velocidade()
        if bola.rect.colliderect(raquete_dir.rect) and bola.speed_x > 0:
            bola.speed_x *= -1
            bola.aumentar_velocidade()

        if bola.rect.left <= 0:
            placar_dir += 1
            bola.reset(direction=-1)
        if bola.rect.right >= LARGURA:
            placar_esq += 1
            bola.reset(direction=1)

        raquete_esq.draw(tela)
        raquete_dir.draw(tela)
        bola.draw(tela)

        desenha_texto(tela, f"{placar_esq}", font_score, VERDE, (LARGURA//4, 50))
        desenha_texto(tela, f"{placar_dir}", font_score, VERMELHO, (LARGURA * 3//4, 50))

        if placar_esq == 10:
            tela_vitoria("verde")
            dificuldade = menu_principal()
            placar_esq = placar_dir = 0
            bola.reset()
            raquete_esq.rect.centery = ALTURA//2
            raquete_dir.rect.centery = ALTURA//2
        if placar_dir == 10:
            tela_vitoria("vermelho")
            dificuldade = menu_principal()
            placar_esq = placar_dir = 0
            bola.reset()
            raquete_esq.rect.centery = ALTURA//2
            raquete_dir.rect.centery = ALTURA//2

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
