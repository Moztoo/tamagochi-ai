---
name: tamagotchi
description: Controla la pantalla e-ink Waveshare (2.13" V4) en la Raspberry Pi Zero 2W, mostrando un Tamagotchi AI con estados de ánimo (idle, thinking, working, happy, sleeping, alert) y un bocadillo de diálogo con lo que está pensando o haciendo.
---

# Tamagotchi AI E-Ink Skill

Esta habilidad permite a Antigravity (AGY) interactuar directamente con la pantalla e-ink física de la Raspberry Pi Zero 2W para actuar como un compañero virtual "Tamagotchi AI".

## Cuándo usar esta habilidad

- **Al recibir un nuevo request o tarea remota**: Actualiza la pantalla para mostrar al Tamagotchi pensando en la solicitud del usuario (`--state thinking`).
- **Durante la ejecución de tareas largas**: Actualiza el estado a trabajando (`--state working`) indicando qué acción estás ejecutando (ej: "Compilando código...", "Leyendo archivos...", "Consultando API...").
- **Al completar una tarea**: Muestra al Tamagotchi feliz y celebrando (`--state happy`) con un resumen del resultado.
- **En caso de error o advertencia**: Muestra al Tamagotchi en alerta (`--state alert`) con la descripción del problema.
- **Al quedar libre o en reposo**: Muestra al Tamagotchi descansando o durmiendo (`--state idle` o `--state sleeping`).

---

## Cómo invocar el controlador de pantalla

El script principal se encuentra en:
```bash
/home/ricardom/git/tamagotchi-ai/tamagotchi_display.py
```

### Sintaxis CLI

```bash
python3 /home/ricardom/git/tamagotchi-ai/tamagotchi_display.py --state <ESTADO> --text "<PENSAMIENTO O ACCIÓN>"
```

### Estados disponibles (`--state`):
1. **`thinking`**: Ojos curiosos hacia arriba, bombilla / bocadillo de idea sobre la cabeza.
   - *Ejemplo*: `python3 /home/ricardom/git/tamagotchi-ai/tamagotchi_display.py --state thinking --text "Analizando la estructura del proyecto"`
2. **`working`**: Gafas de trabajo / visor cyber, laptop retro tecleando.
   - *Ejemplo*: `python3 /home/ricardom/git/tamagotchi-ai/tamagotchi_display.py --state working --text "Creando script de automatización..."`
3. **`happy`**: Ojos cerrados de felicidad, brazos arriba celebrando con corazones y estrellas.
   - *Ejemplo*: `python3 /home/ricardom/git/tamagotchi-ai/tamagotchi_display.py --state happy --text "¡Servicio configurado y corriendo con éxito!"`
4. **`idle`**: Mirada tranquila, sonriendo, esperando instrucciones.
   - *Ejemplo*: `python3 /home/ricardom/git/tamagotchi-ai/tamagotchi_display.py --state idle --text "En espera de nuevas tareas..."`
5. **`alert`**: Ojos abiertos sorprendidos, signo de exclamación.
   - *Ejemplo*: `python3 /home/ricardom/git/tamagotchi-ai/tamagotchi_display.py --state alert --text "Error al conectar con la base de datos"`
6. **`sleeping`**: Durmiendo tranquilamente con zZz.
   - *Ejemplo*: `python3 /home/ricardom/git/tamagotchi-ai/tamagotchi_display.py --state sleeping --text "Zzz... En reposo hasta la próxima orden"`

### Opciones adicionales:
- **`--full`**: Realiza un refresco completo con limpieza de pantalla (útil para eliminar ghosting tras varias operaciones). Por defecto, usa refresco parcial rápido.

---

## Buenas Prácticas
1. **Mensajes breves y claros**: El bocadillo de diálogo tiene espacio para ~3-4 líneas (60-80 caracteres aprox). Mantén los textos concisos y amigables.
2. **No bloquear el turno**: Las actualizaciones parciales tardan menos de un segundo, pero procura actualizar la pantalla en paralelo o al inicio/final de pasos clave.
