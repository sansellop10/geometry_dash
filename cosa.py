import pygame
import colores

class Cosa(pygame.sprite.Sprite): 
    velocidad_global = 10
    cantidad_global = 0

    def __init__(self, size, altura, anchura): 
        super().__init__()
        # Creamos la superficie con el tamaño aleatorio que viene del main
        self.image = pygame.Surface((anchura, altura))
        self.image.fill(colores.COLOR_ENEMIGO)
        
        self.rect = self.image.get_rect()
        
        self.rect.x = size[0]
        
        posicion_suelo = size[1] // 2 + 100
        
        self.rect.bottom = posicion_suelo

    def update(self):
        self.rect.x -= Cosa.velocidad_global
        if self.rect.right <= 0:
            self.kill()
            Cosa.cantidad_global += 1
            if Cosa.cantidad_global % 4 == 0:
                Cosa.velocidad_global += 2

    @classmethod
    def reset_juego(cls):
        cls.velocidad_global = 10
        cls.cantidad_global = 0