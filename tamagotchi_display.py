#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tamagotchi AI Display Controller
Waveshare 2.13inch V4 e-Paper display driver for Raspberry Pi Zero 2W.
Renders an animated retro Tamagotchi AI character with speech bubble status.
Supports multiple expressive moods, funny working messages, and random idle states.
"""

import sys
import os
import time
import random
import argparse
import logging
from datetime import datetime

# Platform-safe fcntl import (Raspberry Pi / Linux has fcntl; fallback for Windows testing)
try:
    import fcntl
    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False

# Setup paths
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
LIB_DIR = os.path.join(BASE_DIR, 'lib')
PIC_DIR = os.path.join(BASE_DIR, 'pic')

if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)

from PIL import Image, ImageDraw, ImageFont
from tamagotchi_sprites import create_sprite

# Try importing the Waveshare EPD driver (only on Linux / Raspberry Pi)
HAS_EPD = False
if os.name != 'nt':
    try:
        from waveshare_epd import epd2in13_V4, epdconfig
        HAS_EPD = True
    except (ImportError, OSError, Exception):
        HAS_EPD = False

LOCK_FILE = '/tmp/tamagotchi_epd.lock' if os.name != 'nt' else os.path.join(os.environ.get('TEMP', '.'), 'tamagotchi_epd.lock')
CACHE_IMG = '/tmp/tamagotchi_last.png' if os.name != 'nt' else os.path.join(os.environ.get('TEMP', '.'), 'tamagotchi_last.png')
STATE_FILE = '/tmp/tamagotchi_state.json' if os.name != 'nt' else os.path.join(os.environ.get('TEMP', '.'), 'tamagotchi_state.json')

# Screen resolution for 2.13" V4 in landscape
EPD_WIDTH = 250
EPD_HEIGHT = 122

ALL_STATES = [
    'idle', 'thinking', 'working', 'coding', 'cleaning', 'searching',
    'coffee', 'gaming', 'music', 'reading', 'snack', 'happy', 'sleeping', 'alert'
]

FUNNY_WORKING_ACTIVITIES = [
    ('working', 'Desengrasando los bytes del sistema...'),
    ('searching', 'Buscando gatitos en la web...'),
    ('coding', 'Sobornando al compilador con cafeína...'),
    ('cleaning', 'Barriendo la basura del garbage collector...'),
    ('working', 'Reescribiendo mentalmente todo en Rust...'),
    ('coding', 'Alineando electrones en la memoria RAM...'),
    ('cleaning', 'Limpiando el polvo de los registros CPU...'),
    ('searching', 'Rastreando bugs interdimensionales...'),
    ('working', 'Invocando al demonio de los sockets...'),
    ('coding', 'Convenciendo a los transistores de cooperar...'),
    ('searching', 'Descargando más RAM cuántica de internet...'),
    ('working', 'Calculando el sentido de la vida (42)...'),
    ('cleaning', 'Destapando cañerías del bus SPI...'),
    ('coding', 'Traduciendo café en código limpio...'),
    ('searching', 'Preguntándole a los patitos de goma...'),
    ('working', 'Acariciando los hilos del procesador...'),
    ('coding', 'Optimizando algoritmos a la velocidad de la luz...'),
    ('cleaning', 'Puliendo los ceros y lustrando los unos...'),
]

IDLE_ACTIVITIES = [
    ('idle', 'Mirando una mosca digital pasar...'),
    ('idle', 'Esperando pacientemente tu próxima gran idea.'),
    ('coffee', 'Tomando un cafecito a 65°C...'),
    ('coffee', 'Recargando cafeína en el bus de datos.'),
    ('gaming', 'Intentando pasarme el nivel 4 de Tetris...'),
    ('gaming', 'Jugando al Snake dentro de un byte...'),
    ('music', 'Sintonizando lofi chill beats para programar.'),
    ('music', 'Escuchando chiptunes en 8-bit a todo volumen.'),
    ('reading', 'Repasando las páginas del manual de Linux...'),
    ('reading', 'Leyendo "Cómo educar a tu humano asistente".'),
    ('snack', 'Comiendo unos doritos sabor a silicio...'),
    ('snack', 'Ñam ñam... una galleta binaria crujiente.'),
    ('idle', 'Silbando mientras llega tu próxima orden.'),
    ('idle', '¿Qué proyecto genial construiremos hoy?'),
    ('coffee', 'Soplando la taza para no quemar transistores.'),
]

def get_random_working():
    """Returns a random (state, text) tuple for funny working actions."""
    return random.choice(FUNNY_WORKING_ACTIVITIES)

def get_random_idle():
    """Returns a random (state, text) tuple for random idle actions."""
    return random.choice(IDLE_ACTIVITIES)

def get_cpu_temp():
    """Returns the Raspberry Pi CPU temperature in Celsius."""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_c = int(f.read().strip()) / 1000.0
            return f"{temp_c:.0f}°C"
    except Exception:
        return "OK"

def wrap_text(text, font, max_width, draw):
    """Wraps text into multiple lines so it fits into max_width."""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = " ".join(current_line + [word])
        try:
            bbox = draw.textbbox((0, 0), test_line, font=font)
            w = bbox[2] - bbox[0]
        except Exception:
            w = draw.textsize(test_line, font=font)[0]
        
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def render_tamagotchi_frame(state='idle', text='Listo para trabajar', subheader=None):
    """
    Renders the complete 250x122 image buffer.
    Mode '1' (1-bit pixels, black and white).
    """
    img = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)
    draw = ImageDraw.Draw(img)

    # Load fonts
    font_path = os.path.join(PIC_DIR, 'Font.ttc')
    if os.path.exists(font_path):
        font_header = ImageFont.truetype(font_path, 11)
        font_state = ImageFont.truetype(font_path, 10)
        font_body = ImageFont.truetype(font_path, 12)
        font_small = ImageFont.truetype(font_path, 10)
    else:
        font_header = ImageFont.load_default()
        font_state = font_header
        font_body = font_header
        font_small = font_header

    now = datetime.now()
    time_str = now.strftime('%H:%M')
    cpu_str = get_cpu_temp()

    # 1. Top status bar (y: 0..16)
    draw.rectangle([0, 0, EPD_WIDTH, 16], fill=0)
    draw.text((4, 2), "AGY-AI REMOTE", font=font_header, fill=255)
    
    # Time and CPU on right
    status_right = f"{time_str} | {cpu_str}"
    try:
        sw = draw.textbbox((0, 0), status_right, font=font_header)[2]
    except Exception:
        sw = draw.textsize(status_right, font=font_header)[0]
    draw.text((EPD_WIDTH - sw - 4, 2), status_right, font=font_header, fill=255)

    # 2. Left side: Tamagotchi sprite & state label (x: 2..64, y: 20..120)
    sprite = create_sprite(state=state, scale=1)
    img.paste(sprite, (9, 21))

    # Tamagotchi state badge below
    state_labels = {
        'idle': 'IDLE',
        'thinking': 'PENSANDO',
        'working': 'TRABAJO',
        'coding': 'CODING',
        'cleaning': 'LIMPIANDO',
        'searching': 'BUSCANDO',
        'coffee': 'CAFECITO',
        'gaming': 'JUGANDO',
        'music': 'MUSICA',
        'reading': 'LEYENDO',
        'snack': 'SNACK',
        'happy': 'FELIZ',
        'sleeping': 'REPOSO',
        'alert': 'ALERTA'
    }
    label = state_labels.get(state, state.upper())
    try:
        lw = draw.textbbox((0, 0), label, font=font_state)[2]
    except Exception:
        lw = draw.textsize(label, font=font_state)[0]
    
    lx = 9 + (48 - lw) // 2
    draw.rounded_rectangle([lx - 4, 75, lx + lw + 4, 90], radius=3, fill=0)
    draw.text((lx, 76), label, font=font_state, fill=255)

    # Mood footer
    mood_decor = "♥ ♥ ♥" if state in ('happy', 'coffee', 'snack') else ("♪ ♫ ♪" if state == 'music' else "★ ★ ★")
    draw.text((12, 97), mood_decor, font=font_small, fill=0)

    # 3. Speech bubble
    bubble_x0 = 68
    bubble_y0 = 20
    bubble_x1 = EPD_WIDTH - 3
    bubble_y1 = EPD_HEIGHT - 3

    # Draw rounded rectangle for speech bubble
    draw.rounded_rectangle([bubble_x0, bubble_y0, bubble_x1, bubble_y1], radius=6, outline=0, fill=255, width=2)

    # Draw speech triangle pointer pointing towards Tamagotchi
    draw.polygon([(bubble_x0, 38), (bubble_x0 - 7, 44), (bubble_x0, 50)], fill=255)
    draw.line([(bubble_x0, 38), (bubble_x0 - 7, 44), (bubble_x0, 50)], fill=0, width=2)
    draw.line([(bubble_x0, 39), (bubble_x0, 49)], fill=255, width=2)

    # Bubble title / header depending on mood
    if state == 'thinking':
        title_text = "Pensando:"
    elif state in ('working', 'coding'):
        title_text = "En progreso:"
    elif state == 'cleaning':
        title_text = "Mantenimiento:"
    elif state == 'searching':
        title_text = "Buscando:"
    elif state == 'happy':
        title_text = "¡Tarea Lista!"
    elif state == 'sleeping':
        title_text = "En reposo:"
    elif state == 'alert':
        title_text = "¡Alerta!"
    elif state == 'coffee':
        title_text = "Pausa café:"
    elif state == 'gaming':
        title_text = "Nivel bonus:"
    elif state == 'music':
        title_text = "Chill beats:"
    elif state == 'reading':
        title_text = "Estudiando:"
    elif state == 'snack':
        title_text = "Recargando:"
    else:
        title_text = "Estado:"

    draw.text((bubble_x0 + 8, bubble_y0 + 5), title_text, font=font_header, fill=0)
    draw.line([(bubble_x0 + 8, bubble_y0 + 19), (bubble_x1 - 8, bubble_y0 + 19)], fill=0, width=1)

    # Text wrapping inside speech bubble
    max_text_w = (bubble_x1 - bubble_x0) - 16
    lines = wrap_text(text, font_body, max_text_w, draw)

    y_text = bubble_y0 + 24
    for line in lines[:4]:
        draw.text((bubble_x0 + 8, y_text), line, font=font_body, fill=0)
        y_text += 16

    return img

def update_display(state='idle', text='Listo para trabajar', full_refresh=False):
    """
    Updates the e-ink screen safely using a file lock.
    """
    lock_fd = None
    try:
        lock_fd = open(LOCK_FILE, 'w')
        if HAS_FCNTL:
            start_lock = time.time()
            locked = False
            while time.time() - start_lock < 10:
                try:
                    fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    locked = True
                    break
                except IOError:
                    time.sleep(0.2)
            if not locked:
                print("Warning: Could not acquire E-Paper lock. Another process is rendering.", file=sys.stderr)
                return False

        # Generate frame
        img = render_tamagotchi_frame(state=state, text=text)
        try:
            img.save(CACHE_IMG)
        except Exception:
            pass

        if not HAS_EPD:
            try:
                print(f"[Simulated Display] State={state} Text='{text}' (Image saved to {CACHE_IMG})", file=sys.stderr)
            except Exception:
                pass
            return True

        epd = epd2in13_V4.EPD()

        if full_refresh:
            epd.init()
            epd.Clear(0xFF)
            epd.display(epd.getbuffer(img))
            epd.sleep()
        else:
            epd.init()
            epd.displayPartial(epd.getbuffer(img))
            epd.sleep()

        try:
            print(f"Tamagotchi updated -> State: {state} | Text: {text}", file=sys.stderr)
        except Exception:
            pass
        return True

    except Exception as e:
        try:
            print(f"Error updating display: {e}", file=sys.stderr)
        except Exception:
            pass
        return False
    finally:
        if lock_fd:
            try:
                if HAS_FCNTL:
                    fcntl.flock(lock_fd, fcntl.LOCK_UN)
                lock_fd.close()
            except Exception:
                pass

def clear_display():
    """Clears the e-ink screen completely to blank white."""
    lock_fd = None
    try:
        lock_fd = open(LOCK_FILE, 'w')
        if HAS_FCNTL:
            start_lock = time.time()
            locked = False
            while time.time() - start_lock < 10:
                try:
                    fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    locked = True
                    break
                except IOError:
                    time.sleep(0.2)
            if not locked:
                print("Warning: Could not acquire E-Paper lock.")
                return False

        if not HAS_EPD:
            print("[Simulated Display] Cleared screen.")
            return True

        epd = epd2in13_V4.EPD()
        epd.init()
        epd.Clear(0xFF)
        epd.sleep()
        print("Pantalla e-ink limpiada por completo (blanco).")
        return True
    except Exception as e:
        print(f"Error clearing display: {e}")
        return False
    finally:
        if lock_fd:
            try:
                if HAS_FCNTL:
                    fcntl.flock(lock_fd, fcntl.LOCK_UN)
                lock_fd.close()
            except Exception:
                pass

def main():
    parser = argparse.ArgumentParser(description="Tamagotchi AI E-Ink Display Controller")
    parser.add_argument('--state', '-s', choices=ALL_STATES,
                        default='idle', help="Tamagotchi emotion/state")
    parser.add_argument('--text', '-t', default="Listo para recibir instrucciones",
                        help="Text thought or action to display in speech bubble")
    parser.add_argument('--random-working', action='store_true',
                        help="Pick a random funny working activity and sprite")
    parser.add_argument('--random-idle', action='store_true',
                        help="Pick a random idle activity and sprite")
    parser.add_argument('--full', '-f', action='store_true', help="Perform full refresh and clear ghosting")
    parser.add_argument('--clear', '-c', action='store_true', help="Clear display to blank white")

    args = parser.parse_args()
    if args.clear:
        clear_display()
    elif args.random_working:
        state, text = get_random_working()
        update_display(state=state, text=text, full_refresh=args.full)
    elif args.random_idle:
        state, text = get_random_idle()
        update_display(state=state, text=text, full_refresh=args.full)
    else:
        update_display(state=args.state, text=args.text, full_refresh=args.full)

if __name__ == '__main__':
    main()
