# 🐣 Tamagotchi AI — Raspberry Pi Zero 2W + Waveshare e-Paper (2.13" V4)

Transforma tu Raspberry Pi Zero 2W con pantalla Waveshare e-Ink en un **Tamagotchi AI interactivo** controlado remotamente mediante **Google Antigravity (`agy`)**.

Cada vez que le envías peticiones remotas a la Pi, la IA actualiza la pantalla física e-ink mostrando a tu pequeño Tamagotchi con sus emociones pixel art y un bocadillo de diálogo que describe lo que está pensando o haciendo en tiempo real.

---

## 🎨 Características

- **Diseño Retro Pixel Art**: Sprites de 48x48 píxeles dibujados a medida para pantallas monocromáticas e-ink:
  - `idle`: Tranquilo, pestañeando y sonriendo.
  - `thinking`: Mirando hacia arriba con una bombillita / idea.
  - `working`: Con visor cyber / tecleando en una mini laptop retro.
  - `happy`: Celebrando con corazones y estrellas (`^ _ ^`).
  - `sleeping`: Zzz... reposo cuando termina la sesión.
  - `alert`: Ojos grandes de sorpresa / exclamación ante advertencias.
- **Bocadillo de Diálogo Dinámico**: Ajuste automático de texto (*word wrap*) con tipografía TrueType clara.
- **Barra de Estado Superior**: Muestra la hora actual y la temperatura real de la CPU de la Raspberry Pi en cada refresco.
- **Refresco Parcial Rápido**: Utiliza las capacidades de partial update del panel Waveshare 2.13" V4 (menos de 1 segundo de actualización sin parpadeos molestos).
- **Protección contra colisiones de Hardware**: Sistema de lockfile (`/tmp/tamagotchi_epd.lock`) que evita corrupción de bus SPI si múltiples procesos invocan la pantalla al mismo tiempo.
- **Integración con Antigravity (AGY)**:
  - **Sesión Remota**: Conexión remota instantánea mediante `--remote-control`.
  - **Permisos Desatendidos**: Automatización con `--dangerously-skip-permissions`.
  - **Lifecycle Hooks**: Actualizaciones automáticas en `PreInvocation` (al recibir el prompt) y `PostInvocation` (al terminar la respuesta).
  - **Custom Skill**: Permite a la IA cambiar su estado y texto a mitad de tareas complejas.

---

## 📂 Estructura del Repositorio

```
~/git/tamagotchi-ai/
├── start_tamagotchi_ai.sh    # Script principal para iniciar agy remoto + pantalla
├── tamagotchi_display.py     # Controlador y renderizador del display e-ink
├── tamagotchi_sprites.py     # Generador de sprites pixel art
├── tamagotchi_hook.py        # Handler para los eventos de Antigravity (hooks.json)
├── demo_tamagotchi.py        # Demo para probar todos los estados y animaciones
├── tamagotchi.service        # Servicio systemd opcional para auto-arranque
├── lib/
│   └── waveshare_epd/        # Driver Waveshare e-Paper 2.13" V4
├── pic/
│   └── Font.ttc              # Tipografía TrueType
├── skills/
│   └── tamagotchi/
│       └── SKILL.md          # Skill oficial de Antigravity
└── .agents/
    ├── hooks.json            # Configuración de hooks de ciclo de vida
    ├── rules/
    │   └── tamagotchi.md     # Regla always_on para la personalidad y uso de pantalla
    └── skills/
        └── tamagotchi/
            └── SKILL.md
```

---

## 🚀 Cómo Iniciar la Sesión Remota

Para arrancar el Tamagotchi AI con conexión remota y permisos automáticos:

```bash
cd ~/git/tamagotchi-ai
./start_tamagotchi_ai.sh
```

El script se encargará de:
1. Verificar que el daemon de control remoto de `agy` esté activo.
2. Obtener el nombre de instancia de la Raspberry Pi (por ejemplo: `pylon-lunar-corona`).
3. Actualizar la pantalla e-ink indicando que el Tamagotchi está en línea y listo.
4. Levantar la sesión con:
   ```bash
   agy --remote-control --dangerously-skip-permissions
   ```
5. Al salir (`Ctrl+C`), pondrá al Tamagotchi a dormir (`sleeping`: Zzz...).

---

## 🌐 Conexión Remota desde tu Navegador / IDE

1. Abre [https://antigravity.google.com](https://antigravity.google.com) o tu IDE Antigravity en tu máquina principal.
2. En la lista de instancias de **Remote Control**, selecciona la instancia de tu Raspberry Pi (ej. `pylon-lunar-corona`).
3. Envía cualquier tarea (por ejemplo: *"Escribe un script para respaldar mis archivos"*).
4. **¡Mira tu pantalla e-ink física!**: El Tamagotchi pasará a estado `thinking` mostrando tu solicitud, luego a `working` mientras ejecuta comandos, y finalmente a `happy` al terminar.

---

## 🛠️ Uso Manual por Línea de Comandos

También puedes pintar en la pantalla directamente desde cualquier terminal o script:

```bash
# Estado pensando
python3 ~/git/tamagotchi-ai/tamagotchi_display.py --state thinking --text "Calculando la respuesta adecuada..."

# Estado trabajando
python3 ~/git/tamagotchi-ai/tamagotchi_display.py --state working --text "Compilando dependencias y tests..."

# Estado feliz / éxito
python3 ~/git/tamagotchi-ai/tamagotchi_display.py --state happy --text "¡Todo ha salido a la perfección!"

# Estado alerta / error
python3 ~/git/tamagotchi-ai/tamagotchi_display.py --state alert --text "Advertencia: Error de conexión detectado."

# Refresco completo (limpieza de ghosting)
python3 ~/git/tamagotchi-ai/tamagotchi_display.py --full --state idle --text "Pantalla reinicializada."
```

---

## 🧪 Ejecutar la Demostración

Para ver todos los estados y emociones en secuencia sobre el display:

```bash
python3 ~/git/tamagotchi-ai/demo_tamagotchi.py
```

---

## ⚙️ Servicio de Arranque Automático (Systemd)

Si deseas que el Tamagotchi AI se levante automáticamente al encender la Raspberry Pi Zero 2W:

```bash
sudo cp ~/git/tamagotchi-ai/tamagotchi.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tamagotchi.service
sudo systemctl start tamagotchi.service
```
