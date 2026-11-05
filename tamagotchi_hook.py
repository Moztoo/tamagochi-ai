#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tamagotchi AI Hook Handler for Antigravity CLI lifecycle events.
Reads hook JSON payload from stdin and updates the e-ink screen.
"""

import sys
import os
import json
import argparse

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tamagotchi_display import update_display

def clean_text(text, max_len=70):
    if not text:
        return ""
    text = " ".join(text.replace("\n", " ").split())
    if len(text) > max_len:
        return text[:max_len - 3] + "..."
    return text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--event', choices=['pre', 'post', 'tool', 'session'], default='pre')
    args = parser.parse_args()

    payload = {}
    try:
        if not sys.stdin.isatty():
            payload = json.load(sys.stdin)
    except Exception:
        pass

    user_input = payload.get('lastUserInput', '')
    
    if args.event == 'pre':
        cleaned = clean_text(user_input, max_len=60)
        thought = f"Petición: {cleaned}" if cleaned else "Pensando en la respuesta..."
        update_display(state='thinking', text=thought, full_refresh=False)

    elif args.event == 'post':
        update_display(state='happy', text="¡Tarea completada! Esperando órdenes.", full_refresh=False)

    elif args.event == 'session':
        update_display(state='idle', text="Tamagotchi AI Online en modo remoto.", full_refresh=True)

    elif args.event == 'tool':
        tool_name = payload.get('toolName', 'tarea')
        update_display(state='working', text=f"Ejecutando: {tool_name}", full_refresh=False)

    # Respond valid JSON on stdout as expected by agy hook protocol
    print(json.dumps({"status": "ok"}))

if __name__ == '__main__':
    main()
