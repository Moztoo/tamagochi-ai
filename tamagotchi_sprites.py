# -*- coding: utf-8 -*-
"""
Tamagotchi Sprite Art Generator
Generates pixel art bitmap images for different Tamagotchi AI states and moods.
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
        # Determined eyes / cyber glasses / visor
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

    elif state == 'coding':
        # Hacker mode: Matrix code and intense concentration
        draw.rectangle([14, 22, 34, 26], fill=0)
        draw.point((20, 24), fill=255)
        draw.point((28, 24), fill=255)
        # Determined mouth
        draw.line([22, 32, 26, 32], fill=0, width=1)
        # Laptop terminal with prompt '>'
        draw.rectangle([13, 34, 35, 41], outline=0, fill=255, width=1)
        draw.line([(15, 36), (17, 37)], fill=0)
        draw.line([(17, 37), (15, 38)], fill=0)
        draw.line([(18, 38), (22, 38)], fill=0)
        # Typing hands
        draw.ellipse([16, 33, 19, 36], fill=0)
        draw.ellipse([29, 33, 32, 36], fill=0)
        # Code brackets floating
        # '<' on left
        draw.line([(5, 12), (3, 15)], fill=0)
        draw.line([(3, 15), (5, 18)], fill=0)
        # '/>' on right
        draw.line([(40, 11), (43, 14)], fill=0)
        draw.line([(43, 14), (40, 17)], fill=0)
        draw.line([(44, 11), (42, 17)], fill=0)
        # Bits 0 and 1
        draw.rectangle([22, 4, 26, 9], outline=0, fill=255)
        draw.line([(32, 5), (32, 9)], fill=0)

    elif state == 'cleaning':
        # Bandana tied on forehead for hard chores / dusting
        draw.line([12, 17, 36, 17], fill=0, width=2)
        draw.polygon([(9, 15), (5, 13), (6, 18)], fill=0)
        # Wink and focused eye
        draw.line([16, 25, 21, 25], fill=0, width=2)
        draw.rectangle([27, 24, 31, 28], fill=0)
        draw.point((28, 25), fill=255)
        # Smile
        draw.arc([22, 30, 26, 34], start=0, end=180, fill=0, width=1)
        # Broom handle
        draw.line([34, 18, 41, 38], fill=0, width=2)
        # Broom bristles
        draw.polygon([(37, 38), (44, 36), (43, 44), (35, 42)], fill=0)
        # Dust puffs being swept away
        draw.arc([9, 37, 15, 41], start=180, end=360, fill=0)
        draw.point((7, 38), fill=0)
        draw.point((10, 35), fill=0)

    elif state == 'searching':
        # Detective hat
        draw.rectangle([14, 11, 34, 14], fill=0)
        draw.rounded_rectangle([17, 6, 31, 12], radius=2, fill=0)
        # Left eye winking or normal
        draw.rectangle([16, 24, 20, 28], fill=0)
        draw.point((17, 25), fill=255)
        # Big magnifying glass over right eye
        draw.ellipse([24, 20, 36, 32], outline=0, fill=255, width=2)
        # Huge magnified eye inside glass
        draw.ellipse([27, 23, 33, 29], fill=0)
        draw.point((28, 24), fill=255)
        # Magnifying glass handle
        draw.line([34, 30, 42, 38], fill=0, width=2)
        # Little cat paw print in the air (detecting cats!)
        draw.ellipse([41, 6, 44, 9], fill=0)
        draw.point((39, 4), fill=0)
        draw.point((42, 3), fill=0)
        draw.point((45, 5), fill=0)

    elif state == 'coffee':
        # Peaceful closed eyes enjoying aroma (u u)
        draw.arc([16, 25, 21, 29], start=0, end=180, fill=0, width=1)
        draw.arc([27, 25, 32, 29], start=0, end=180, fill=0, width=1)
        # Blush cheeks
        draw.point((14, 29), fill=0)
        draw.point((34, 29), fill=0)
        # Cute relaxed smile
        draw.arc([22, 28, 26, 32], start=0, end=180, fill=0, width=1)
        # Coffee mug held in front
        draw.rounded_rectangle([20, 32, 28, 40], radius=2, outline=0, fill=255, width=1)
        # Mug handle
        draw.arc([26, 33, 31, 38], start=270, end=90, fill=0, width=1)
        # Hands holding mug
        draw.ellipse([18, 34, 21, 37], fill=0)
        draw.ellipse([27, 34, 30, 37], fill=0)
        # Rising steam wisps
        draw.line([(22, 29), (24, 26)], fill=0)
        draw.line([(24, 26), (22, 23)], fill=0)
        draw.line([(26, 29), (28, 26)], fill=0)
        draw.line([(28, 26), (26, 23)], fill=0)

    elif state == 'gaming':
        # Eyes looking down intensely at handheld console
        draw.rectangle([17, 24, 21, 28], fill=0)
        draw.rectangle([27, 24, 31, 28], fill=0)
        # Cheerful mouth
        draw.arc([22, 28, 26, 31], start=0, end=180, fill=0, width=1)
        # Handheld game console (Game Boy style)
        draw.rounded_rectangle([17, 31, 31, 42], radius=2, outline=0, fill=255, width=1)
        # Screen
        draw.rectangle([20, 33, 28, 36], fill=0)
        # D-pad and buttons
        draw.point((19, 39), fill=0)
        draw.point((29, 39), fill=0)
        # Arcade pixel alien/ghost floating on top
        draw.polygon([(38, 6), (44, 6), (44, 11), (42, 13), (40, 11), (38, 13)], fill=0)
        draw.point((40, 8), fill=255)
        draw.point((42, 8), fill=255)

    elif state == 'music':
        # Retro over-ear headphones
        # Headband arc
        draw.arc([10, 10, 38, 26], start=180, end=360, fill=0, width=2)
        # Left & Right earpads
        draw.rounded_rectangle([8, 20, 12, 28], radius=2, fill=0)
        draw.rounded_rectangle([36, 20, 40, 28], radius=2, fill=0)
        # Vibing happy eyes (^ ^)
        draw.line([(17, 26), (19, 24)], fill=0, width=1)
        draw.line([(19, 24), (21, 26)], fill=0, width=1)
        draw.line([(27, 26), (29, 24)], fill=0, width=1)
        draw.line([(29, 24), (31, 26)], fill=0, width=1)
        # Singing/smiling mouth
        draw.chord([22, 28, 26, 33], start=0, end=180, fill=0)
        # Floating musical notes ♪
        draw.ellipse([38, 11, 41, 14], fill=0)
        draw.line([(41, 7), (41, 12)], fill=0, width=2)
        draw.line([(41, 7), (44, 9)], fill=0, width=2)
        # Floating small note on left
        draw.ellipse([4, 10, 6, 12], fill=0)
        draw.line([(6, 6), (6, 11)], fill=0, width=1)

    elif state == 'reading':
        # Round reading glasses
        draw.ellipse([15, 22, 22, 28], outline=0, fill=255, width=1)
        draw.ellipse([26, 22, 33, 28], outline=0, fill=255, width=1)
        draw.line([(22, 25), (26, 25)], fill=0, width=1)
        draw.point((18, 25), fill=0)
        draw.point((29, 25), fill=0)
        # Little smile
        draw.line([23, 31, 25, 31], fill=0, width=1)
        # Open book held in hands
        draw.polygon([(15, 34), (24, 37), (33, 34), (33, 41), (24, 44), (15, 41)], outline=0, fill=255)
        # Book spine
        draw.line([(24, 37), (24, 44)], fill=0, width=1)
        # Text lines on book pages
        draw.line([(17, 37), (22, 38)], fill=0)
        draw.line([(26, 38), (31, 37)], fill=0)

    elif state == 'snack':
        # Chubby munching cheek puff!
        draw.ellipse([31, 27, 36, 32], fill=0)
        # One eye winking
        draw.line([(16, 25), (21, 25)], fill=0, width=2)
        # Other eye happy curve
        draw.arc([26, 23, 31, 27], start=180, end=360, fill=0, width=2)
        # Mouth chewing
        draw.ellipse([22, 29, 26, 33], fill=0)
        # Cookie in hand
        draw.ellipse([20, 33, 27, 40], outline=0, fill=255, width=1)
        # Chocolate chips
        draw.point((22, 35), fill=0)
        draw.point((25, 37), fill=0)
        # Bite taken out
        draw.ellipse([24, 33, 27, 36], fill=255)
        # Falling crumbs
        draw.point((29, 39), fill=0)
        draw.point((30, 42), fill=0)

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
        draw.polygon([(10, 6), (7, 3), (4, 6), (7, 10)], fill=0)
        draw.polygon([(10, 6), (13, 3), (16, 6), (13, 10)], fill=0)
        draw.line([40, 7, 44, 7], fill=0)
        draw.line([42, 5, 42, 9], fill=0)

    elif state == 'sleeping':
        # Sleeping eyes (- -)
        draw.line([16, 27, 22, 27], fill=0, width=2)
        draw.line([26, 27, 32, 27], fill=0, width=2)
        # Calm sleeping smile
        draw.arc([22, 29, 26, 33], start=0, end=180, fill=0, width=1)
        # Zzz floating up
        draw.text((32, 18), "z", fill=0)
        draw.text((37, 8), "Z", fill=0)
        # Cute sleeping drool bubble
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
