#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tamagotchi AI Idle Manager & Daemon
Handles random idle animations when no tasks are running,
and manages delayed transitions (e.g., returning to IDLE after task completion).
"""

import sys
import os
import time
import json
import argparse
import subprocess

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from tamagotchi_display import update_display, get_random_idle, STATE_FILE

BUSY_FLAG = '/tmp/tamagotchi_busy.flag' if os.name != 'nt' else os.path.join(os.environ.get('TEMP', '.'), 'tamagotchi_busy.flag')
IDLE_PID_FILE = '/tmp/tamagotchi_idle.pid' if os.name != 'nt' else os.path.join(os.environ.get('TEMP', '.'), 'tamagotchi_idle.pid')

def is_busy():
    """Checks if the agent is currently busy processing a prompt or tools."""
    if os.path.exists(BUSY_FLAG):
        # Safety check: if flag is older than 5 minutes, consider it stale
        try:
            mtime = os.path.getmtime(BUSY_FLAG)
            if time.time() - mtime > 300:
                os.remove(BUSY_FLAG)
                return False
            return True
        except Exception:
            return False
    return False

def set_busy(busy=True, prompt=""):
    """Sets or clears the busy flag and updates state tracking."""
    try:
        if busy:
            with open(BUSY_FLAG, 'w') as f:
                f.write(str(time.time()))
            state_data = {
                "status": "busy",
                "prompt": prompt,
                "timestamp": time.time()
            }
            with open(STATE_FILE, 'w') as f:
                json.dump(state_data, f)
        else:
            if os.path.exists(BUSY_FLAG):
                try:
                    os.remove(BUSY_FLAG)
                except Exception:
                    pass
            state_data = {
                "status": "idle",
                "timestamp": time.time()
            }
            with open(STATE_FILE, 'w') as f:
                json.dump(state_data, f)
    except Exception as e:
        print(f"State file error: {e}")

def transition_working(delay_seconds=3):
    """
    Waits delay_seconds after prompt arrival. If still busy,
    transitions screen from 'thinking' to a funny working state.
    """
    time.sleep(delay_seconds)
    if is_busy():
        # Check current state from STATE_FILE
        try:
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, 'r') as f:
                    data = json.load(f)
                    if data.get("status") != "busy":
                        return
        except Exception:
            pass

        from tamagotchi_display import get_random_working
        state, text = get_random_working()
        update_display(state=state, text=text, full_refresh=False)

def schedule_idle(delay_seconds=6):
    """
    Waits delay_seconds and, if not busy, resets screen to IDLE.
    Runs synchronously (intended to be spawned in a detached process/thread).
    """
    time.sleep(delay_seconds)
    if not is_busy():
        update_display(state='idle', text="Listo para recibir instrucciones", full_refresh=False)
        set_busy(False)

def run_idle_daemon(interval=90):
    """
    Background idle daemon loop.
    Every `interval` seconds (default 90s for e-ink longevity),
    if the agent is not busy, picks a random cute mood/activity.
    """
    # Write PID
    try:
        with open(IDLE_PID_FILE, 'w') as f:
            f.write(str(os.getpid()))
    except Exception:
        pass

    print(f"Tamagotchi Idle Daemon started (Interval: {interval}s)...")
    
    last_update = time.time()
    
    try:
        while True:
            time.sleep(5)
            # If busy, wait until idle
            if is_busy():
                last_update = time.time()
                continue

            now = time.time()
            if now - last_update >= interval:
                state, text = get_random_idle()
                update_display(state=state, text=text, full_refresh=False)
                last_update = time.time()
    except (KeyboardInterrupt, SystemExit):
        print("Tamagotchi Idle Daemon stopped.")
    finally:
        if os.path.exists(IDLE_PID_FILE):
            try:
                os.remove(IDLE_PID_FILE)
            except Exception:
                pass

def main():
    parser = argparse.ArgumentParser(description="Tamagotchi Idle Manager")
    parser.add_argument('--schedule-idle', type=float, metavar='SECONDS',
                        help="Wait SECONDS and switch to idle if not busy")
    parser.add_argument('--transition-working', type=float, metavar='SECONDS',
                        help="Wait SECONDS and transition from thinking to working if still busy")
    parser.add_argument('--daemon', action='store_true',
                        help="Run the idle animation daemon")
    parser.add_argument('--interval', type=int, default=90,
                        help="Idle animation interval in seconds (default: 90)")
    parser.add_argument('--once', action='store_true',
                        help="Trigger a single random idle mood right now")
    parser.add_argument('--clear-busy', action='store_true',
                        help="Clear the busy flag manually")

    args = parser.parse_args()

    if args.clear_busy:
        set_busy(False)
        print("Busy flag cleared.")
    elif args.transition_working is not None:
        transition_working(args.transition_working)
    elif args.schedule_idle is not None:
        schedule_idle(args.schedule_idle)
    elif args.once:
        if not is_busy():
            state, text = get_random_idle()
            update_display(state=state, text=text, full_refresh=False)
    elif args.daemon:
        run_idle_daemon(interval=args.interval)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
