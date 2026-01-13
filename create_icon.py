#!/usr/bin/env python3
"""
Generate Liberator app icon: B-24 bomber silhouette over matrix code
with metallic colors (copper, gold, bronze, silver).
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

# Metallic color palette (from theme.py)
METALLIC_COPPER = "#B87333"
METALLIC_COPPER_LIGHT = "#CD853F"
METALLIC_COPPER_DARK = "#8B4513"

METALLIC_GOLD = "#D4AF37"
METALLIC_GOLD_LIGHT = "#FFD700"
METALLIC_GOLD_DARK = "#B8860B"

METALLIC_BRONZE = "#CD7F32"
METALLIC_BRONZE_LIGHT = "#E6A857"
METALLIC_BRONZE_DARK = "#8B4513"

METALLIC_SILVER = "#C0C0C0"
METALLIC_SILVER_LIGHT = "#E8E8E8"
METALLIC_SILVER_DARK = "#808080"

BG_DARK = "#1A1A1A"
BG_MATRIX = "#0A0A0A"

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_matrix_background(width, height, color_scheme='silver'):
    """Create matrix-like code background."""
    img = Image.new('RGB', (width, height), BG_MATRIX)
    draw = ImageDraw.Draw(img)
    
    # Choose color based on scheme
    if color_scheme == 'gold':
        matrix_color = METALLIC_GOLD
        matrix_light = METALLIC_GOLD_LIGHT
    elif color_scheme == 'copper':
        matrix_color = METALLIC_COPPER
        matrix_light = METALLIC_COPPER_LIGHT
    elif color_scheme == 'bronze':
        matrix_color = METALLIC_BRONZE
        matrix_light = METALLIC_BRONZE_LIGHT
    else:  # silver
        matrix_color = METALLIC_SILVER
        matrix_light = METALLIC_SILVER_LIGHT
    
    matrix_rgb = hex_to_rgb(matrix_color)
    matrix_light_rgb = hex_to_rgb(matrix_light)
    
    # Draw matrix code characters
    char_size = max(8, width // 40)
    chars = "01"
    
    for y in range(0, height, char_size):
        for x in range(0, width, char_size * 2):
            # Random character
            char = chars[x % len(chars)]
            
            # Varying opacity for depth
            opacity = 0.3 + (x + y) % 3 * 0.2
            
            # Draw character
            try:
                # Use a simple font or default
                font = ImageFont.load_default()
            except:
                font = None
            
            # Create semi-transparent effect
            color = tuple(int(c * opacity) for c in matrix_rgb)
            
            # Draw as small rectangles to simulate code
            if (x + y) % 7 == 0:
                draw.rectangle([x, y, x + char_size - 2, y + char_size - 2], 
                              fill=color, outline=None)
            elif (x + y) % 11 == 0:
                draw.rectangle([x, y, x + char_size - 1, y + char_size - 1], 
                              fill=matrix_light_rgb, outline=None)
    
    return img

def create_b24_silhouette(width, height):
    """Create B-24 Liberator bomber silhouette based on reference image."""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # B-24 characteristic features from reference:
    # - High-mounted wing (positioned high on fuselage)
    # - Four engine nacelles with propellers
    # - Twin tail booms (H-tail configuration)
    # - Long, slender fuselage
    # - Star insignia on fuselage
    
    center_x = width // 2
    center_y = height // 2
    
    # Position aircraft slightly to the right (as in reference)
    offset_x = width * 0.05
    
    # Main fuselage (long and slender, positioned left of center)
    fuselage_width = width * 0.12
    fuselage_length = height * 0.5
    fuselage_x = center_x - width * 0.25 + offset_x
    fuselage_y = center_y - fuselage_length // 2
    
    # Draw fuselage as elongated ellipse
    draw.ellipse([fuselage_x, fuselage_y, 
                  fuselage_x + fuselage_width, 
                  fuselage_y + fuselage_length],
                 fill=(184, 115, 51, 255),  # Copper
                 outline=(212, 175, 55, 255),  # Gold outline
                 width=max(1, width // 256))
    
    # High-mounted wing (positioned high on fuselage)
    wing_span = width * 0.75
    wing_chord = height * 0.08
    wing_y = center_y - height * 0.2  # High on fuselage
    
    # Left wing (extends from fuselage)
    wing_left_x = fuselage_x + fuselage_width // 2
    wing_left_end = center_x - wing_span // 2 + offset_x
    
    # Draw left wing
    draw.polygon([
        (wing_left_x, wing_y),
        (wing_left_end, wing_y),
        (wing_left_end, wing_y + wing_chord),
        (wing_left_x, wing_y + wing_chord)
    ], fill=(212, 175, 55, 255), outline=(205, 127, 50, 255))  # Gold with bronze outline
    
    # Right wing
    wing_right_x = fuselage_x + fuselage_width // 2
    wing_right_end = center_x + wing_span // 2 + offset_x
    
    draw.polygon([
        (wing_right_x, wing_y),
        (wing_right_end, wing_y),
        (wing_right_end, wing_y + wing_chord),
        (wing_right_x, wing_y + wing_chord)
    ], fill=(212, 175, 55, 255), outline=(205, 127, 50, 255))
    
    # Four engine nacelles (2 per wing, on leading edge)
    engine_width = width * 0.06
    engine_height = height * 0.1
    engine_y = wing_y + wing_chord // 2 - engine_height // 2
    
    # Left wing engines (outer and inner)
    left_outer_x = wing_left_end + engine_width // 2
    left_inner_x = wing_left_x + (wing_left_end - wing_left_x) * 0.4
    
    # Left outer engine
    draw.ellipse([left_outer_x - engine_width // 2, engine_y,
                  left_outer_x + engine_width // 2, engine_y + engine_height],
                fill=(205, 127, 50, 255),  # Bronze
                outline=(212, 175, 55, 255),  # Gold outline
                width=max(1, width // 256))
    
    # Left inner engine
    draw.ellipse([left_inner_x - engine_width // 2, engine_y,
                  left_inner_x + engine_width // 2, engine_y + engine_height],
                fill=(205, 127, 50, 255),  # Bronze
                outline=(212, 175, 55, 255),  # Gold outline
                width=max(1, width // 256))
    
    # Right wing engines
    right_outer_x = wing_right_end - engine_width // 2
    right_inner_x = wing_right_x + (wing_right_end - wing_right_x) * 0.6
    
    # Right outer engine
    draw.ellipse([right_outer_x - engine_width // 2, engine_y,
                  right_outer_x + engine_width // 2, engine_y + engine_height],
                fill=(205, 127, 50, 255),  # Bronze
                outline=(212, 175, 55, 255),  # Gold outline
                width=max(1, width // 256))
    
    # Right inner engine
    draw.ellipse([right_inner_x - engine_width // 2, engine_y,
                  right_inner_x + engine_width // 2, engine_y + engine_height],
                fill=(205, 127, 50, 255),  # Bronze
                outline=(212, 175, 55, 255),  # Gold outline
                width=max(1, width // 256))
    
    # Propeller on front-most engine (left outer)
    prop_size = engine_width * 1.2
    prop_x = left_outer_x
    prop_y = engine_y + engine_height // 2
    
    # Draw propeller as circle with metallic effect
    draw.ellipse([prop_x - prop_size // 2, prop_y - prop_size // 2,
                  prop_x + prop_size // 2, prop_y + prop_size // 2],
                fill=(192, 192, 192, 200),  # Semi-transparent silver
                outline=(212, 175, 55, 255),  # Gold outline
                width=max(1, width // 256))
    
    # Twin tail booms (H-tail configuration)
    boom_width = width * 0.03
    boom_height = height * 0.3
    boom_y = center_y + height * 0.1
    
    # Left tail boom (extends from left wing)
    left_boom_x = wing_left_end + boom_width // 2
    
    draw.ellipse([left_boom_x - boom_width // 2, boom_y,
                  left_boom_x + boom_width // 2, boom_y + boom_height],
                fill=(192, 192, 192, 255),  # Silver
                outline=(212, 175, 55, 255),  # Gold outline
                width=max(1, width // 256))
    
    # Right tail boom (extends from right wing)
    right_boom_x = wing_right_end - boom_width // 2
    
    draw.ellipse([right_boom_x - boom_width // 2, boom_y,
                  right_boom_x + boom_width // 2, boom_y + boom_height],
                fill=(192, 192, 192, 255),  # Silver
                outline=(212, 175, 55, 255),  # Gold outline
                width=max(1, width // 256))
    
    # Horizontal stabilizer connecting the two booms (H-tail)
    stabilizer_y = boom_y + boom_height * 0.7
    stabilizer_width = right_boom_x - left_boom_x
    stabilizer_height = height * 0.02
    
    draw.rectangle([left_boom_x, stabilizer_y,
                    right_boom_x, stabilizer_y + stabilizer_height],
                  fill=(212, 175, 55, 255),  # Gold
                  outline=(205, 127, 50, 255))  # Bronze outline
    
    # Vertical stabilizers (fins) on each boom
    fin_width = width * 0.04
    fin_height = height * 0.12
    
    # Left fin
    draw.polygon([
        (left_boom_x, boom_y + boom_height),
        (left_boom_x - fin_width // 2, boom_y + boom_height + fin_height),
        (left_boom_x + fin_width // 2, boom_y + boom_height + fin_height)
    ], fill=(212, 175, 55, 255), outline=(205, 127, 50, 255))  # Gold with bronze outline
    
    # Right fin
    draw.polygon([
        (right_boom_x, boom_y + boom_height),
        (right_boom_x - fin_width // 2, boom_y + boom_height + fin_height),
        (right_boom_x + fin_width // 2, boom_y + boom_height + fin_height)
    ], fill=(212, 175, 55, 255), outline=(205, 127, 50, 255))
    
    # Star insignia on fuselage (towards rear, as in reference)
    star_x = fuselage_x + fuselage_width * 0.6
    star_y = center_y + height * 0.05
    star_size = width * 0.03
    
    # Draw five-pointed star
    star_points = []
    for i in range(10):  # 5 points, 2 vertices each
        angle = (i * math.pi / 5) - (math.pi / 2)
        if i % 2 == 0:
            # Outer point
            radius = star_size
        else:
            # Inner point
            radius = star_size * 0.4
        x = star_x + radius * math.cos(angle)
        y = star_y + radius * math.sin(angle)
        star_points.append((x, y))
    
    draw.polygon(star_points, fill=(255, 255, 255, 255), outline=(212, 175, 55, 255))  # White star with gold outline
    
    return img

def create_icon(size=512, color_scheme='gold'):
    """Create complete icon with bomber and matrix background."""
    # Create matrix background
    bg = create_matrix_background(size, size, color_scheme)
    
    # Create bomber silhouette
    bomber = create_b24_silhouette(size, size)
    
    # Composite: bomber over matrix
    icon = Image.alpha_composite(bg.convert('RGBA'), bomber)
    
    return icon.convert('RGB')

def create_icon_set():
    """Create icon in all required sizes for macOS."""
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    
    # Create assets directory
    os.makedirs('assets', exist_ok=True)
    
    # Generate PNG icons
    for size in sizes:
        icon = create_icon(size, 'gold')
        icon_path = f'assets/icon_{size}x{size}.png'
        icon.save(icon_path, 'PNG')
        print(f"✅ Created {icon_path}")
    
    # Create iconset directory structure for .icns
    iconset_dir = 'assets/icon.iconset'
    os.makedirs(iconset_dir, exist_ok=True)
    
    # Create iconset files with proper naming (required by iconutil)
    iconset_files = {
        'icon_16x16.png': 16,
        'icon_16x16@2x.png': 32,
        'icon_32x32.png': 32,
        'icon_32x32@2x.png': 64,
        'icon_128x128.png': 128,
        'icon_128x128@2x.png': 256,
        'icon_256x256.png': 256,
        'icon_256x256@2x.png': 512,
        'icon_512x512.png': 512,
        'icon_512x512@2x.png': 1024,
    }
    
    print("\n📦 Creating iconset for .icns file...")
    for iconset_name, size in iconset_files.items():
        icon = create_icon(size, 'gold')
        iconset_path = os.path.join(iconset_dir, iconset_name)
        icon.save(iconset_path, 'PNG')
        print(f"   Created {iconset_name}")
    
    # Create .icns file using iconutil (macOS)
    print("\n📦 Creating .icns file...")
    icns_path = 'assets/icon.icns'
    result = os.system(f'iconutil -c icns "{iconset_dir}" -o "{icns_path}" 2>&1')
    
    if result == 0:
        print(f"✅ Created {icns_path}")
    else:
        print("⚠️  Could not create .icns (iconutil may not be available)")
        print("   Using 512x512 PNG as fallback - app will use PNG icon")

if __name__ == '__main__':
    print("🎨 Generating Liberator app icon...")
    print("   B-24 bomber silhouette over matrix code")
    print("   Metallic colors: Copper, Gold, Bronze, Silver\n")
    
    create_icon_set()
    
    # Also create a single high-res icon for direct use
    icon_512 = create_icon(512, 'gold')
    icon_512.save('assets/icon.png', 'PNG')
    print("\n✅ Main icon saved to: assets/icon.png")
