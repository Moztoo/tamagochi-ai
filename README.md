# 🐣 Tamagotchi AI — Raspberry Pi Zero 2W + Waveshare e-Paper (2.13" V4)

Transform your Raspberry Pi Zero 2W with a Waveshare e-Paper display into an **interactive AI Tamagotchi**, remotely controlled via **Google Antigravity (`agy`)**.

Whenever you send remote requests or tasks to the Pi, the AI updates the physical e-ink screen in real time—displaying your little Tamagotchi companion with custom pixel art moods, witty commentary, and a dynamic dialogue speech bubble.

---

## 🔄 Dynamic Lifecycle Flow

```
[ IDLE Loop ] ──► [ Prompt Received ] ──► [ Running / Tools ] ──► [ Done ] ──► [ Back to IDLE ]
(Random Coffee,   (Thinking + prompt)     (Funny work sprites     (Happy        (Resumes random
 Gaming, Music...)                         & witty messages)       celebration)  idle activities)
```

1. **Resting & Idle (`tamagotchi_idle.py`)**:
   - When no tasks are active, the background idle daemon gently cycles through cute random activities every ~90 seconds (sipping coffee, playing Tetris, listening to music, reading manuals, having a snack).
2. **On Request Arrival (`PreInvocation`)**:
   - The screen immediately transitions to **`thinking`**, displaying the user's prompt in the speech bubble.
   - Automatically transitions to working mode while the agent prepares its plan.
3. **While Running & Executing Tools (`PreToolUse`)**:
   - Dynamically selects matching sprites (`working`, `coding`, `cleaning`, `searching`) with funny action messages:
     - *"Desengrasando los bytes del sistema..."*
     - *"Buscando gatitos en la web..."*
     - *"Sobornando al compilador con cafeína..."*
     - *"Puliendo los ceros y lustrando los unos..."*
     - *"Alineando electrones en la memoria RAM..."*
4. **On Task Completion (`PostInvocation`)**:
   - The Tamagotchi celebrates in **`happy`** mode (*"¡Tarea completada con éxito!"*).
   - After a 6-second celebration window, it automatically returns to **`idle`** and resumes resting animations.

---

## 🎨 14 Expressive Moods & Pixel Art Sprites

Custom 48x48 pixel art sprites handcrafted for high-contrast monochrome e-ink screens:

### ⚙️ Working & Execution
- **`thinking`**: Looking upward with a glowing lightbulb / idea bubble.
- **`working`**: Cyber visor engaged, typing on a retro mini laptop with spark effects.
- **`coding`**: Matrix hacker mode with terminal prompt `>` and floating `< / >` brackets.
- **`cleaning`**: Bandana tied on forehead, sweeping away dust and bugs with a broom.
- **`searching`**: Detective hat and giant magnifying glass tracking cat paws and data.

### ☕ Idle & Relaxing
- **`idle`**: Cute curious blinking eyes, gentle smile, and sprouting antenna.
- **`coffee`**: Sipping a hot steaming mug of coffee/tea with content closed eyes.
- **`gaming`**: Intently focused on a retro handheld console (Game Boy style).
- **`music`**: Wearing retro over-ear headphones, vibing with musical notes (♪ ♫).
- **`reading`**: Round reading glasses, holding an open documentation manual.
- **`snack`**: Chubby munching cheek puff, nibbling on a chocolate chip cookie.

### 📢 Status & Alerts
- **`happy`**: Celebrating with raised arms, hearts, and stars (`^ _ ^`).
- **`sleeping`**: Deep slumber with floating zZz and drool bubble.
- **`alert`**: Wide-eyed surprise / exclamation mark on warnings or errors.

---

## 📂 Repository Structure

```
~/git/tamagotchi-ai/
├── start_tamagotchi_ai.sh    # Main launcher (starts remote agy + idle daemon)
├── tamagotchi_display.py     # Display driver, UI renderer & activity catalogs
├── tamagotchi_sprites.py     # Pixel art generator (14 distinct states)
├── tamagotchi_hook.py        # Antigravity lifecycle event handler (hooks.json)
├── tamagotchi_idle.py        # Idle manager daemon & delayed transition worker
├── demo_tamagotchi.py        # Demo script cycling through all 14 moods
├── tamagotchi.service        # Optional systemd service for auto-start on boot
├── lib/
│   └── waveshare_epd/        # Waveshare e-Paper 2.13" V4 driver library
├── pic/
│   └── Font.ttc              # TrueType font asset
├── skills/
│   └── tamagotchi/
│       └── SKILL.md          # Antigravity skill definition
└── .agents/
    ├── hooks.json            # Lifecycle hooks (SessionStart, PreInvocation, PreToolUse, PostInvocation, Stop)
    ├── rules/
    │   └── tamagotchi.md     # Persona rule for display usage
    └── skills/
        └── tamagotchi/
            └── SKILL.md
```

---

## 🚀 Starting the Remote Session

To start the Tamagotchi AI with remote access, automated permissions, and background idle animations:

```bash
cd ~/git/tamagotchi-ai
./start_tamagotchi_ai.sh
```

The script automatically:
1. Verifies that the `agy` remote control daemon is active.
2. Retrieves the Raspberry Pi instance name (e.g., `pylon-lunar-corona`).
3. Updates the e-ink screen indicating the Tamagotchi is online.
4. Starts the background idle animation daemon (`tamagotchi_idle.py`).
5. Launches the headless remote session:
   ```bash
   agy --remote-control --dangerously-skip-permissions
   ```
6. On exit (`Ctrl+C`), gracefully stops the idle daemon and sets the Tamagotchi to sleep (`sleeping`: Zzz...).

---

## 🛠️ Manual Command-Line Usage

You can also trigger moods, activities, or daemon commands manually:

```bash
# Random funny working action
python3 ~/git/tamagotchi-ai/tamagotchi_display.py --random-working

# Random cute idle activity
python3 ~/git/tamagotchi-ai/tamagotchi_display.py --random-idle

# Specific state and custom message
python3 ~/git/tamagotchi-ai/tamagotchi_display.py --state coffee --text "Tomando un cafecito a 65°C..."

# Run the idle background daemon manually
python3 ~/git/tamagotchi-ai/tamagotchi_idle.py --daemon --interval 90 &

# Full refresh (clears ghosting)
python3 ~/git/tamagotchi-ai/tamagotchi_display.py --full --state idle --text "Pantalla reinicializada."
```

---

## 🧪 Running the Demo

To preview all 14 moods, expressions, and speech bubbles in sequence:

```bash
python3 ~/git/tamagotchi-ai/demo_tamagotchi.py
```

---

## ⚙️ Auto-Start Service (Systemd)

To launch the Tamagotchi AI automatically whenever your Raspberry Pi boots:

```bash
sudo cp ~/git/tamagotchi-ai/tamagotchi.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tamagotchi.service
sudo systemctl start tamagotchi.service
```
