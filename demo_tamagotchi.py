#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tamagotchi AI Demo Script
Cycles through all 14 states and animations on the Waveshare e-ink display.
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
    ("coffee", "Tomando un cafecito a 65°C para recargar energía..."),
    ("gaming", "Echándome una partidita a Tetris mientras descanso..."),
    ("music", "Sintonizando chiptunes en 8-bit para inspirarme..."),
    ("reading", "Leyendo la documentación del kernel de Linux..."),
    ("snack", "Ñam ñam... unas galletitas binarias crujientes."),
    ("thinking", "Petición: Optimizar base de datos. Analizando..."),
    ("working", "Desengrasando los bytes del sistema operativo..."),
    ("coding", "Sobornando al compilador con cafeína pura..."),
    ("cleaning", "Puliendo los ceros y lustrando los unos..."),
    ("searching", "Buscando gatitos en la web... y bugs también."),
    ("happy", "¡Tarea completada con éxito! Todo listo."),
    ("alert", "¡Alerta! Se detectó un uso inusual de memoria."),
    ("sleeping", "Zzz... Modo reposo activado. Despiértame con un comando.")
]

def main():
    print("Iniciando demostración completa de estados de Tamagotchi AI...")
    for idx, (state, text) in enumerate(DEMO_SEQUENCE):
        print(f"[{idx+1}/{len(DEMO_SEQUENCE)}] Estado: {state:<10} | Texto: {text}")
        update_display(state=state, text=text, full_refresh=(idx == 0))
        if idx < len(DEMO_SEQUENCE) - 1:
            time.sleep(2)
    print("\nDemostración completada con éxito.")

if __name__ == '__main__':
    main()
