import pygame
import random
import sys
import math
import array

# Inicialización de Pygame (mixer primero para sonidos)
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.init()

# ============================================================
# GENERADOR DE SONIDOS PROCEDIMENTALES ESTILO WWII
# ============================================================

def generar_onda_cuadrada(frecuencia, duracion_ms, volumen=0.5, sample_rate=22050):
    """Genera una onda cuadrada (estilo síntesis retro/chip-tune)"""
    n_samples = int(sample_rate * duracion_ms / 1000)
    buf = array.array('h', [0] * n_samples * 2)  # stereo
    amplitude = int(32767 * volumen)
    period = sample_rate / frecuencia
    half_period = int(period / 2)
    
    for i in range(n_samples):
        # Onda cuadrada
        val = amplitude if (i % period) < half_period else -amplitude
        # Envelope de decay exponencial
        envelope = math.exp(-i * 0.0003)
        val = int(val * envelope)
        buf[i*2] = val      # canal izquierdo
        buf[i*2+1] = val    # canal derecho
    return buf


def generar_ruido_blanco(duracion_ms, volumen=0.3, sample_rate=22050):
    """Genera ruido blanco con envelope (para explosiones)"""
    n_samples = int(sample_rate * duracion_ms / 1000)
    buf = array.array('h', [0] * n_samples * 2)
    amplitude = int(32767 * volumen)
    
    for i in range(n_samples):
        # Ruido pseudo-aleatorio simple
        val = random.randint(-amplitude, amplitude)
        # Envelope: ataque rápido, decay exponencial
        envelope = math.exp(-i * 0.0008)
        val = int(val * envelope)
        buf[i*2] = val
        buf[i*2+1] = val
    return buf


def generar_sirena_aerea(duracion_ms, sample_rate=22050):
    """Genera sirena estilo WWII (tono descendente/ascendente)"""
    n_samples = int(sample_rate * duracion_ms / 1000)
    buf = array.array('h', [0] * n_samples * 2)
    amplitude = int(32767 * 0.4)
    
    for i in range(n_samples):
        t = i / sample_rate
        # Frecuencia que oscila entre 400-800 Hz (sirena clásica)
        freq = 400 + 400 * (0.5 + 0.5 * math.sin(2 * math.pi * 0.5 * t))
        # Onda senoidal para sirena más realista
        val = int(amplitude * math.sin(2 * math.pi * freq * t))
        # Envelope suave
        envelope = 0.5 + 0.5 * math.sin(math.pi * t / (duracion_ms / 1000))
        val = int(val * envelope)
        buf[i*2] = val
        buf[i*2+1] = val
    return buf


def generar_zumbido_motor(duracion_ms, sample_rate=22050):
    """Genera zumbido grave de motor de avión (loopable)"""
    n_samples = int(sample_rate * duracion_ms / 1000)
    buf = array.array('h', [0] * n_samples * 2)
    amplitude = int(32767 * 0.15)
    
    for i in range(n_samples):
        t = i / sample_rate
        # Armónicos graves para sonido de motor
        val = 0
        val += math.sin(2 * math.pi * 60 * t)      # fundamental
        val += 0.5 * math.sin(2 * math.pi * 120 * t)  # 2do armónico
        val += 0.25 * math.sin(2 * math.pi * 180 * t) # 3er armónico
        val += 0.1 * math.sin(2 * math.pi * 240 * t)  # 4to armónico
        val = int(amplitude * val / 1.85)
        buf[i*2] = val
        buf[i*2+1] = val
    return buf


def crear_sonido_desde_buffer(buf):
    """Crea un objeto Sound de pygame desde un buffer array"""
    sound = pygame.mixer.Sound(buffer=buf)
    return sound


# Generar todos los sonidos al inicio
print("Generando sonidos WWII...")

# Disparo: ráfaga corta de metralleta (onda cuadrada aguda, 50ms)
buf_disparo = generar_onda_cuadrada(1200, 50, 0.4)
sonido_disparo = crear_sonido_desde_buffer(buf_disparo)

