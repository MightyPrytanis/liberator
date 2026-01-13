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
    """Create B-24 Liberator bomber silhouette."""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # B-24 characteristic features:
    # - Twin tail booms
    # - High wing
    # - Four engines (two on each wing)
    # - Distinctive fuselage
    
    center_x = width // 2
    center_y = height // 2
    
    # Main fuselage (central body)
    fuselage_width = width * 0.15
    fuselage_height = height * 0.4
    fuselage_x = center_x - fuselage_width // 2
    fuselage_y = center_y - fuselage_height // 2 + height * 0.1
    
    # Draw fuselage
    draw.ellipse([fuselage_x, fuselage_y, 
                  fuselage_x + fuselage_width, 
                  fuselage_y + fuselage_height],
                 fill=(184, 115, 51, 255),  # Copper
                 outline=(212, 175, 55, 255),  # Gold outline
                 width=2)
    
    # Wings (high wing configuration)
    wing_span = width * 0.85
    wing_width = height * 0.12
    wing_y = center_y - height * 0.15
    
    # Left wing
    draw.ellipse([center_x - wing_span // 2, wing_y,
                  center_x - wing_span // 2 + wing_span * 0.4, wing_y + wing_width],
                fill=(212, 175, 55, 255),  # Gold
                outline=(205, 127, 50, 255),  # Bronze outline
                width=2)
    
    # Right wing
    draw.ellipse([center_x + wing_span // 2 - wing_span * 0.4, wing_y,
                  center_x + wing_span // 2, wing_y + wing_width],
                fill=(212, 175, 55, 255),  # Gold
                outline=(205, 127, 50, 255),  # Bronze outline
                width=2)
    
    # Engine nacelles (4 total - 2 per wing)
    engine_size = width * 0.08
    
    # Left wing engines
    engine_y = wing_y + wing_width // 2 - engine_size // 2
    draw.ellipse([center_x - wing_span * 0.3 - engine_size // 2, engine_y,
                  center_x - wing_span * 0.3 + engine_size // 2, engine_y + engine_size],
                fill=(205, 127, 50, 255),  # Bronze
                outline=(212, 175, 55, 255),  # Gold outline
                width=2)
    
    draw.ellipse([center_x - wing_span * 0.15 - engine_size // 2, engine_y,
                  center_x - wing_span * 0.15 + engine_size // 2, engine_y + engine_size],
                fill=(205, 127, 50, 255),  # Bronze
                outline=(212, 175, 55, 255),  # Gold outline
                width=2)
    
    # Right wing engines
    draw.ellipse([center_x + wing_span * 0.15 - engine_size // 2, engine_y,
                  center_x + wing_span * 0.15 + engine_size // 2, engine_y + engine_size],
                fill=(205, 127, 50, 255),  # Bronze
                outline=(212, 175, 55, 255),  # Gold outline
                width=2)
    
    draw.ellipse([center_x + wing_span * 0.3 - engine_size // 2, engine_y,
                  center_x + wing_span * 0.3 + engine_size // 2, engine_y + engine_size],
                fill=(205, 127, 50, 255),  # Bronze
                outline=(212, 175, 55, 255),  # Gold outline
                width=2)
    
    # Twin tail booms (distinctive B-24 feature)
    boom_width = width * 0.04
    boom_height = height * 0.25
    boom_y = center_y + height * 0.15
    
    # Left boom
    draw.ellipse([center_x - wing_span * 0.25 - boom_width // 2, boom_y,
                  center_x - wing_span * 0.25 + boom_width // 2, boom_y + boom_height],
                fill=(192, 192, 192, 255),  # Silver
                outline=(212, 175, 55, 255),  # Gold outline
                width=2)
    
    # Right boom
    draw.ellipse([center_x + wing_span * 0.25 - boom_width // 2, boom_y,
                  center_x + wing_span * 0.25 + boom_width // 2, boom_y + boom_height],
                fill=(192, 192, 192, 255),  # Silver
                outline=(212, 175, 55, 255),  # Gold outline
                width=2)
    
    # Tail fins
    fin_width = width * 0.06
    fin_height = height * 0.15
    
    # Left fin
    points_left = [
        (center_x - wing_span * 0.25, boom_y + boom_height),
        (center_x - wing_span * 0.25 - fin_width // 2, boom_y + boom_height + fin_height),
        (center_x - wing_span * 0.25 + fin_width // 2, boom_y + boom_height + fin_height)
    ]
    draw.polygon(points_left, fill=(212, 175, 55, 255), outline=(205, 127, 50, 255))
    
    # Right fin
    points_right = [
        (center_x + wing_span * 0.25, boom_y + boom_height),
        (center_x + wing_span * 0.25 - fin_width // 2, boom_y + boom_height + fin_height),
        (center_x + wing_span * 0.25 + fin_width // 2, boom_y + boom_height + fin_height)
    ]
    draw.polygon(points_right, fill=(212, 175, 55, 255), outline=(205, 127, 50, 255))
    
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
