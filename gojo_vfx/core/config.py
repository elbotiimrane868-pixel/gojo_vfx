# config.py
# Central configuration for the Gojo VFX System

# Display Settings
WINDOW_NAME = "Gojo VFX System (Hollow Purple)"
CAM_WIDTH = 1280
CAM_HEIGHT = 720
TARGET_FPS = 30

# Colors (BGR for OpenCV)
COLOR_BLUE = (255, 150, 0)      # BGR for Orange-ish? Wait, it's Blue. B = 255, G = 150, R = 0 -> Cyan/Blue
# Let's fix colors:
COLOR_BLUE = (255, 100, 50)     # Bright Blue
COLOR_RED = (50, 50, 255)       # Bright Red
COLOR_PURPLE = (255, 50, 255)   # Purple
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# Effect Thresholds
GESTURE_HOLD_FRAMES = 10        # Frames a gesture must be held to activate
FUSION_DISTANCE_THRESHOLD_MAX = 400
FUSION_DISTANCE_THRESHOLD_MIN = 50

# Math/Physics limits
MAX_PARTICLES = 500
TRAIL_LENGTH = 10

# Smoothing factor for hand coordinates (0.0 to 1.0, higher is smoother/laggy)
SMOOTHING_FACTOR = 0.5 
