import pygame
import random
import os

# Inicialización de Pygame
pygame.init()

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 600

# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Juego tipo Polytopia simplificado')

# FPS (Frames per second)
clock = pygame.time.Clock()

# Tamaño de las celdas y unidades
TAMAÑO_CELDA = 40

# Cargar imágenes
fondo = pygame.image.load('background.png')
ciudad_img = pygame.image.load('city.png')
unidad_img = pygame.image.load('unit.png')
disparo_img = pygame.image.load('shot.png')

# Escalar imágenes a tamaños adecuados
ciudad_img = pygame.transform.scale(ciudad_img, (TAMAÑO_CELDA, TAMAÑO_CELDA))
unidad_img = pygame.transform.scale(unidad_img, (TAMAÑO_CELDA, TAMAÑO_CELDA))
disparo_img = pygame.transform.scale(disparo_img, (10, 10))

# Cargar imágenes de la explosión
explosion_imgs = [pygame.image.load(f'explosion_{i}.png') for i in range(1, 6)]
explosion_imgs = [pygame.transform.scale(img, (TAMAÑO_CELDA, TAMAÑO_CELDA)) for img in explosion_imgs]

# Clases del juego
class Ciudad:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.explosion_frame = 0
        self.exploding = False

    def dibujar(self):
        if self.exploding:
            pantalla.blit(explosion_imgs[self.explosion_frame // 5], (self.x * TAMAÑO_CELDA, self.y * TAMAÑO_CELDA))
            self.explosion_frame += 1
            if self.explosion_frame >= len(explosion_imgs) * 5:
                self.explosion_frame = 0
                self.exploding = False
                return False
        else:
            pantalla.blit(ciudad_img, (self.x * TAMAÑO_CELDA, self.y * TAMAÑO_CELDA))
        return True

    def explotar(self):
        self.exploding = True

class Unidad:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def mover(self, dx, dy):
        self.x += dx
        self.y += dy

    def dibujar(self):
        pantalla.blit(unidad_img, (self.x * TAMAÑO_CELDA, self.y * TAMAÑO_CELDA))

class Disparo:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def mover(self):
        self.x += self.dx
        self.y += self.dy

    def dibujar(self):
        pantalla.blit(disparo_img, (self.x * TAMAÑO_CELDA + TAMAÑO_CELDA // 2, self.y * TAMAÑO_CELDA + TAMAÑO_CELDA // 2))

    def colisiona_con(self, ciudad):
        return self.x == ciudad.x and self.y == ciudad.y

def dibujar_tablero():
    pantalla.blit(fondo, (0, 0))

def juego():
    game_over = False

    # Crear ciudades y unidades
    ciudades = [Ciudad(random.randint(0, ANCHO // TAMAÑO_CELDA - 1), random.randint(0, ALTO // TAMAÑO_CELDA - 1)) for _ in range(5)]
    unidades = [Unidad(random.randint(0, ANCHO // TAMAÑO_CELDA - 1), random.randint(0, ALTO // TAMAÑO_CELDA - 1)) for _ in range(3)]
    disparos = []

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    unidades[0].mover(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    unidades[0].mover(1, 0)
                elif event.key == pygame.K_UP:
                    unidades[0].mover(0, -1)
                elif event.key == pygame.K_DOWN:
                    unidades[0].mover(0, 1)
                elif event.key == pygame.K_SPACE:
                    disparos.append(Disparo(unidades[0].x, unidades[0].y, 0, -1))

        dibujar_tablero()

        for ciudad in ciudades[:]:
            if not ciudad.dibujar():
                ciudades.remove(ciudad)

        for unidad in unidades:
            unidad.dibujar()

        for disparo in disparos[:]:
            disparo.mover()
            disparo.dibujar()
            for ciudad in ciudades:
                if disparo.colisiona_con(ciudad):
                    ciudad.explotar()
                    disparos.remove(disparo)
                    break

        pygame.display.update()
        clock.tick(15)

    pygame.quit()

juego()

