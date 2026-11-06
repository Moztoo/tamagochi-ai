#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tamagotchi AI Hook Handler for Antigravity CLI lifecycle events.
Reads hook JSON payload from stdin and updates the e-ink screen.
Follows the flow:
  - IDLE + random actions when resting.
  - PreInvocation: 'thinking' with user prompt, then auto-transitions to 'working'.
  - PreToolUse: 'working' / 'coding' / 'cleaning' / 'searching' with funny phrases.
  - PostInvocation: 'happy' celebration, then returns to 'idle' after a delay.
"""

import sys
import os
import json
import time
import random
import argparse
import subprocess

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tamagotchi_display import update_display, get_random_working
from tamagotchi_idle import set_busy, is_busy

TOOL_FUNNY_MAP = {
    'write_file': [
        ('coding', 'Escribiendo bytes de alta fidelidad...'),
        ('coding', 'Traduciendo café en código limpio...'),
        ('cleaning', 'Puliendo los ceros y lustrando los unos...'),
        ('working', 'Afilando el lápiz binario...'),
    ],
    'edit_file': [
        ('coding', 'Sobornando al compilador con cafeína...'),
        ('coding', 'Alineando electrones en la memoria RAM...'),
        ('cleaning', 'Barriendo la basura del garbage collector...'),
        ('working', 'Reescribiendo mentalmente todo en Rust...'),
    ],
    'run_command': [
        ('working', 'Desengrasando los bytes del sistema...'),
        ('working', 'Invocando al demonio de los sockets...'),
        ('cleaning', 'Destapando cañerías del bus SPI...'),
        ('coding', 'Convenciendo a los transistores de cooperar...'),
        ('working', 'Acariciando los hilos del procesador...'),
    ],
    'read_file': [
        ('searching', 'Buscando gatitos en la web...'),
        ('searching', 'Rastreando bugs interdimensionales...'),
        ('searching', 'Preguntándole a los patitos de goma...'),
        ('reading', 'Inspeccionando pergaminos binarios...'),
    ],
    'search_web': [
        ('searching', 'Buscando gatitos en la web...'),
        ('searching', 'Descargando más RAM cuántica de internet...'),
        ('searching', 'Surfeando en la superautopista de la info...'),
    ]
}

def clean_text(text, max_len=60):
    if not text:
        return ""
    text = " ".join(text.replace("\n", " ").split())
    if len(text) > max_len:
        return text[:max_len - 3] + "..."
    return text

def spawn_delayed_transition(cmd_args):
    """Spawns a detached process without blocking hook response."""
    python_bin = sys.executable or "python3"
    full_cmd = [python_bin] + cmd_args
    try:
        if os.name == 'nt':
            subprocess.Popen(full_cmd, cwd=BASE_DIR, creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
        else:
            subprocess.Popen(full_cmd, cwd=BASE_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    except Exception as e:
        print(f"Error spawning background transition: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--event', choices=['pre', 'post', 'tool', 'session', 'stop'], default='pre')
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
        set_busy(True, prompt=cleaned)
        update_display(state='thinking', text=thought, full_refresh=False)

        # Spawn delayed transition to funny working mode in background
        idle_script = os.path.join(BASE_DIR, 'tamagotchi_idle.py')
        spawn_delayed_transition([idle_script, '--transition-working', '3'])

        # Output hook response immediately
        print(json.dumps({"status": "ok"}))

    elif args.event == 'tool':
        # PreToolUse hook
        tool_call = payload.get('toolCall', {})
        tool_name = tool_call.get('name', 'tarea')
        
        candidates = TOOL_FUNNY_MAP.get(tool_name)
        if candidates:
            state, text = random.choice(candidates)
        else:
            state, text = get_random_working()

        update_display(state=state, text=text, full_refresh=False)
        # PreToolUse expects 'decision': 'allow'
        print(json.dumps({"decision": "allow"}))

    elif args.event == 'post':
        set_busy(False)
        # Display completion celebration
        update_display(state='happy', text="¡Tarea completada con éxito!", full_refresh=False)
        
        # Schedule return to IDLE after 6 seconds
        idle_script = os.path.join(BASE_DIR, 'tamagotchi_idle.py')
        spawn_delayed_transition([idle_script, '--schedule-idle', '6'])
        
        print(json.dumps({"status": "ok"}))

    elif args.event == 'session':
        set_busy(False)
        update_display(state='idle', text="Tamagotchi AI Online en modo remoto.", full_refresh=True)
        print(json.dumps({"status": "ok"}))

    elif args.event == 'stop':
        set_busy(False)
        update_display(state='sleeping', text="Zzz... Sesión remota finalizada.", full_refresh=False)
        print(json.dumps({"status": "ok"}))

if __name__ == '__main__':
    main()
