# Liberator Metallic Theme

## Overview

Liberator features a luxurious metallic color scheme using **Copper**, **Gold**, **Bronze**, and **Silver** colors for a premium, professional appearance.

## Color Palette

### Primary Colors

**Copper**
- Primary: `#B87333` - Rich copper
- Light: `#CD853F` - Light copper  
- Dark: `#8B4513` - Dark copper
- Used for: Secondary buttons, accents, borders

**Gold**
- Primary: `#D4AF37` - Classic gold
- Light: `#FFD700` - Bright gold
- Dark: `#B8860B` - Dark gold
- Used for: Primary buttons, selected tabs, highlights

**Bronze**
- Primary: `#CD7F32` - Bronze
- Light: `#E6A857` - Light bronze
- Dark: `#8B4513` - Dark bronze
- Used for: Success buttons, headers

**Silver**
- Primary: `#C0C0C0` - Silver
- Light: `#E8E8E8` - Light silver
- Dark: `#808080` - Dark silver
- Used for: Neutral elements, borders, text

### Background Colors
- Primary: `#2C2C2C` - Dark background
- Secondary: `#3A3A3A` - Slightly lighter
- Tertiary: `#4A4A4A` - Even lighter

### Text Colors
- Primary: `#E8E8E8` - Light text
- Secondary: Silver - Secondary text
- Accent: Gold - Accent text

## Button Styles

### Primary Buttons (Gold)
- Main actions like "Liberate Project"
- Gold gradient with dark gold border
- Hover: Brighter gold
- Used for: Primary actions

### Secondary Buttons (Copper)
- Secondary actions
- Copper gradient with dark copper border
- Hover: Lighter copper
- Used for: Secondary actions, repair, refactor

### Success Buttons (Bronze)
- Success/positive actions
- Bronze gradient with dark bronze border
- Hover: Lighter bronze
- Used for: Analyze, auto-fix

### Neutral Buttons (Silver)
- Neutral actions
- Silver gradient with dark silver border
- Hover: Lighter silver
- Used for: Refresh, test, send

## UI Elements

### Tabs
- **Inactive**: Silver gradient
- **Active/Selected**: Gold gradient
- **Hover**: Copper gradient

### Group Boxes
- Copper borders
- Gold titles
- Dark background

### Input Fields
- Dark background with silver borders
- Gold border on focus
- Light text

### Progress Bars
- Silver border
- Gold gradient fill
- Centered text

### Checkboxes
- Silver border (unchecked)
- Gold gradient (checked)
- Copper border on hover

### Lists and Trees
- Dark background
- Gold selection
- Copper hover
- Bronze headers

### Menus
- Dark background
- Gold selection
- Copper hover

## Theme Application

The theme is automatically applied to:
- Main window
- All tabs
- All buttons
- All input fields
- All widgets
- Setup wizard
- All dialogs

## Customization

To customize colors, edit `liberator/gui/theme.py`:

```python
# Change primary gold color
METALLIC_GOLD = "#YOUR_COLOR"

# Update gradients
GOLD_GRADIENT = "qlineargradient(...)"
```

## Visual Hierarchy

1. **Gold** - Most important actions and selections
2. **Copper** - Secondary actions and accents
3. **Bronze** - Success states and headers
4. **Silver** - Neutral elements and borders

## Accessibility

- High contrast between text and backgrounds
- Clear visual hierarchy
- Distinct button states (normal, hover, pressed, disabled)
- Readable text sizes and colors

---

**The metallic theme gives Liberator a premium, professional appearance! ✨**
