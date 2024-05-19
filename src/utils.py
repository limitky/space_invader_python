import pygame
import os

def load_images():
    background = pygame.image.load('assets/background.png')
    unit_img = pygame.image.load('assets/unit.png')
    enemy_img = pygame.image.load('assets/enemy.png')
    explosion_imgs = [pygame.image.load(f'assets/explosion{i}.png') for i in range(1, 6)]
    bullet_img = pygame.image.load('assets/bullet.png')
    return background, unit_img, enemy_img, explosion_imgs, bullet_img

def load_sounds():
    shoot_sound = pygame.mixer.Sound('assets/shoot.wav')
    explode_sound = pygame.mixer.Sound('assets/explode.wav')
    return shoot_sound, explode_sound

def play_sound(sound):
    sound.play()
