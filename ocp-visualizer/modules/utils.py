"""
Module for utility functions.
"""

import os
import logging
from difflib import SequenceMatcher

def to_upper_camel_case(s):
    """Converts a string to upper camel case."""
    if not s:
        return ""
    words = s.split()
    return ''.join(word.capitalize() for word in words)

def setup_logging(verbosity):
    """Sets up logging based on the verbosity flag."""
    log_levels = {
        "debug": logging.DEBUG,
        "verbose": logging.INFO,
        "error": logging.ERROR
    }
    
    logging.basicConfig(level=log_levels.get(verbosity, logging.ERROR),
                       format="%(asctime)s - %(levelname)s - %(message)s")

def generate_reference_image(input_path, output_path, node_counts=None, cluster_name=None, version=None, 
                         platform=None, support=None, worker_total_cpu=None):
    """Generates a reference image for layout comparison.
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path where the output image will be saved
        node_counts (dict): Dictionary containing node counts with keys:
            - master: Number of master nodes
            - infrastructure: Number of infrastructure nodes
            - worker: Number of worker nodes
        cluster_name (str): Name of the cluster to display
        version (str): Version of the cluster to display in title
        platform (str): Platform information
        support (str): Support information
        worker_total_cpu (int): Total worker vCPU count
    """
    try:
        from layout import ReferenceImageLayout
        layout = ReferenceImageLayout(node_counts, cluster_name, version, platform, support, worker_total_cpu)
        layout.draw_all_elements()
        layout.image.save(output_path, 'PNG')
        return True
    except Exception as e:
        logging.error(f"Error generating reference image: {e}")
        return False 