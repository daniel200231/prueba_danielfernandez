import random
import pygame
import sys

pygame.init()


ANCHO, ALTO = 700, 500
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Shooter PRUEBA CON PYGAME")


BLANCO =pygame.Color("white")
NEGRO = pygame.Color("black")
ROJO = pygame.Color("red")
AZUL = pygame.Color("blue")

clock = pygame.time.Clock()
FPS = 62


def dibujar_texto(texto, fuente, color, superficie, x, y):
    txt_obj = fuente.render(texto, True, color)
    superficie.blit(txt_obj, (x, y))

def jugador(x, y):
    pygame.draw.rect(ventana, AZUL, (x, y, 50, 50))

def enemigo(x, y):
    pygame.draw.rect(ventana, ROJO, (x, y, 40, 40))

def disparar_bala(x, y):
    pygame.draw.rect(ventana, BLANCO, (x, y, 10, 20))

def menu_principal():
    fuente = pygame.font.Font(None, 74)
    en_menu = True

    while en_menu:
        ventana.fill(NEGRO)
        dibujar_texto("DISPARA CON LA TECLA (X)", pygame.font.Font(None, 36), BLANCO, ventana, 200, 240)
        dibujar_texto("PRESIONA ENTER PARA EMPEZAR", pygame.font.Font(None, 36), BLANCO, ventana, 150, 290)
        dibujar_texto("PRESIONA ESC PARA SALIR", pygame.font.Font(None, 36), BLANCO, ventana, 180, 340)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    en_menu = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(FPS)

def juego():
    jugador_x = ANCHO // 2
    jugador_y = ALTO - 60
    velocidad_jugador = 7

    balas = []
    velocidad_bala = -12

    enemigos = []
    velocidad_enemigo = 5
    spawn_timer = 0
    score=0
    corriendo = True
    while corriendo:
        ventana.fill(NEGRO)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

        
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and jugador_x > 0:
            jugador_x -= velocidad_jugador
        if teclas[pygame.K_RIGHT] and jugador_x < ANCHO - 50:
            jugador_x += velocidad_jugador
        if teclas[pygame.K_x]:
            if len(balas) < 10:
                balas.append([jugador_x + 20, jugador_y])

        jugador(jugador_x, jugador_y)


        for bala in balas[:]:
            bala[1] += velocidad_bala
            disparar_bala(bala[0], bala[1])
            if bala[1] < 0:
                balas.remove(bala)


        spawn_timer += 1
        if spawn_timer > 30:
            enemigos.append([random.randint(0, ANCHO - 40), -40])
            spawn_timer = 0


        for enemigo_pos in enemigos[:]:
            enemigo_pos[1] += velocidad_enemigo
            enemigo(enemigo_pos[0], enemigo_pos[1])
            if enemigo_pos[1] > ALTO:
                enemigos.remove(enemigo_pos)
                
                break


            for bala in balas[:]:
                bala_rect = pygame.Rect(bala[0], bala[1], 10, 20)
                enemigo_rect = pygame.Rect(enemigo_pos[0], enemigo_pos[1], 40, 40)
                if bala_rect.colliderect(enemigo_rect):
                    if bala in balas:
                        balas.remove(bala)
                    if enemigo_pos in enemigos:
                        enemigos.remove(enemigo_pos)
                    score +=10
                        
                    break
        fuente_score = pygame.font.Font(None, 26)
        texto_score = fuente_score.render(f"Score: {score}", True, BLANCO)
        ventana.blit(texto_score, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


menu_principal()
juego()
