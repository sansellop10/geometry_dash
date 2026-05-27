import pygame, sys
import colores
from personaje import Player
from enemigo import Enemigo
from cosa import Cosa
import random

pygame.init()

size = (900, 550)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Geometry Dash")

lista_sprites = pygame.sprite.Group()
lista_enemigos = pygame.sprite.Group()

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 64, bold=True)
font_small = pygame.font.SysFont("Arial", 24)

EVENTO_ENEMIGO = pygame.USEREVENT + 1
pygame.time.set_timer(EVENTO_ENEMIGO, 2000)

lista_particulas = []

game_over = False
player = None

def reset_game():
    global game_over, player, lista_particulas

    lista_sprites.empty()
    lista_enemigos.empty()
    lista_particulas.clear() # CORRECCIÓN: Vaciamos las partículas al reiniciar
    
    player = Player(size) 
    lista_sprites.add(player)
    
    Enemigo.reset_juego() 
    game_over = False

reset_game()

while True:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                pygame.quit()
                sys.exit()

            case pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_k:
                        player.saltar()
                    
                    if event.key == pygame.K_a:
                        game_over = True
                
                elif game_over and event.key == pygame.K_r:
                    reset_game()

            case _ if event.type == EVENTO_ENEMIGO:
                if not game_over:
                    numero_enemigos = random.randint(1, 3)
                    dado = random.randint(1, 6)
                    separacion = 10
                    anchura = 60
                    if dado >4:
                        enemigo = Cosa(size, 60, 200)
                        lista_sprites.add(enemigo)
                        lista_enemigos.add(enemigo)
                    else:
                        for i in range(numero_enemigos):
                            if dado <= 2:
                                anchura = 50
                                enemigo = Enemigo(size, 50, 50)  
                            else:
                                enemigo = Enemigo(size, 60, 60)
                                
                            enemigo.rect.x += i * (anchura + separacion)
                            lista_sprites.add(enemigo)
                            lista_enemigos.add(enemigo)

    # ==========================================
    # --- LÓGICA DEL JUEGO (Cálculos) ---
    # ==========================================
    if not game_over:
        lista_sprites.update()

        # 1. GENERACIÓN de partículas (Solo si está tocando su suelo actual)
        if not player.saltando: 
            tamano = random.randint(4, 8) 
            pos_x = player.rect.left # Nace desde la parte trasera del cubo
            pos_y = player.rect.bottom - tamano +2
            vel_x = random.uniform(-4, -1) 
            vel_y = random.uniform(-2, 0)  
            
            
            lista_particulas.append([pos_x, pos_y, vel_x, vel_y, tamano])
            
        # 2. ACTUALIZACIÓN de partículas (Fuera del IF para que se muevan aunque saltes)
        for particula in lista_particulas[:]:
            particula[0] += particula[2] # Mover X
            particula[1] += particula[3] # Mover Y
            particula[4] -= 0.2          # Envejecer
            
            if particula[4] <= 0:
                lista_particulas.remove(particula)

        # 3. COLISIONES estilo Geometry Dash
        enemigos_tocados = pygame.sprite.spritecollide(player, lista_enemigos, False)
        
        for enemigo in enemigos_tocados:
            if player.velocidad_y > 0 and (player.rect.bottom <= enemigo.rect.top + 15) and type(enemigo) == Cosa:
                player.suelo = enemigo.rect.top
                player.rect.bottom = enemigo.rect.top
                player.velocidad_y = 0
                player.saltando = False
            else:
                game_over = True
        
    # ==========================================
    # --- RENDERIZADO (Dibujo en pantalla) ---
    # ==========================================
    screen.fill(colores.COLOR_FONDO) # 1. Limpiamos el lienzo de juego primero
    
    # 2. Dibujamos las partículas (Por detrás de los personajes para que quede mejor)
    for particula in lista_particulas:
        pygame.draw.rect(screen, (150, 150, 150), (particula[0], particula[1], particula[4], particula[4]))

    # 3. Dibujamos los personajes y enemigos
    lista_sprites.draw(screen)

    # 4. Dibujamos la interfaz (Puntuación)
    texto_puntos = font_small.render(f"Puntuación: {Enemigo.cantidad_global}", True, (255, 255, 255))
    screen.blit(texto_puntos, (20, 20))

    # 5. Capa superior de Game Over si corresponde
    if game_over:
        overlay = pygame.Surface(size)
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        texto_gameover = font.render("GAME OVER", True, (255, 0, 0))
        texto_reiniciar = font_small.render("Pulsa R para reiniciar", True, (255, 255, 255))
        
        screen.blit(texto_gameover, (size[0]//2 - texto_gameover.get_width()//2, 180))
        screen.blit(texto_reiniciar, (size[0]//2 - texto_reiniciar.get_width()//2, 330))
    
    pygame.display.flip()
    clock.tick(60)