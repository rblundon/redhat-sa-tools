"""
Module for command line argument parsing.
"""

import argparse

def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Set logging levels and specify an input file.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--debug", action="store_const", const="debug", dest="verbosity",
                      help="Set logging level to DEBUG")
    group.add_argument("-v", "--verbose", action="store_const", const="verbose", dest="verbosity",
                      help="Set logging level to INFO (verbose)")
    
    parser.add_argument("-f", "--file", type=str, help="Input file path")
    parser.add_argument("--generate-images", action="store_true", help="Generate reference images and display node counts")
    #parser.add_argument("--image-input", type=str, help="Input image path for reference image generation (default: eval.png)")
    #parser.add_argument("--image-output", type=str, help="Output path for generated reference image (default: reference.png)")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")

    args = parser.parse_args()
    
    # Validate arguments
    if not args.generate_images and not args.file:
        parser.error("the following arguments are required: -f/--file")
    
    return args 