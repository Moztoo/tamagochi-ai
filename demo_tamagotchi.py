#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tamagotchi AI Demo Script
Cycles through all states on the Waveshare e-ink display.
"""

import time
import sys
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tamagotchi_display import update_display

DEMO_SEQUENCE = [
    ("idle", "¡Hola Mundo! Soy tu Tamagotchi AI en la Raspberry Pi."),
    ("thinking", "¿Qué tarea remota prepararemos hoy? Analizando..."),
    ("working", "Compilando código y actualizando repositorios..."),
    ("happy", "¡Todo completado al 100%! ¡Excelente trabajo!"),
    ("alert", "¡Cuidado! Se detectó un uso alto de memoria."),
    ("sleeping", "Zzz... Modo reposo activado. Despiértame con un comando.")
]

def main():
    print("Iniciando demostración de Tamagotchi AI...")
    for idx, (state, text) in enumerate(DEMO_SEQUENCE):
        print(f"[{idx+1}/{len(DEMO_SEQUENCE)}] Estado: {state} | Texto: {text}")
        update_display(state=state, text=text, full_refresh=(idx == 0))
        if idx < len(DEMO_SEQUENCE) - 1:
            time.sleep(3)
    print("Demostración completada con éxito.")

if __name__ == '__main__':
    main()
