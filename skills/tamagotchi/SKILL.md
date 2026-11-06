---
name: tamagotchi
description: Controls the Waveshare e-Paper display (2.13" V4) on the Raspberry Pi Zero 2W, showing an AI Tamagotchi with 14 expressive moods and animations (idle, thinking, working, coding, cleaning, searching, coffee, gaming, music, reading, snack, happy, sleeping, alert), funny action quotes, and dynamic speech bubbles.
---

# Tamagotchi AI E-Ink Skill

This skill allows Antigravity (AGY) to interact directly with the physical e-ink display on the Raspberry Pi Zero 2W to act as a virtual "Tamagotchi AI" companion.

## Lifecycle Flow

1. **Resting / Idle**:
   - Cycles through cute random activities (`idle`, `coffee`, `gaming`, `music`, `reading`, `snack`).
2. **On Prompt Arrival (`PreInvocation`)**:
   - Shows `thinking` with the user's prompt text in the speech bubble.
   - Automatically transitions to a funny working mood after a brief moment while the model runs.
3. **During Tool & Task Execution (`PreToolUse`)**:
   - Displays witty working actions with matching sprites (`working`, `coding`, `cleaning`, `searching`) such as *"Degreasing system bytes..."*, *"Searching for kittens on the web..."*, *"Bribing the compiler with caffeine..."*.
4. **On Task Completion (`PostInvocation`)**:
   - Shows `happy` celebration (*"Task completed successfully!"*).
   - Automatically returns to `idle` after a few seconds and resumes resting activities.

---

## How to Invoke the Display Controller

The controller script is located at:
```bash
/home/ricardom/git/tamagotchi-ai/tamagotchi_display.py
```

### CLI Syntax

```bash
python3 /home/ricardom/git/tamagotchi-ai/tamagotchi_display.py --state <STATE> --text "<THOUGHT OR ACTION>"
```

Or trigger random activities:
```bash
# Random funny working action
python3 /home/ricardom/git/tamagotchi-ai/tamagotchi_display.py --random-working

# Random cute idle action
python3 /home/ricardom/git/tamagotchi-ai/tamagotchi_display.py --random-idle
```

### Available States (`--state`):
- **Working / Busy states**:
  1. `thinking`: Looking upward with thought bubble / lightbulb filament.
  2. `working`: Cyber visor, typing on retro mini laptop.
  3. `coding`: Hacker mode, terminal prompt, code brackets (`</>`).
  4. `cleaning`: Bandana on forehead, sweeping away bugs and dust with a broom.
  5. `searching`: Detective hat, giant magnifying glass inspecting paws & bugs.
- **Idle / Relaxing states**:
  6. `idle`: Curious blinking eyes, sweet smile, leaf antenna.
  7. `coffee`: Sipping a steaming mug of hot coffee/tea with content closed eyes.
  8. `gaming`: Focused on a retro handheld console (Game Boy style).
  9. `music`: Retro over-ear headphones, vibing with floating music notes (♪ ♫).
  10. `reading`: Wearing round reading glasses, holding an open book/manual.
  11. `snack`: Chubby munching cheek puff, nibbling on a chocolate chip cookie.
- **Status states**:
  12. `happy`: Celebrating with raised arms, hearts, and sparkles.
  13. `sleeping`: Deep slumber with floating zZz and drool bubble.
  14. `alert`: Surprised wide eyes, exclamation mark on warnings or errors.

### Additional Options:
- **`--full`**: Performs a full screen refresh (clears ghosting). Partial refresh is default.
- **`--clear`**: Wipes the display to blank white.

---

## Idle Daemon (`tamagotchi_idle.py`)

Runs in the background to keep the Tamagotchi alive with charming random moods when no tasks are running:
```bash
python3 /home/ricardom/git/tamagotchi-ai/tamagotchi_idle.py --daemon --interval 90 &
```