# Explosión: ruido blanco con decay (200ms)
buf_explosion = generar_ruido_blanco(200, 0.5)
sonido_explosion = crear_sonido_desde_buffer(buf_explosion)

# Game Over: sirena aérea (2 segundos)
buf_gameover = generar_sirena_aerea(2000)
sonido_gameover = crear_sonido_desde_buffer(buf_gameover)

# Motor avión: zumbido grave loopable (1 segundo, se repite)
buf_motor = generar_zumbido_motor(1000)
sonido_motor = crear_sonido_desde_buffer(buf_motor)

# Canal dedicado para el motor (loop)
canal_motor = pygame.mixer.Channel(0)
canal_motor.play(sonido_motor, loops=-1)
canal_motor.set_volume(0.3)

print("Sonidos generados correctamente.")

# ============================================================
# CONFIGURACIÓN DEL JUEGO - 2 JUGADORES
# ============================================================

# Configuración de la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Juego de Disparos 2D - Edición WWII (2 Jugadores)")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 100, 255)
AMARILLO = (255, 255, 0)
GRIS_OSCURO = (40, 40, 40)
NARANJA = (255, 165, 0)
CYAN = (0, 255, 255)

# Configuración de jugadores (2 players en la parte inferior)
JUGADOR_ANCHO = 50
JUGADOR_ALTO = 50
JUGADOR_Y = ALTO_PANTALLA - JUGADOR_ALTO - 10
JUGADOR_VELOCIDAD = 7

# Jugador 1 (Izquierda - Verde) - Controles: A/D + Espacio
jugador1_x = ANCHO_PANTALLA // 4 - JUGADOR_ANCHO // 2
jugador1_color = VERDE
jugador1_color_oscuro = (0, 180, 0)
jugador1_disparo_color = AMARILLO
jugador1_tecla_izq = pygame.K_a
jugador1_tecla_der = pygame.K_d
jugador1_tecla_disparo = pygame.K_SPACE
jugador1_ultimo_disparo = 0

# Jugador 2 (Derecha - Azul) - Controles: Flechas + Enter/Control derecho
jugador2_x = 3 * ANCHO_PANTALLA // 4 - JUGADOR_ANCHO // 2
jugador2_color = AZUL
jugador2_color_oscuro = (0, 80, 200)
jugador2_disparo_color = CYAN
jugador2_tecla_izq = pygame.K_LEFT
jugador2_tecla_der = pygame.K_RIGHT
jugador2_tecla_disparo = pygame.K_RETURN  # Enter
jugador2_ultimo_disparo = 0

# Configuración de disparos compartida
DISPARO_ANCHO = 5
DISPARO_ALTO = 15
DISPARO_VELOCIDAD = 10
CADENCIA_DISPARO = 150  # ms entre disparos
disparos = []  # Lista de {"x", "y", "color", "jugador"}

# Configuración de enemigos
ENEMIGO_RADIO = 20
ENEMIGO_VELOCIDAD_MIN = 3
ENEMIGO_VELOCIDAD_MAX = 6
enemigos = []
tiempo_ultimo_enemigo = 0
intervalo_enemigo = 1000  # milisegundos

# Puntuación (compartida - modo cooperativo)
puntuacion = 0
fuente = pygame.font.Font(None, 36)
fuente_pequena = pygame.font.Font(None, 24)

# Reloj para controlar FPS
reloj = pygame.time.Clock()
FPS = 60

# Estado del juego
jugando = True
game_over = False
gameover_sound_played = False


def crear_enemigo():
    """Crea un nuevo enemigo en una posición aleatoria en la parte superior"""
    x = random.randint(ENEMIGO_RADIO, ANCHO_PANTALLA - ENEMIGO_RADIO)
    y = -ENEMIGO_RADIO
    velocidad = random.randint(ENEMIGO_VELOCIDAD_MIN, ENEMIGO_VELOCIDAD_MAX)
    color = (random.randint(100, 255), random.randint(50, 200), random.randint(50, 200))
    return {"x": x, "y": y, "velocidad": velocidad, "color": color, "radio": ENEMIGO_RADIO}


