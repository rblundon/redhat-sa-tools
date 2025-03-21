#!/usr/bin/python3
"""
Layout management for the reference image generator.
"""

import logging
import os
from PIL import Image, ImageDraw
from typing import Tuple

from modules.config import *
from modules.functions import mm_to_pixels, add_text_box, add_rotated_text, add_image_box, add_horizontal_line

def generate_reference_image(input_path, output_path, node_counts=None, cluster_name=None, version=None, platform=None, support=None, worker_total_cpu=None, variant="?"):
    """Generate a reference image with the specified parameters."""
    try:
        # Create layout with provided parameters
        layout = ReferenceImageLayout(
            node_counts=node_counts,
            cluster_name=cluster_name,
            version=version,
            platform=platform,
            support=support,
            worker_total_cpu=worker_total_cpu,
            variant=variant
        )
        
        # Draw all elements
        layout.draw_all_elements()
        
        # Save the image
        layout.save(output_path)
        
        return True
    except Exception as e:
        logging.error(f"Error generating reference image: {e}")
        return False

def get_icon_path(support_level: str) -> str:
    """Get the path to the appropriate icon based on support level.
    
    Args:
        support_level (str): The support level (Premium, Standard, Eval, None)
        
    Returns:
        str: Path to the icon image file
    """
    logger = logging.getLogger(__name__)
    
    # Normalize the support level string
    support_level = support_level.lower().strip()
    
    # Map support levels to icon filenames
    icon_map = {
        'premium': 'ocp-premium.png',
        'standard': 'ocp-standard.png',
        'eval': 'ocp-eval.png',
        'none': 'ocp-none.png'
    }
    
    # Get the icon filename, default to none if not found
    if support_level not in icon_map:
        logger.warning(f"Unknown support level '{support_level}', defaulting to 'none'")
        icon_file = 'ocp-none.png'
    else:
        icon_file = icon_map[support_level]
    
    # Construct the full path
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reference', 'images', icon_file)

