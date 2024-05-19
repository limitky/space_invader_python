import os
import pygame

def initialize_assets():
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/../')
    pygame.mixer.init()