def dibujar_jugador(x, y, color, color_oscuro):
    """Dibuja un jugador (avión estilo WWII)"""
    # Cuerpo principal (fuselaje)
    pygame.draw.rect(pantalla, color, (x + 15, y, 20, JUGADOR_ALTO))
    # Alas
    pygame.draw.rect(pantalla, color, (x, y + 15, JUGADOR_ANCHO, 20))
    # Cabina
    pygame.draw.rect(pantalla, color_oscuro, (x + 18, y + 5, 14, 14))
    # Detalle: hélice (animada)
    tiempo = pygame.time.get_ticks() / 100
    if int(tiempo) % 2 == 0:
        pygame.draw.line(pantalla, GRIS_OSCURO, (x + 25, y - 5), (x + 25, y + 5), 2)
    else:
        pygame.draw.line(pantalla, GRIS_OSCURO, (x + 20, y), (x + 30, y), 2)


def dibujar_disparo(disparo):
    """Dibuja un disparo (tracer estilo WWII)"""
    color_principal = disparo["color"]
    color_brillo = tuple(min(255, c + 80) for c in color_principal)
    pygame.draw.rect(pantalla, color_principal, (disparo["x"], disparo["y"], DISPARO_ANCHO, DISPARO_ALTO))
    pygame.draw.rect(pantalla, color_brillo, (disparo["x"] + 1, disparo["y"] + 2, 3, DISPARO_ALTO - 4))


def dibujar_enemigo(enemigo):
    """Dibuja un enemigo (avión/bombardero - círculo con alas)"""
    cx, cy = int(enemigo["x"]), int(enemigo["y"])
    r = enemigo["radio"]
    color = enemigo["color"]
    
    # Alas del bombardero
    pygame.draw.ellipse(pantalla, color, (cx - r * 1.5, cy - 5, r * 3, 10))
    # Fuselaje
    pygame.draw.circle(pantalla, color, (cx, cy), r)
    # Cabina
    pygame.draw.circle(pantalla, (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50)), (cx, cy - 5), r // 3)
    # Motores en las alas
    pygame.draw.circle(pantalla, GRIS_OSCURO, (cx - r, cy - 2), 4)
    pygame.draw.circle(pantalla, GRIS_OSCURO, (cx + r, cy - 2), 4)


def dibujar_puntuacion(puntos):
    """Dibuja la puntuación en la esquina superior izquierda"""
    texto = fuente.render(f"Puntuación: {puntos}", True, BLANCO)
    pantalla.blit(texto, (10, 10))
    # Indicador de sonido
    texto_sound = fuente_pequena.render("🔊 Sonidos WWII activados", True, (150, 150, 150))
    pantalla.blit(texto_sound, (10, 45))
    # Leyenda de controles
    controles = [
        "P1: A/D + ESPACIO  |  P2: ←/→ + ENTER",
        "Verde = Jugador 1  |  Azul = Jugador 2"
    ]
    for i, linea in enumerate(controles):
        texto_ctrl = fuente_pequena.render(linea, True, (120, 120, 120))
        pantalla.blit(texto_ctrl, (10, 70 + i * 22))


