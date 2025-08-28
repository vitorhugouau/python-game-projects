import pygame
import sys
import random
import math

pygame.init()

LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo com voo e inimigos perseguidores")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 24)
GAME_OVER_FONT = pygame.font.SysFont("Arial", 48, bold=True)

BG_COLOR = (20, 20, 40)
PLAYER_COLOR = (200, 50, 50)
BALL_COLOR = (255, 215, 0)
ENEMY_COLOR = (200, 0, 0)
TEXT_COLOR = (255, 255, 255)

player_pos = pygame.Vector2(LARGURA // 2, ALTURA // 2)
player_size = pygame.Vector2(50, 50)
player_speed = 5

NUM_BALLS = 10
BALL_RADIUS = 10
balls = []

BASE_NUM_ENEMIES = 3
MAX_ENEMIES = 15
ENEMY_RADIUS = 15
enemies = []

BASE_ENEMY_SPEED = 1.5
MAX_ENEMY_SPEED = 5

score = 0
game_over = False

def gerar_bolinhas():
    global balls
    balls = []
    for _ in range(NUM_BALLS):
        x = random.randint(BALL_RADIUS, LARGURA - BALL_RADIUS)
        y = random.randint(BALL_RADIUS, ALTURA // 2)
        balls.append(pygame.Vector2(x, y))

def gerar_inimigos(num_enemies):
    global enemies
    enemies = []
    for _ in range(num_enemies):
        x = random.randint(ENEMY_RADIUS, LARGURA - ENEMY_RADIUS)
        y = random.randint(ALTURA // 2 + ENEMY_RADIUS, ALTURA - ENEMY_RADIUS)
        enemies.append({'pos': pygame.Vector2(x, y), 'speed': BASE_ENEMY_SPEED})

def desenha_bolinhas():
    for bola in balls:
        pygame.draw.circle(tela, BALL_COLOR, (int(bola.x), int(bola.y)), BALL_RADIUS)

def desenha_inimigos():
    for inimigo in enemies:
        pos = inimigo['pos']
        pygame.draw.circle(tela, ENEMY_COLOR, (int(pos.x), int(pos.y)), ENEMY_RADIUS)

def checa_colisao():
    global balls, score, game_over
    jogador_rect = pygame.Rect(player_pos.x, player_pos.y, player_size.x, player_size.y)

    bolas_para_remover = []
    for bola in balls:
        bola_rect = pygame.Rect(bola.x - BALL_RADIUS, bola.y - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)
        if jogador_rect.colliderect(bola_rect):
            bolas_para_remover.append(bola)
            score += 1
    for bola in bolas_para_remover:
        balls.remove(bola)
    if len(balls) == 0:
        gerar_bolinhas()

    for inimigo in enemies:
        inimigo_pos = inimigo['pos']
        inimigo_rect = pygame.Rect(inimigo_pos.x - ENEMY_RADIUS, inimigo_pos.y - ENEMY_RADIUS, ENEMY_RADIUS*2, ENEMY_RADIUS*2)
        if jogador_rect.colliderect(inimigo_rect):
            game_over = True

def move_inimigos():
    for inimigo in enemies:
        pos = inimigo['pos']

        direcao = player_pos - pos
        distancia = direcao.length()
        if distancia != 0:
            direcao = direcao.normalize()
        else:
            direcao = pygame.Vector2(0, 0)

        velocidade = inimigo['speed']

        pos.x += direcao.x * velocidade
        pos.y += direcao.y * velocidade

        pos.x = max(ENEMY_RADIUS, min(pos.x, LARGURA - ENEMY_RADIUS))
        pos.y = max(ENEMY_RADIUS, min(pos.y, ALTURA - ENEMY_RADIUS))

def atualiza_dificuldade():
    num_enemies = min(BASE_NUM_ENEMIES + score // 5, MAX_ENEMIES)
    if len(enemies) < num_enemies:
        for _ in range(num_enemies - len(enemies)):
            x = random.randint(ENEMY_RADIUS, LARGURA - ENEMY_RADIUS)
            y = random.randint(ALTURA // 2 + ENEMY_RADIUS, ALTURA - ENEMY_RADIUS)
            enemies.append({'pos': pygame.Vector2(x, y), 'speed': BASE_ENEMY_SPEED})

    velocidade_nova = min(BASE_ENEMY_SPEED + (score * 0.1), MAX_ENEMY_SPEED)
    for inimigo in enemies:
        inimigo['speed'] = velocidade_nova

def desenha_score():
    texto = FONT.render(f"Pontuação: {score}", True, TEXT_COLOR)
    tela.blit(texto, (10, 10))

def desenha_jogador():
    pygame.draw.rect(tela, PLAYER_COLOR, (player_pos.x, player_pos.y, player_size.x, player_size.y), border_radius=10)

def desenha_game_over():
    texto1 = GAME_OVER_FONT.render("Game Over!", True, (255, 0, 0))
    texto2 = FONT.render("Pressione Enter para reiniciar", True, TEXT_COLOR)
    tela.blit(texto1, (LARGURA//2 - texto1.get_width()//2, ALTURA//2 - texto1.get_height()))
    tela.blit(texto2, (LARGURA//2 - texto2.get_width()//2, ALTURA//2 + 10))

def main():
    global score, game_over, player_pos

    score = 0
    game_over = False
    player_pos.update(LARGURA // 2, ALTURA // 2)
    gerar_bolinhas()
    gerar_inimigos(BASE_NUM_ENEMIES)

    rodando = True
    while rodando:
        clock.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if game_over and evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    score = 0
                    game_over = False
                    player_pos.update(LARGURA // 2, ALTURA // 2)
                    gerar_bolinhas()
                    enemies.clear()
                    gerar_inimigos(BASE_NUM_ENEMIES)

        if not game_over:
            teclas = pygame.key.get_pressed()

            if teclas[pygame.K_LEFT]:
                player_pos.x -= player_speed
            if teclas[pygame.K_RIGHT]:
                player_pos.x += player_speed
            if teclas[pygame.K_UP]:
                player_pos.y -= player_speed
            if teclas[pygame.K_DOWN]:
                player_pos.y += player_speed

            player_pos.x = max(0, min(player_pos.x, LARGURA - player_size.x))
            player_pos.y = max(0, min(player_pos.y, ALTURA - player_size.y))

            atualiza_dificuldade()

            move_inimigos()

            checa_colisao()

        tela.fill(BG_COLOR)
        desenha_bolinhas()
        desenha_inimigos()
        desenha_jogador()
        desenha_score()

        if game_over:
            desenha_game_over()

        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
