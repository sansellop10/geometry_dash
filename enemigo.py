import pygame
import colores
from cosa import Cosa

class Enemigo(Cosa): 

    def __init__(self, size, altura, anchura): 
        super().__init__(size, altura, anchura)
        self.image = pygame.Surface((anchura, altura), pygame.SRCALPHA) # 'SRCALPHA' hace que el fondo sea transparente
        
        # 2. Dibujamos el triángulo DENTRO de esa superficie
        # Definimos las 3 esquinas del pincho (coordenadas relativas a su propia caja)
        punto_alto = (anchura // 2, 0)          # La punta de arriba (centrada horizontalmente)
        punto_izq  = (0, altura)                # La esquina inferior izquierda
        punto_der  = (anchura, altura)           # La esquina inferior derecha
        
        # Pintamos el triángulo relleno con tu color de enemigo
        pygame.draw.polygon(self.image, colores.COLOR_ENEMIGO, [punto_alto, punto_izq, punto_der])
        
        # 3. Posicionamos el objeto en el suelo exacto del juego
        self.rect = self.image.get_rect()
        self.rect.x = size[0]
        
        posicion_suelo = size[1] // 2 + 100
        
        self.rect.bottom = posicion_suelo
