# Context del Proyecto: Juego de Disparos 2D (Pygame)

---

## 📋 Resumen General

**Nombre del proyecto:** Shooter 2D Simple - Edición WWII (2 Jugadores)  
**Lenguaje:** Python 3.x  
**Framework:** Pygame ≥ 2.0.0  
**Estructura:** Un solo archivo (`shooter_game.py`)  
**Objetivo:** Juego de disparos 2D cooperativo local con 2 jugadores en la parte inferior, gráficos geométricos básicos y sonidos procedimentales estilo Segunda Guerra Mundial

---

## 🎮 Mecánicas Implementadas

| Característica | Estado | Detalles |
|----------------|--------|----------|
| **2 Jugadores locales (co-op)** | ✅ **NUEVO v1.2** | Ambos en parte inferior, lados separados |
| Movimiento Jugador 1 (A/D) | ✅ Completo | Lado izquierdo, límite en centro - 10px |
| Movimiento Jugador 2 (←/→) | ✅ Completo | Lado derecho, límite en centro + 10px |
| Disparo J1 (Espacio) / J2 (Enter) | ✅ Completo | Cadencia 150ms independiente por jugador |
| Enemigos cayendo | ✅ Completo | Bombarderos (círculos+alas), velocidad 3-6 |
| Colisión disparo-enemigo | ✅ Completo | Detección círculo-rectángulo, +10 pts |
| Puntuación compartida (co-op) | ✅ Completo | Esquina sup. izq., fuente 36pt |
| Dificultad progresiva | ✅ Completo | Spawn 1000ms → 400ms mín. |
| Game Over | ✅ Completo | Al tocar fondo, sirena + reinicio (Espacio) |
| Reinicio de partida | ✅ Completo | Reset de todas las variables |
| **Sonidos procedimentales WWII** | ✅ v1.1 | Metralleta, explosión, sirena, motor (loop) |

---

## 🎮 Controles (2 Jugadores - Teclado Compartido)

| Acción | Jugador 1 (Verde - Izquierda) | Jugador 2 (Azul - Derecha) |
|--------|-------------------------------|----------------------------|
| Mover Izquierda | `A` | `Flecha Izquierda` |
| Mover Derecha | `D` | `Flecha Derecha` |
| Disparar | `Espacio` | `Enter` (Intro) |
| Reiniciar (Game Over) | `Espacio` | `Espacio` |
| Salir | `ESC` | `ESC` |

**Nota:** Ambos jugadores comparten la misma pantalla y teclado (local co-op).

---

## 🔊 Sistema de Sonidos (Procedimentales - Sin Archivos Externos)

| Sonido | Tipo | Descripción Técnica |
|--------|------|---------------------|
| **Disparo** | Onda cuadrada 1200Hz, 50ms | Estilo metralleta/chip-tune, envelope decay |
| **Explosión** | Ruido blanco 200ms | Envelope ataque rápido + decay exponencial |
| **Game Over** | Sirena aérea 2s | Frecuencia oscilante 400-800Hz (0.5Hz), onda senoidal |
| **Motor (ambiente)** | Armónicos graves 60Hz base | Loop infinito: fundamental + 3 armónicos (120, 180, 240Hz) |

**Implementación:** `array.array('h')` + `pygame.mixer.Sound(buffer=...)` + `pygame.mixer.Channel` dedicado para motor.

---

## 📁 Archivos del Proyecto

```
TFR-Nose/
├── shooter_game.py   # Juego completo (lógica + render + sonidos + bucle principal)
├── requirements.txt  # Dependencias (pygame>=2.0.0)
└── context.md        # Este archivo
```

---

## 🔧 Detalles Técnicos

### Constantes Principales
```python
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
FPS = 60
JUGADOR_ANCHO = 50
JUGADOR_ALTO = 50
JUGADOR_Y = ALTO_PANTALLA - JUGADOR_ALTO - 10
JUGADOR_VELOCIDAD = 7
DISPARO_ANCHO = 5
DISPARO_ALTO = 15
DISPARO_VELOCIDAD = 10
CADENCIA_DISPARO = 150  # ms
ENEMIGO_RADIO = 20
ENEMIGO_VELOCIDAD_MIN = 3
ENEMIGO_VELOCIDAD_MAX = 6
```

### Configuración de Audio
```python
pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512)
# 22.05 kHz, 16-bit signed, estéreo, buffer 512 samples
```