def dibujar_game_over(puntos):
    """Dibuja la pantalla de game over"""
    # Fondo semitransparente
    overlay = pygame.Surface((ANCHO_PANTALLA, ALTO_PANTALLA))
    overlay.fill(NEGRO)
    overlay.set_alpha(200)
    pantalla.blit(overlay, (0, 0))

    # Texto Game Over
    fuente_grande = pygame.font.Font(None, 72)
    texto_game_over = fuente_grande.render("GAME OVER", True, ROJO)
    rect_game_over = texto_game_over.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 80))
    pantalla.blit(texto_game_over, rect_game_over)

    # Puntuación final
    texto_puntuacion = fuente.render(f"Puntuación final: {puntos}", True, BLANCO)
    rect_puntuacion = texto_puntuacion.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 - 10))
    pantalla.blit(texto_puntuacion, rect_puntuacion)

    # Mensaje temático
    texto_tema = fuente_pequena.render('"El cielo ya no es el límite..."', True, (200, 150, 150))
    rect_tema = texto_tema.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 30))
    pantalla.blit(texto_tema, rect_tema)

    # Instrucciones para reiniciar
    texto_reiniciar = fuente.render("Presiona ESPACIO para reiniciar o ESC para salir", True, BLANCO)
    rect_reiniciar = texto_reiniciar.get_rect(center=(ANCHO_PANTALLA // 2, ALTO_PANTALLA // 2 + 70))
    pantalla.blit(texto_reiniciar, rect_reiniciar)


def reiniciar_juego():
    """Reinicia todas las variables del juego"""
    global jugador1_x, jugador2_x, disparos, enemigos, puntuacion
    global tiempo_ultimo_enemigo, intervalo_enemigo, game_over, gameover_sound_played
    global jugador1_ultimo_disparo, jugador2_ultimo_disparo, jugando
    
    jugador1_x = ANCHO_PANTALLA // 4 - JUGADOR_ANCHO // 2
    jugador2_x = 3 * ANCHO_PANTALLA // 4 - JUGADOR_ANCHO // 2
    disparos = []
    enemigos = []
    puntuacion = 0
    tiempo_ultimo_enemigo = pygame.time.get_ticks()
    intervalo_enemigo = 1000
    jugador1_ultimo_disparo = 0
    jugador2_ultimo_disparo = 0
    game_over = False
    gameover_sound_played = False
    jugando = True


# Bucle principal del juego
tiempo_ultimo_enemigo = pygame.time.get_ticks()

while True:
    # Manejo de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if evento.key == pygame.K_SPACE and game_over:
                reiniciar_juego()

    if not game_over:
        # ========== MOVIMIENTO JUGADOR 1 (A/D) ==========
        teclas = pygame.key.get_pressed()
        if teclas[jugador1_tecla_izq]:
            jugador1_x -= JUGADOR_VELOCIDAD
        if teclas[jugador1_tecla_der]:
            jugador1_x += JUGADOR_VELOCIDAD

        # Limitar movimiento jugador 1 (mitad izquierda - 10px margen centro)
        limite_der_j1 = ANCHO_PANTALLA // 2 - JUGADOR_ANCHO - 10
        if jugador1_x < 0:
            jugador1_x = 0
        if jugador1_x > limite_der_j1:
            jugador1_x = limite_der_j1

        # ========== MOVIMIENTO JUGADOR 2 (Flechas) ==========
        if teclas[jugador2_tecla_izq]:
            jugador2_x -= JUGADOR_VELOCIDAD
        if teclas[jugador2_tecla_der]:
            jugador2_x += JUGADOR_VELOCIDAD

        # Limitar movimiento jugador 2 (mitad derecha - 10px margen centro)
        limite_izq_j2 = ANCHO_PANTALLA // 2 + 10
        if jugador2_x < limite_izq_j2:
            jugador2_x = limite_izq_j2
        if jugador2_x > ANCHO_PANTALLA - JUGADOR_ANCHO:
            jugador2_x = ANCHO_PANTALLA - JUGADOR_ANCHO

        # ========== DISPARO JUGADOR 1 (ESPACIO) ==========
        if teclas[jugador1_tecla_disparo]:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - jugador1_ultimo_disparo >= CADENCIA_DISPARO:
                disparo_x = jugador1_x + JUGADOR_ANCHO // 2 - DISPARO_ANCHO // 2
                disparo_y = JUGADOR_Y
                disparos.append({
                    "x": disparo_x, 
                    "y": disparo_y, 
                    "color": jugador1_disparo_color,
                    "jugador": 1
                })
                sonido_disparo.play()
                jugador1_ultimo_disparo = tiempo_actual

        # ========== DISPARO JUGADOR 2 (ENTER) ==========
        if teclas[jugador2_tecla_disparo]:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - jugador2_ultimo_disparo >= CADENCIA_DISPARO:
                disparo_x = jugador2_x + JUGADOR_ANCHO // 2 - DISPARO_ANCHO // 2
                disparo_y = JUGADOR_Y
                disparos.append({
                    "x": disparo_x, 
                    "y": disparo_y, 
                    "color": jugador2_disparo_color,
                    "jugador": 2
                })
                sonido_disparo.play()
                jugador2_ultimo_disparo = tiempo_actual

        # Actualizar disparos
        for disparo in disparos[:]:
            disparo["y"] -= DISPARO_VELOCIDAD
            # Eliminar disparos que salen de la pantalla
            if disparo["y"] + DISPARO_ALTO < 0:
                disparos.remove(disparo)

        # Generar enemigos
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_ultimo_enemigo > intervalo_enemigo:
            enemigos.append(crear_enemigo())
            tiempo_ultimo_enemigo = tiempo_actual
            # Aumentar dificultad gradualmente
            if intervalo_enemigo > 400:
                intervalo_enemigo -= 10

        # Actualizar enemigos
        for enemigo in enemigos[:]:
            enemigo["y"] += enemigo["velocidad"]
            # Verificar si el enemigo llegó al fondo (Game Over)
            if enemigo["y"] - enemigo["radio"] > ALTO_PANTALLA:
                game_over = True

        # Detectar colisiones disparo-enemigo
        for disparo in disparos[:]:
            for enemigo in enemigos[:]:
                # Colisión círculo-rectángulo simplificada
                cx, cy = enemigo["x"], enemigo["y"]
                closest_x = max(disparo["x"], min(cx, disparo["x"] + DISPARO_ANCHO))
                closest_y = max(disparo["y"], min(cy, disparo["y"] + DISPARO_ALTO))
                distancia_cuadrado = (cx - closest_x) ** 2 + (cy - closest_y) ** 2

                if distancia_cuadrado < enemigo["radio"] ** 2:
                    # Colisión detectada
                    if disparo in disparos:
                        disparos.remove(disparo)
                    if enemigo in enemigos:
                        enemigos.remove(enemigo)
                    puntuacion += 10
                    sonido_explosion.play()
                    break

    else:
        # Game Over - reproducir sirena una sola vez
        if not gameover_sound_played:
            canal_motor.stop()  # Parar motor
            sonido_gameover.play()
            gameover_sound_played = True

    # ========== DIBUJADO ==========
    pantalla.fill(NEGRO)

    # Fondo: estrellas/nubes sutiles (scrolling lento)
    for i in range(20):
        x_star = (i * 37 + pygame.time.get_ticks() // 50) % ANCHO_PANTALLA
        y_star = (i * 73 + pygame.time.get_ticks() // 100) % ALTO_PANTALLA
        pygame.draw.circle(pantalla, (50, 50, 60), (x_star, y_star), 1)

    # Línea divisoria sutil entre jugadores
    pygame.draw.line(pantalla, (30, 30, 40), (ANCHO_PANTALLA // 2, 0), (ANCHO_PANTALLA // 2, ALTO_PANTALLA), 1)

    if not game_over:
        # Dibujar jugadores
        dibujar_jugador(jugador1_x, JUGADOR_Y, jugador1_color, jugador1_color_oscuro)
        dibujar_jugador(jugador2_x, JUGADOR_Y, jugador2_color, jugador2_color_oscuro)

        # Dibujar disparos
        for disparo in disparos:
            dibujar_disparo(disparo)

        # Dibujar enemigos
        for enemigo in enemigos:
            dibujar_enemigo(enemigo)

        dibujar_puntuacion(puntuacion)
    else:
        dibujar_game_over(puntuacion)

    pygame.display.flip()
    reloj.tick(FPS)