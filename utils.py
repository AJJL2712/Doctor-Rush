import os
import pygame
from constants import WIDTH_SCREEN

#Funcion para escalar imagenes
def scale_img (image, scale):
    new_image = pygame.transform.scale(image, (int(image.get_width()*scale), int(image.get_height()*scale)))
    return new_image

#Funcion para contar elementos en un directorio
def count_elements (directory):
    return len(os.listdir(directory))

#Funcion para enlistar elementos de un directorio
def name_folder (directory):
    return os.listdir(directory)

#Funcion para calcular distancia entre dos puntos
def calculate_distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

#Funcion para dibujar texto centrado en la pantalla
def draw_text_centered(screen, text, font, color, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH_SCREEN // 2, y))
    screen.blit(text_surface, text_rect)

