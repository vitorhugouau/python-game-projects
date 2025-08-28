import pygame
import random
import sys

pygame.init()
pygame.display.set_caption("Campo Minado")

WIDTH, HEIGHT = 600, 600
LINHAS, COLUNAS = 10, 10
TAMANHO = WIDTH // COLUNAS
MINAS = 15

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
CINZA_CLARO = (200, 200, 200)
CINZA_ESCURO = (100, 100, 100)

tela = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 30)

def gerar_minas():
    minas = set()
    while len(minas) < MINAS:
        pos = (random.randint(0, LINHAS-1), random.randint(0, COLUNAS-1))
        minas.add(pos)
    return minas

def contar_minas_vizinhas(linha, coluna, minas):
    count = 0
    for x in range(linha-1, linha+2):
        for y in range(coluna-1, coluna+2):
            if (x, y) in minas and (x, y) != (linha, coluna):
                count += 1
    return count

def criar_tabuleiro(minas):
    tabuleiro = [[0]*COLUNAS for _ in range(LINHAS)]
    for (x,y) in minas:
        tabuleiro[x][y] = -1

    for i in range(LINHAS):
        for j in range(COLUNAS):
            if tabuleiro[i][j] == -1:
                continue
            tabuleiro[i][j] = contar_minas_vizinhas(i, j, minas)
    return tabuleiro

def texto_central(texto, fonte, cor, tela, y_offset=0):
    surface = fonte.render(texto, True, cor)
    rect = surface.get_rect(center=(WIDTH//2, HEIGHT//2 + y_offset))
    tela.blit(surface, rect)

def revelar_vazio(tabuleiro, aberto, linha, coluna):
    if aberto[linha][coluna]:
        return
    aberto[linha][coluna] = True
    if tabuleiro[linha][coluna] == 0:
        for x in range(max(0, linha-1), min(LINHAS, linha+2)):
            for y in range(max(0, coluna-1), min(COLUNAS, coluna+2)):
                if not aberto[x][y]:
                    revelar_vazio(tabuleiro, aberto, x, y)

def main():
    minas = gerar_minas()
    tabuleiro = criar_tabuleiro(minas)
    aberto = [[False]*COLUNAS for _ in range(LINHAS)]
    marcado = [[False]*COLUNAS for _ in range(LINHAS)]
    game_over = False
    venceu = False

    while True:
        tela.fill(CINZA_CLARO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not game_over and not venceu:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    linha = y // TAMANHO
                    coluna = x // TAMANHO

                    if evento.button == 1:
                        if not marcado[linha][coluna]:
                            aberto[linha][coluna] = True
                            if tabuleiro[linha][coluna] == -1:
                                game_over = True
                            elif tabuleiro[linha][coluna] == 0:
                                revelar_vazio(tabuleiro, aberto, linha, coluna)

                    elif evento.button == 3:
                        if not aberto[linha][coluna]:
                            marcado[linha][coluna] = not marcado[linha][coluna]

            else:
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                    minas = gerar_minas()
                    tabuleiro = criar_tabuleiro(minas)
                    aberto = [[False]*COLUNAS for _ in range(LINHAS)]
                    marcado = [[False]*COLUNAS for _ in range(LINHAS)]
                    game_over = False
                    venceu = False

        if not game_over:
            total_abertos = sum([row.count(True) for row in aberto])
            if total_abertos == LINHAS*COLUNAS - MINAS:
                venceu = True

        for i in range(LINHAS):
            for j in range(COLUNAS):
                rect = pygame.Rect(j*TAMANHO, i*TAMANHO, TAMANHO, TAMANHO)
                if aberto[i][j]:
                    pygame.draw.rect(tela, CINZA_ESCURO, rect)
                    if tabuleiro[i][j] > 0:
                        num_text = font.render(str(tabuleiro[i][j]), True, AZUL)
                        tela.blit(num_text, (j*TAMANHO + TAMANHO//3, i*TAMANHO + TAMANHO//5))
                    elif tabuleiro[i][j] == -1:
                        pygame.draw.circle(tela, VERMELHO, rect.center, TAMANHO//3)
                else:
                    pygame.draw.rect(tela, CINZA_CLARO, rect)
                    if marcado[i][j]:
                        pygame.draw.polygon(tela, VERMELHO, [
                            (rect.left + TAMANHO//4, rect.top + TAMANHO//5),
                            (rect.left + TAMANHO//4, rect.bottom - TAMANHO//5),
                            (rect.right - TAMANHO//4, rect.centery)
                        ])
                    pygame.draw.rect(tela, PRETO, rect, 2)

        if game_over:
            texto_central("Game Over! Pressione R para reiniciar", font, VERMELHO, tela)
        if venceu:
            texto_central("Parabéns! Você venceu! Pressione R para jogar novamente", font, (0, 150, 0), tela)

        pygame.display.flip()

if __name__ == "__main__":
    main()
