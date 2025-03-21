"""
Module for processing cluster data and files.
"""

import csv
import os
import logging
from datetime import datetime
from collections import defaultdict

def read_cluster_csv_file(file_path):
    """Reads and processes the cluster CSV file."""
    clusters = {}
    try:
        with open(file_path, newline='', encoding='utf-16') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')  # Assuming tab-separated values
            
            # Skip header rows
            next(reader)  # Skip the first line (garbage)
            headers = next(reader)  # Read actual headers
            
            # Convert to DictReader for named field access
            reader = csv.DictReader(csvfile, fieldnames=headers, delimiter='\t')
            
            # Process the data
            for row in reader:
                if not row or not row["Cluster Id"]:  # Skip empty rows
                    continue
                    
                cluster_id = row["Cluster Id"]
                clusters[cluster_id] = {
                    "EBS Account": row["EBS Account"],
                    "Account": row["Account"],
                    "Version": row["Version"],
                    "EOL": row["EOL"] == "True",
                    "Support": row["Support"],
                    "Platform": row["Platform"],
                    "Network Type": row["Network Type"],
                    "Install Type": row["Install Type"],
                    "Managed Product": row["Managed Product"],
                    "Update Risk": row["Update Risk"],
                    "CI": row["ci"] == "True",
                    "Initial Version": row["Initial Version"],
                    "Last Seen": row["Last Seen"],
                    "Associates": row["Associates"] if row["Associates"] else None,
                    "Desired Version": row["Desired Version"],
                    "Install Date": row["Install Date"],
                    "UPI": row["upi"] == "ⓘ"  # Check for the UPI indicator
                }
                
                # Check for 'Variant' key
                if "Variant" not in row:
                    logging.error(f"Missing 'Variant' key for cluster ID {cluster_id}. Setting to '?' by default.")
                    clusters[cluster_id]["Variant"] = "?"
                else:
                    clusters[cluster_id]["Variant"] = row["Variant"]
                
        logging.debug(f"CSV Data: {clusters}")
        return clusters
    
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")

    return None  # Return None if there was an error

def get_file_creation_date(cluster_file):
    """Gets the creation date of the cluster file."""
    try:
        timestamp = os.path.getctime(cluster_file)
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except Exception as e:
        logging.error(f"Error getting file creation date: {e}")
        return "Unknown"

def process_cluster_data(cluster_file):
    """Processes the cluster data from the CSV file."""
    node_info = {}
    
    try:
        with open(cluster_file, 'r', encoding='utf-16') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                node_info[row['Host Name']] = {
                    'CPU': row['Cores'],
                    'Memory': row['Memory (GB)'],
                    'Node Role': ' '.join(eval(row['Roles']))  # Convert string list to space-separated roles
                }
    except Exception as e:
        logging.error(f"Error processing cluster data: {e}")
    
    return node_info

def process_node_data(node_info, node_type):
    """Processes node data for a specific node type."""
    nodes = {}
    for node_name, data in node_info.items():
        if node_type.lower() in data.get('Node Role', '').lower():
            nodes[node_name] = data
    return nodes

def get_cluster_name(node_names):
    """Extracts the cluster name from node names."""
    if not node_names:
        return "Unknown Cluster"
    
    # Find the common prefix among node names
    prefix = os.path.commonprefix(node_names)
    if prefix:
        # Remove any trailing hyphens or underscores
        return prefix.rstrip('-_')
    return "Unknown Cluster" 