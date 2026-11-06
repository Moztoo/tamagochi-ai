#!/usr/bin/env bash
# ==============================================================================
# Tamagotchi AI - Remote Launcher for Raspberry Pi Zero 2W
# Starts Antigravity CLI session with:
#   --dangerously-skip-permissions
#   --remote-control
# ==============================================================================

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
export PYTHONPATH="$DIR:$DIR/lib:$PYTHONPATH"

# 1. Ensure remote-control daemon is running or start it
echo "==> Verificando servicio Remote Control de Antigravity..."
if agy remote-control status 2>&1 | grep -q "inactive"; then
    echo "==> Iniciando daemon de control remoto..."
    agy remote-control start
fi

INSTANCE_NAME=$(agy remote-control status 2>&1 | grep "Instance name" | cut -d':' -f2 | xargs)
if [ -z "$INSTANCE_NAME" ]; then
    INSTANCE_NAME="Tamagotchi-Pi"
fi

echo "==> Instancia remota: $INSTANCE_NAME"

# 2. Update e-ink screen to Idle/Ready
echo "==> Actualizando pantalla e-ink..."
python3 "$DIR/tamagotchi_display.py" --full --state idle --text "Conectado: $INSTANCE_NAME. Listo para peticiones."

# 3. Start background idle animation daemon (cycles random cute moods when idle)
echo "==> Iniciando daemon de animaciones en reposo..."
python3 "$DIR/tamagotchi_idle.py" --daemon --interval 90 &
IDLE_PID=$!

# 4. Handle exit cleanly
cleanup() {
    echo ""
    echo "==> Finalizando sesión..."
    if [ -n "$IDLE_PID" ]; then
        kill "$IDLE_PID" 2>/dev/null || true
    fi
    python3 "$DIR/tamagotchi_display.py" --state sleeping --text "Zzz... Sesión remota en reposo."
    exit 0
}
trap cleanup SIGINT SIGTERM

# 5. Launch agy with remote-control and dangerously-skip-permissions
echo "==> Levantando sesión de Antigravity (agy)..."
echo "==> Flags: --remote-control --dangerously-skip-permissions"
echo "---------------------------------------------------------"

exec agy --remote-control --dangerously-skip-permissions "$@"