### Estructuras de Datos
- **Jugador 1:** `jugador1_x` (int), posición Y fija en `JUGADOR_Y`
- **Jugador 2:** `jugador2_x` (int), posición Y fija en `JUGADOR_Y`
- **Disparos:** Lista de dicts `{"x": int, "y": int, "color": tuple, "jugador": 1|2}`
- **Enemigos:** Lista de dicts `{"x": int, "y": int, "velocidad": int, "color": tuple, "radio": int}`

### Funciones Principales
| Función | Propósito |
|---------|-----------|
| `generar_onda_cuadrada()` | Síntesis onda cuadrada con envelope |
| `generar_ruido_blanco()` | Ruido con envelope para explosiones |
| `generar_sirena_aerea()` | Tono oscilante estilo sirena WWII |
| `generar_zumbido_motor()` | Armónicos graves loopable |
| `crear_sonido_desde_buffer()` | Wrapper `pygame.mixer.Sound` |
| `crear_enemigo()` | Genera bombardero aleatorio |
| `dibujar_jugador(x, y, color, color_oscuro)` | Avión paramétrico (reutilizable p1/p2) |
| `dibujar_disparo(disparo)` | Tracer con color por jugador |
| `dibujar_enemigo(enemigo)` | Bombardero con alas, cabina, motores |
| `dibujar_puntuacion(puntos)` | Texto + indicador sonido + leyenda controles |
| `dibujar_game_over(puntos)` | Overlay + sirena + mensaje temático |
| `reiniciar_juego()` | Reset completo + flags sonido + posiciones iniciales |

---

## 🐛 Issues Conocidos / Limitaciones

1. **Sin vidas** - Game Over inmediato al tocar un enemigo el fondo
2. **Sin menú principal** - Inicia directo en gameplay
3. **Colisión simplificada** - Usa punto más cercano del rectángulo al centro del círculo
4. **Un solo tipo de enemigo** - Solo varía color y velocidad
5. **Sin power-ups / armas especiales**
6. **Sin high score persistente** - Se pierde al cerrar
7. **Sonidos mono-canal** - Disparo y explosión comparten canal por defecto
8. **Sin control de volumen en UI** - Solo hardcoded en código
9. **Teclado compartido** - Posible "ghosting" en teclados baratos (A/D + Flechas + Espacio/Enter simultáneo)

---

## 🚀 Ideas para Futuras Mejoras

### Prioridad Alta
- [ ] Añadir sistema de vidas (3 iconos avión por jugador en esquinas sup.)
- [ ] Menú principal (Jugar, Controles, Sonido, Salir)
- [ ] Control de volumen maestro / SFX / Música en menú

### Prioridad Media
- [ ] Tipos de enemigos (cazas rápidos, bombarderos pesados, ace que dispara)
- [ ] Power-ups (disparo triple, escudo temporal, bomba limpia-pantalla)
- [ ] High score guardado en archivo JSON
- [ ] Partículas al destruir enemigo (humo, chispas)
- [ ] Canales de audio separados para SFX simultáneos
- [ ] Soporte para mandos/joysticks (evita ghosting teclado)

### Prioridad Baja
- [ ] Jefes finales cada X puntos
- [ ] Fondos con parallax scrolling (nubes, ciudad)
- [ ] Modo versus (competitivo) además de co-op
- [ ] Tabla de clasificación online
- [ ] Música procedimental adaptativa (tensión según enemigos)

---

## 📝 Historial de Cambios

| Fecha | Versión | Cambios |
|-------|---------|---------|
| 2026-10-15 | v1.0.0 | **Creación inicial**: juego completo funcional en un archivo, requirements.txt, context.md |
| 2026-10-15 | v1.1.0 | **Sonidos WWII procedimentales**: metralleta, explosión, sirena aérea, motor avión loop. Gráficos temáticos (avión jugador, bombarderos, trazadores). Fondo estrellado scrolling. Cadencia de disparo. |
| 2026-10-15 | v1.2.0 | **Modo 2 jugadores local (co-op)**: Jugador 1 (Verde, A/D+Espacio) lado izquierdo, Jugador 2 (Azul, Flechas+Enter) lado derecho. Puntuación compartida. Línea divisoria visual. Controles independientes con cadencia propia. Reinicio sincronizado. |

---

## 🎯 Próximos Pasos Inmediatos

1. Probar el juego en diferentes resoluciones y ajustar balance
2. Implementar sistema de vidas (3 iconos avión por jugador)
3. Añadir menú principal con opciones de audio
4. Separar canales de audio para SFX simultáneos
5. Añadir power-ups básicos (disparo rápido, escudo)
6. Considerar soporte gamepad para evitar ghosting de teclado

---

> **Nota:** Este archivo debe actualizarse con cada cambio significativo en el código base.