#!/usr/bin/python3
"""
Python Script Template
Author: Ryan Blundon
Date: 2025-02-06
Description: Brief description of what this script does.
"""

import os
import sys
import logging
import subprocess
from modules.arg_parser import parse_args
from modules.utils import setup_logging, to_upper_camel_case
from modules.layout import generate_reference_image
from modules.data_processor import (
    read_cluster_csv_file,
    get_file_creation_date,
    process_cluster_data,
    process_node_data,
    get_cluster_name
)
from modules.html_generator import generate_html_report
from modules.config import REFERENCE_DIR, FONTS_DIR, IMAGES_DIR, CSS_DIR

# Get script directory for relative paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Constants
home_directory = os.path.expanduser("~")
output_dir = "rblundon@redhat.com - Google Drive/My Drive/CustomerDocs"
css_file = os.path.join(CSS_DIR, "ocp-stylesheet.css")
openshift_logo = os.path.join(SCRIPT_DIR, "reference", "images", "ocp-logo.png")

# Activate the virtual environment
subprocess.call(['source', os.path.join(home_directory, 'redhat-sa-tools', 'bin', 'activate')], shell=True)

def ensure_reference_dirs():
    """Ensure reference directories exist."""
    os.makedirs(FONTS_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)

def main():
    """Main entry point for the script."""
    args = parse_args()
    setup_logging(args.verbosity)
    logger = logging.getLogger(__name__)

    # Ensure reference directories exist
    ensure_reference_dirs()

    # Handle image generation if requested without file
    if args.generate_images and not args.file:
        logger.info("Generating reference images...")
        success = generate_reference_image(args.image_input, args.image_output)
        if not success:
            return 1
        return 0

    # Get the directory of the input file for relative paths
    input_file_dir = os.path.dirname(os.path.abspath(args.file))
    
    # Read the cluster information file
    cluster_data = read_cluster_csv_file(args.file)
    if not cluster_data:
        return 1

    logging.info("Script started.")
    logging.info(f"Processing file: {args.file}")

    # Process each cluster
    for cluster_id, cluster_info in cluster_data.items():
        logging.debug(f"Processing cluster: {cluster_id}")
        cluster_version = cluster_info['Version']
        logging.info(f"Cluster Version: {cluster_version}")
        account_name = to_upper_camel_case(cluster_info['Account'])

        logging.info(f"Processing data for cluster: {cluster_id}")

        logging.info(f"Determining date of data for cluster: {cluster_id}")
        # Use input file directory for finding related CSV files
        cluster_csv = os.path.join(input_file_dir, f"{cluster_id}.csv")
        file_date = get_file_creation_date(cluster_csv)
        logging.info(f"Date of data for cluster is: {file_date}")

        node_info = process_cluster_data(cluster_csv)

        master_nodes = process_node_data(node_info, "Master")
        logging.debug(f"Master Nodes returned: {master_nodes}")
        infrastructure_nodes = process_node_data(node_info, "Infra")
        logging.debug(f"Infrastructure Nodes returned: {infrastructure_nodes}")
        worker_nodes = process_node_data(node_info, "Worker")
        logging.debug(f"Worker Nodes returned: {worker_nodes}")

        cluster_name = get_cluster_name(list(node_info.keys()))
        logging.info(f"Cluster Name: {cluster_name}")

        # Generate HTML report only if --html flag is used
        if args.html:
            output_folder = os.path.join(home_directory, output_dir, account_name)
            worker_total_cpu = generate_html_report(
                cluster_id, cluster_name, cluster_version,
                master_nodes, infrastructure_nodes, worker_nodes,
                file_date, output_folder, css_file, openshift_logo
            )
        else:
            worker_total_cpu = sum(int(float(data.get('CPU', 0))) for data in worker_nodes.values())

        # Handle image generation if requested
        if args.generate_images:
            logger.info("Generating reference images...")
            # Create image output filename using cluster name and date
            output_folder = os.path.join(home_directory, output_dir, account_name)
            image_output = os.path.join(output_folder, f"{cluster_name}_{file_date}.png")
            # Ensure output folder exists
            os.makedirs(output_folder, exist_ok=True)
            
            # Prepare node counts for image generation
            node_counts = {
                'master': len(master_nodes),
                'infrastructure': len(infrastructure_nodes),
                'worker': len(worker_nodes)
            }
            
            # Get platform and support info
            platform = cluster_info.get('Platform', 'Unknown')
            support = cluster_info.get('Support', 'Unknown')
            variant = cluster_info.get('Variant', '?')  # Use the 'Variant' value from the cluster data
            
            success = generate_reference_image(args.image_input, image_output, node_counts, cluster_name, cluster_version, 
                                            platform=platform, support=support, worker_total_cpu=worker_total_cpu,
                                            variant=variant)
            if not success:
                return 1
            logging.info(f"Cluster Name: {cluster_name}")
            logging.info(f"Master Node Count: {len(master_nodes)}")
            logging.info(f"Infrastructure Node Count: {len(infrastructure_nodes)}")
            logging.info(f"Worker Node Count: {len(worker_nodes)}")
            logging.info(f"Worker Node vCPU Count: {worker_total_cpu}")
    
    logging.info("Script finished.")

if __name__ == '__main__':
    sys.exit(main())
