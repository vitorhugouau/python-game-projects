import pygame
import numpy as np
import colorsys
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visualizador Mandelbrot Interativo")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 18)

max_iter = 80
zoom = 1.0
offset_x, offset_y = -0.6, 0.0

dragging = False
start_pos = None
end_pos = None

def mandelbrot(c, max_iter):
    z = 0
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter, time_factor):
    pixels = np.zeros((height, width, 3), dtype=np.uint8)
    for ix in range(width):
        for iy in range(height):
            x = xmin + (xmax - xmin) * ix / width
            y = ymin + (ymax - ymin) * iy / height
            c = complex(x, y)
            m = mandelbrot(c, max_iter)
            
            hue = (m / max_iter + time_factor) % 1.0
            saturation = 1.0
            value = 1.0 if m < max_iter else 0
            r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
            pixels[iy, ix] = (int(r*255), int(g*255), int(b*255))
    return pixels

def draw_zoom_rect():
    if dragging and start_pos and end_pos:
        x1, y1 = start_pos
        x2, y2 = end_pos
        rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)

def main():
    global zoom, offset_x, offset_y, dragging, start_pos, end_pos

    running = True
    time_factor = 0.0
    fractal_surface = None

    while running:
        screen.fill((0, 0, 0))

        scale = 1 / zoom
        xmin = offset_x - scale * 2
        xmax = offset_x + scale * 2
        ymin = offset_y - scale * 1.5
        ymax = offset_y + scale * 1.5

        if not dragging:
            fractal_pixels = mandelbrot_set(xmin, xmax, ymin, ymax, WIDTH, HEIGHT, max_iter, time_factor)
            fractal_surface = pygame.surfarray.make_surface(fractal_pixels.swapaxes(0,1))

        if fractal_surface:
            screen.blit(fractal_surface, (0,0))

        draw_zoom_rect()

        draw_text = font.render("Clique e arraste para dar zoom. ESC para resetar. Q para sair.", True, (255,255,255))
        screen.blit(draw_text, (10, HEIGHT-30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    zoom = 1.0
                    offset_x, offset_y = -0.6, 0.0
                if event.key == pygame.K_q:
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                    start_pos = event.pos
                    end_pos = event.pos

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    end_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and dragging:
                    dragging = False
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    if abs(x2 - x1) > 10 and abs(y2 - y1) > 10:
                        rect_min_x = min(x1, x2)
                        rect_max_x = max(x1, x2)
                        rect_min_y = min(y1, y2)
                        rect_max_y = max(y1, y2)

                        new_xmin = xmin + (rect_min_x / WIDTH) * (xmax - xmin)
                        new_xmax = xmin + (rect_max_x / WIDTH) * (xmax - xmin)
                        new_ymin = ymin + (rect_min_y / HEIGHT) * (ymax - ymin)
                        new_ymax = ymin + (rect_max_y / HEIGHT) * (ymax - ymin)

                        offset_x = (new_xmin + new_xmax) / 2
                        offset_y = (new_ymin + new_ymax) / 2
                        zoom *= 2 * (xmax - xmin) / (new_xmax - new_xmin)

        time_factor += 0.005
        time_factor %= 1.0

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
