#!/usr/bin/python3
"""
Configuration settings for the reference image generator.
"""

import os

# DPI settings
BASE_DPI = 300

# Directory paths
REFERENCE_DIR = os.path.join(os.path.dirname(__file__), '..', 'reference')
FONTS_DIR = os.path.join(REFERENCE_DIR, 'fonts')
IMAGES_DIR = os.path.join(REFERENCE_DIR, 'images')
CSS_DIR = os.path.join(REFERENCE_DIR, 'css')

# Image dimensions
IMAGE_WIDTH_MM = 100
IMAGE_HEIGHT_MM = 100
DPI = 300

# Colors
TEXT_COLOR = 'white'
LINE_COLOR = 'white'

# Font settings
DEFAULT_FONT = os.path.join(FONTS_DIR, 'RedHatText-Regular.otf')
BOLD_FONT = os.path.join(FONTS_DIR, 'RedHatText-Bold.otf')
TITLE_FONT_SIZE_MM = 5
ROTATED_TEXT_FONT_SIZE_MM = 8
BOX_TEXT_FONT_SIZE_MM = 5

# Layout dimensions (in millimeters)
TITLE_BOX_HEIGHT_MM = 20
TITLE_BOX_MARGIN_MM = 20
ICON_BOX_SIZE_MM = 60
LEFT_BOX_SIZE_MM = 20
LEFT_BOX_START_TOP_MM = 20
RIGHT_COLUMN_WIDTH_MM = 20

# Line settings
LINE_WIDTH_PX = 2
HORIZONTAL_LINE_START_X_MM = 0
HORIZONTAL_LINE_END_X_MM = 20
HORIZONTAL_LINE_Y_POSITIONS_MM = [40, 60]
