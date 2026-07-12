import cv2

# Window Configuration
WINDOW_NAME = "AirCanvas"
WIDTH = 1280
HEIGHT = 720
FPS_TARGET = 30

# Brush Configuration
DEFAULT_BRUSH_SIZE = 5
DEFAULT_ERASER_SIZE = 40
SMOOTHING_FACTOR = 0.45  # EMA smoothing factor (0 = no smoothing, 1 = maximum smoothing)

# Styling Palette (BGR)
COLOR_PALETTE = {
    "RED": (40, 40, 255),      # Vibrantly tailored BGR colors
    "GREEN": (40, 255, 40),
    "BLUE": (255, 100, 40),
    "YELLOW": (0, 230, 230),
    "BLACK": (30, 30, 30),
    "WHITE": (255, 255, 255),
    "GRAY": (180, 180, 180),
    "BG_DARK": (20, 20, 20),
    "HUD_BG": (15, 15, 15),
    "BORDER_GLOW": (0, 255, 255),
    "ERASER_HUD": (200, 200, 200)
}

# Top Toolbar Configuration
TOOLBAR_HEIGHT = 90
BUTTON_PADDING = 10

# Toolbar buttons layout definition
# Type options: "color" (draw with color), "eraser" (erase), "action" (instant trigger)
BUTTONS_CONFIG = [
    {"id": "RED", "label": "RED", "color": COLOR_PALETTE["RED"], "type": "color"},
    {"id": "GREEN", "label": "GREEN", "color": COLOR_PALETTE["GREEN"], "type": "color"},
    {"id": "BLUE", "label": "BLUE", "color": COLOR_PALETTE["BLUE"], "type": "color"},
    {"id": "YELLOW", "label": "YELLOW", "color": COLOR_PALETTE["YELLOW"], "type": "color"},
    {"id": "BLACK", "label": "BLACK", "color": COLOR_PALETTE["BLACK"], "type": "color"},
    {"id": "ERASER", "label": "ERASER", "color": COLOR_PALETTE["GRAY"], "type": "eraser"},
    {"id": "CLEAR", "label": "CLEAR", "color": (50, 50, 180), "type": "action"},
    {"id": "SAVE", "label": "SAVE", "color": (50, 180, 50), "type": "action"}
]
