import pygame
import colores

class Player(pygame.sprite.Sprite):
    def __init__(self, size): 
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(colores.COLOR_PLAYER)
        
        self.rect = self.image.get_rect()
        self.rect.x = size[0] // 4
        
        # El suelo base del juego
        self.suelo_base = size[1] // 2 + 100
        self.suelo = self.suelo_base
        
        self.rect.bottom = self.suelo

        # Físicas
        self.velocidad_y = 0
        self.gravedad = 1.2         
        self.impulso_salto = -20    
        self.saltando = False

    def saltar(self):
        if not self.saltando:
            self.velocidad_y = self.impulso_salto
            self.saltando = True

    def update(self):
        # Aplicamos gravedad
        self.velocidad_y += self.gravedad
        self.rect.y += self.velocidad_y
        
        # Comprobamos el suelo actual (puede ser el suelo real o el techo de un enemigo)
        if self.rect.bottom >= self.suelo:
            self.rect.bottom = self.suelo  
            self.velocidad_y = 0           
            self.saltando = False          
        
        # Resetear el suelo al base por defecto cada frame.
        # Si seguimos encima de un enemigo, el main.py se encargará de volver a cambiarlo antes de que caiga.
        self.suelo = self.suelo_base