class ReferenceImageLayout:
    """Manages the layout and drawing of the reference image."""
    
    def __init__(self, node_counts=None, cluster_name=None, version=None, platform=None, support=None, worker_total_cpu=None, variant="?"):
        """Initialize the layout with dimensions from config."""
        self.logger = logging.getLogger(__name__)
        self.pixel_width = mm_to_pixels(IMAGE_WIDTH_MM, DPI)
        self.pixel_height = mm_to_pixels(IMAGE_HEIGHT_MM, DPI)
        self.size = (self.pixel_width, self.pixel_height)
        
        # Store node counts, cluster name, and version
        self.node_counts = node_counts or {
            'master': 0,
            'infrastructure': 0,
            'worker': 0
        }
        self.cluster_name = cluster_name or 'Name Box'
        self.version = version or 'Version'
        self.platform = platform or 'Unknown'
        self.support = support or 'None'
        self.worker_total_cpu = worker_total_cpu or 0
        self.variant = variant
        
        # Create base image
        self.image = Image.new('RGBA', self.size, (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)
        
        # Calculate all positions
        self._calculate_positions()
        
    def _calculate_positions(self) -> None:
        """Calculate all box positions and dimensions."""
        try:
            # Title box
            self.title_box_height = mm_to_pixels(TITLE_BOX_HEIGHT_MM)
            self.title_box_left = mm_to_pixels(TITLE_BOX_MARGIN_MM)
            self.title_box_width = self.pixel_width - (2 * self.title_box_left)
            self.title_box_top = 0
            self.title_box_bottom = self.title_box_height
            
            # Icon box
            self.icon_box_size = mm_to_pixels(ICON_BOX_SIZE_MM)
            self.icon_box_left = (self.pixel_width - self.icon_box_size) // 2
            self.icon_box_top = self.title_box_bottom
            
            # Left column
            self.left_box_size = mm_to_pixels(LEFT_BOX_SIZE_MM)
            self.left_box_left = 0
            self.left_box_start_top = mm_to_pixels(LEFT_BOX_START_TOP_MM)
            
            # Calculate positions for each box in the left column
            self.cp_box_top = self.left_box_start_top
            self.cp_box_bottom = self.cp_box_top + self.left_box_size
            
            self.infra_box_top = mm_to_pixels(40)
            self.infra_box_bottom = self.infra_box_top + self.left_box_size
            
            self.worker_box_top = mm_to_pixels(60)
            self.worker_box_bottom = self.worker_box_top + self.left_box_size
            
            # Name box
            self.name_box_height = mm_to_pixels(20)
            self.name_box_top = self.worker_box_bottom
            self.name_box_bottom = self.name_box_top + self.name_box_height
            
            # Right column
            self.right_column_width = mm_to_pixels(RIGHT_COLUMN_WIDTH_MM)
            self.right_column_left = self.pixel_width - self.right_column_width
            
            self.logger.debug("All positions calculated successfully")
            
        except Exception as e:
            self.logger.error(f"Error calculating positions: {e}")
            raise
    
    def draw_all_elements(self) -> None:
        """Draw all elements on the image."""
        try:
            # Add all elements
            formatted_cpu = "{:,}".format(self.worker_total_cpu)
            right_column_text = f"{self.platform} ({formatted_cpu} vCPU)"
            add_rotated_text(
                self.image, right_column_text,
                self.right_column_left, 0,
                self.right_column_width, self.pixel_height,
                font_size=7.5,
                color=TEXT_COLOR
            )
            
            add_text_box(
                self.draw, f'{self.variant} - {self.version}',
                self.title_box_left, self.title_box_top,
                self.title_box_width, self.title_box_height,
                font_size=7.5,
                color=TEXT_COLOR,
                bold=False
            )
            
            # Use 7.5mm font size for all text
            font_size = 7.5
            
            # Format node counts with comma separators
            master_count = "{:,}".format(self.node_counts["master"])
            infra_count = "{:,}".format(self.node_counts["infrastructure"])
            worker_count = "{:,}".format(self.node_counts["worker"])
            
            add_text_box(
                self.draw, master_count,
                self.left_box_left, self.cp_box_top,
                self.left_box_size, self.left_box_size,
                font_size=font_size,
                color=TEXT_COLOR,
                bold=False
            )
            
            add_text_box(
                self.draw, infra_count,
                self.left_box_left, self.infra_box_top,
                self.left_box_size, self.left_box_size,
                font_size=font_size,
                color=TEXT_COLOR,
                bold=False
            )
            
            add_text_box(
                self.draw, worker_count,
                self.left_box_left, self.worker_box_top,
                self.left_box_size, self.left_box_size,
                font_size=font_size,
                color=TEXT_COLOR,
                bold=False
            )
            
            add_text_box(
                self.draw, self.cluster_name,
                0, self.name_box_top,
                self.pixel_width, self.name_box_height,
                font_size=font_size,
                color=TEXT_COLOR,
                bold=True  # Only the cluster name is bold
            )
            
            # Get the appropriate icon based on support level
            icon_path = get_icon_path(self.support)
            add_image_box(
                self.image, icon_path,
                self.icon_box_left, self.icon_box_top,
                self.icon_box_size
            )
            
            # Add horizontal lines
            for y_pos in HORIZONTAL_LINE_Y_POSITIONS_MM:
                add_horizontal_line(
                    self.draw, y_pos,
                    start_x_mm=HORIZONTAL_LINE_START_X_MM,
                    end_x_mm=HORIZONTAL_LINE_END_X_MM,
                    color=LINE_COLOR,
                    width=LINE_WIDTH_PX
                )
            
            self.logger.debug("All elements drawn successfully")
            
        except Exception as e:
            self.logger.error(f"Error drawing elements: {e}")
            raise
    
    def save(self, output_path) -> None:
        """Save the image to file."""
        try:
            self.image.save(output_path, 'PNG')
            self.logger.info(f"Image saved successfully to {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving image: {e}")
            raise 