# -*- coding: utf-8 -*-
"""
Tamagotchi Sprite Art Generator
Generates pixel art bitmap images for different Tamagotchi AI states.
Resolution of each sprite is 48x48 pixels, crisp and high-contrast for 1-bit e-ink.
"""

from PIL import Image, ImageDraw

def create_sprite(state='idle', scale=1):
    """
    Returns a PIL Image (mode '1', 48*scale x 48*scale) representing the tamagotchi in the given state.
    0 = black, 255 = white (background).
    """
    w, h = 48, 48
    img = Image.new('1', (w, h), 255)
    draw = ImageDraw.Draw(img)

    # Base body shape for Tamagotchi (Round cute egg / buddy)
    # Center is at x=24, y=28, radius approx 16
    
    # Draw body outline (thick pixel rounded shape)
    draw.rounded_rectangle([10, 14, 38, 42], radius=10, outline=0, fill=255, width=2)
    
    # Feet
    draw.ellipse([14, 40, 20, 45], fill=0)
    draw.ellipse([28, 40, 34, 45], fill=0)

    if state == 'idle':
        # Big curious cute eyes
        draw.rectangle([17, 24, 21, 29], fill=0)
        draw.rectangle([27, 24, 31, 29], fill=0)
        # Eye shine / pupils
        draw.point((18, 25), fill=255)
        draw.point((28, 25), fill=255)
        # Tiny cute smile
        draw.arc([22, 29, 26, 33], start=0, end=180, fill=0, width=1)
        draw.point((24, 33), fill=0)
        # Cheeks (blush dots)
        draw.point((14, 30), fill=0)
        draw.point((15, 30), fill=0)
        draw.point((33, 30), fill=0)
        draw.point((34, 30), fill=0)
        # Cute little antenna / hair leaf
        draw.line([24, 14, 24, 7], fill=0, width=2)
        draw.ellipse([22, 5, 26, 9], fill=0)

    elif state == 'thinking':
        # Eyes looking up and to the right
        draw.rectangle([18, 22, 22, 27], fill=0)
        draw.rectangle([28, 22, 32, 27], fill=0)
        draw.point((21, 23), fill=255)
        draw.point((31, 23), fill=255)
        # Small "o" mouth wondering
        draw.ellipse([23, 31, 26, 34], outline=0, fill=255)
        # Hand on chin
        draw.rectangle([30, 32, 34, 36], fill=0)
        # Thought bubble / lightbulb above head
        draw.ellipse([34, 5, 44, 15], outline=0, fill=255)
        # Question mark or bulb filament
        draw.point((39, 9), fill=0)
        draw.line([38, 8, 40, 8], fill=0)
        draw.point((39, 12), fill=0)
        # Thought dots
        draw.point((30, 13), fill=0)
        draw.point((32, 11), fill=0)

    elif state == 'working':
        # Determined eyes or cyber glasses / visor
        draw.rectangle([14, 23, 34, 28], fill=0)  # Cool visor/glasses
        draw.line([16, 25, 22, 25], fill=255)     # Visor glint left
        draw.line([26, 25, 32, 25], fill=255)     # Visor glint right
        # Focused confident smirk
        draw.line([22, 33, 27, 32], fill=0, width=2)
        # Small laptop / keyboard in front
        draw.rectangle([13, 35, 35, 41], outline=0, fill=255, width=1)
        # Laptop screen
        draw.line([15, 32, 15, 38], fill=0, width=2)
        # Typing hands
        draw.ellipse([18, 33, 21, 36], fill=0)
        draw.ellipse([27, 33, 30, 36], fill=0)
        # Gears / sparks around
        draw.line([40, 10, 44, 14], fill=0)
        draw.line([44, 10, 40, 14], fill=0)

    elif state == 'happy':
        # Closed joyful happy eyes (^ ^)
        draw.arc([16, 23, 22, 29], start=180, end=360, fill=0, width=2)
        draw.arc([26, 23, 32, 29], start=180, end=360, fill=0, width=2)
        # Open cheering happy mouth
        draw.chord([21, 29, 27, 35], start=0, end=180, fill=0)
        # Hands up in the air celebrating!
        draw.line([10, 24, 6, 17], fill=0, width=2)
        draw.ellipse([5, 15, 8, 18], fill=0)
        draw.line([38, 24, 42, 17], fill=0, width=2)
        draw.ellipse([40, 15, 43, 18], fill=0)
        # Hearts / Stars floating
        # Heart on top left
        draw.polygon([(10, 6), (7, 3), (4, 6), (7, 10)], fill=0)
        draw.polygon([(10, 6), (13, 3), (16, 6), (13, 10)], fill=0)
        # Sparkle on right
        draw.line([40, 7, 44, 7], fill=0)
        draw.line([42, 5, 42, 9], fill=0)

    elif state == 'sleeping':
        # Sleeping eyes (- -)
        draw.line([16, 27, 22, 27], fill=0, width=2)
        draw.line([26, 27, 32, 27], fill=0, width=2)
        # Calm sleeping smile
        draw.arc([22, 29, 26, 33], start=0, end=180, fill=0, width=1)
        # Zzz floating up
        # First small z
        draw.text((32, 18), "z", fill=0)
        # Second larger Z
        draw.text((37, 8), "Z", fill=0)
        # Snorlax-like cute sleeping drool bubble
        draw.ellipse([27, 31, 30, 34], outline=0, fill=255)

    elif state == 'alert':
        # Wide alert / surprised eyes (O O)
        draw.ellipse([16, 22, 23, 29], outline=0, fill=255, width=2)
        draw.ellipse([25, 22, 32, 29], outline=0, fill=255, width=2)
        draw.ellipse([18, 24, 21, 27], fill=0)
        draw.ellipse([27, 24, 30, 27], fill=0)
        # Open shocked mouth 'o'
        draw.ellipse([22, 32, 26, 37], fill=0)
        # Exclamation mark above
        draw.line([24, 4, 24, 11], fill=0, width=2)
        draw.point((24, 13), fill=0)

    if scale != 1:
        img = img.resize((w * scale, h * scale), Image.NEAREST)

    return img
