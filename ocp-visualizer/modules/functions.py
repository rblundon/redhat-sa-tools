#!/usr/bin/python3
"""
Functions for image manipulation and drawing.

This module provides utility functions for creating and manipulating images,
with a focus on drawing text, lines, and placing images in specific positions.
All measurements are in millimeters and are converted to pixels based on DPI.
"""

from PIL import Image, ImageDraw, ImageFont
from typing import Tuple, Union
from modules.config import DEFAULT_FONT, BOLD_FONT, BASE_DPI
import logging

# Set the base DPI for the image (300 is standard for print)
BASE_DPI = 300

def mm_to_pixels(mm: float, dpi: int = BASE_DPI) -> int:
    """
    Convert millimeters to pixels based on DPI.

    Args:
        mm: Length in millimeters
        dpi: Dots per inch (default: 300)

    Returns:
        int: Length in pixels

    Note:
        Uses the formula: pixels = (mm * dpi) / 25.4
        where 25.4 is the number of millimeters in an inch
    """
    return int((mm * dpi) / 25.4)

def add_text_box(
    draw: ImageDraw.ImageDraw,
    text: str,
    x: int,
    y: int,
    width: int,
    height: int,
    font_size: float = 5,
    color: str = 'white',
    bold: bool = False
) -> None:
    """
    Add a text box with centered text.

    Args:
        draw: PIL ImageDraw object to draw on
        text: Text to display
        x: X coordinate of box top-left corner
        y: Y coordinate of box top-left corner
        width: Width of box in pixels
        height: Height of box in pixels
        font_size: Font size in millimeters (default: 5)
        color: Text color (default: 'white')
        bold: Whether to use bold font (default: False)
    """
    font_path = BOLD_FONT if bold else DEFAULT_FONT
    draw.text(
        (x + width/2, y + height/2),
        text,
        fill=color,
        anchor='mm',
        font=ImageFont.truetype(font_path, mm_to_pixels(font_size))
    )

def add_rotated_text(
    image: Image.Image,
    text: str,
    x: int,
    y: int,
    width: int,
    height: int,
    font_size: float = 8,
    color: str = 'white'
) -> None:
    """
    Add rotated text (90 degrees counterclockwise).

    Args:
        image: PIL Image to add text to
        text: Text to display
        x: X coordinate for text placement
        y: Y coordinate for text placement
        width: Width of text area in pixels
        height: Height of text area in pixels
        font_size: Font size in millimeters (default: 8)
        color: Text color (default: 'white')
    """
    text_img = Image.new('RGBA', (height, width), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_img)
    font = ImageFont.truetype(DEFAULT_FONT, mm_to_pixels(font_size))
    text_draw.text(
        (height/2, width/2),
        text,
        fill=color,
        anchor='mm',
        font=font
    )
    text_img = text_img.rotate(90, expand=True)
    image.paste(text_img, (x, y), text_img)

def add_image_box(
    image: Image.Image,
    img_path: str,
    x: int,
    y: int,
    size: int
) -> None:
    """
    Add an image box with the specified image.

    Args:
        image: PIL Image to add the image to
        img_path: Path to the image file
        x: X coordinate for image placement
        y: Y coordinate for image placement
        size: Size in pixels (both width and height)

    Note:
        The image will be resized to size x size pixels using LANCZOS resampling
    """
    img = Image.open(img_path)
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    image.paste(img, (x, y))

def add_horizontal_line(
    draw: ImageDraw.ImageDraw,
    y_mm: float,
    start_x_mm: float = 0,
    end_x_mm: float = 20,
    color: str = 'white',
    width: int = 2
) -> None:
    """
    Add a horizontal line at the specified y position.

    Args:
        draw: PIL ImageDraw object to draw on
        y_mm: Y position in millimeters
        start_x_mm: Starting X position in millimeters (default: 0)
        end_x_mm: Ending X position in millimeters (default: 20)
        color: Line color (default: 'white')
        width: Line width in pixels (default: 2)
    """
    draw.line(
        [(mm_to_pixels(start_x_mm), mm_to_pixels(y_mm)), 
         (mm_to_pixels(end_x_mm), mm_to_pixels(y_mm))],
        fill=color,
        width=width
    ) 