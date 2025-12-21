import pygame
import constants
from constants import WIDTH_CHARACTER, HEIGHT_CHARACTER, COLOR_CHARACTER

#Personaje
class Character():
    def __init__(self,x,y, animation, energy):
        self.energy = energy
        self.flip = False
        self.animation = animation
        self.animation_patients = animation
        #Animaciones de la imagen mostradas actualmente
        self.frame_index = 0
        #Almacenamiento de la hora actual (en milisegundos desde que inicia pygame)
        self.update_time = pygame.time.get_ticks()
        self.image = animation[self.frame_index]
        self.shape = pygame.Rect(0, 0, WIDTH_CHARACTER, HEIGHT_CHARACTER)
        self.shape.center = (x,y)
#Movimiento
    def move(self, delta_x, delta_y):
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False
        self.shape.x = self.shape.x + delta_x
        self.shape.y = self.shape.y + delta_y
#Frames
    def update(self):
        cooldown_animation = 100
        self.image = self.animation[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animation:
            self.frame_index = self.frame_index + 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation):
            self.frame_index = 0
#Dibujo
    def draw(self, interface):
        image_flip = pygame.transform.flip(self.image, self.flip, False)
        interface.blit(image_flip, self.shape)
        #pygame.draw.rect(interface, COLOR_CHARACTER, self.shape)
