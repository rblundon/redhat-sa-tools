#!/usr/bin/python3
"""
Author: Ryan Blundon
Date: 2025-03-19
Description: This script processes node exports from SupportSense and creates a HTML file with node details and a PNG
summary for each cluster.
"""

import argparse
import logging
import csv
import os
import shutil
import datetime
import math
from difflib import SequenceMatcher
from collections import defaultdict
from airium import Airium # pip install airium
import subprocess

home_directory = os.path.expanduser("~")
output_dir = "CustomerDocs"
css_file = "ocp-stylesheet.css"
openshift_logo = "ocp-logo.png"

# Activate the virtual environment
subprocess.call(['source', os.path.join(home_directory, 'redhat-sa-tools', 'bin', 'activate')], shell=True)

def setup_logging(verbosity):
    """Sets up logging based on the verbosity flag."""
    log_levels = {
        "debug": logging.DEBUG,
        "verbose": logging.INFO,
        "error": logging.ERROR
    }
    
    logging.basicConfig(level=log_levels.get(verbosity, logging.ERROR),
                        format="%(asctime)s - %(levelname)s - %(message)s")

def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Set logging levels and specify an input file.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--debug", action="store_const", const="debug", dest="verbosity",
                       help="Set logging level to DEBUG")
    group.add_argument("-v", "--verbose", action="store_const", const="verbose", dest="verbosity",
                       help="Set logging level to INFO (verbose)")
    
    parser.add_argument("-f", "--file", type=str, required=True, help="Input file path")
    parser.add_argument("--counts", action="store_true", help="Display node counts")

    args = parser.parse_args()
    return args.verbosity, args.file, args.counts

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        logging.info(f"Folder created: {folder_path}")
    else:
        logging.info(f"Folder already exists: {folder_path}")

def read_cluster_csv_file(file_path):
    clusters = {}
    try:
        with open(file_path, newline='', encoding='utf-16') as csvfile:
            reader = csv.reader(csvfile, delimiter='\t')  # Assuming tab-separated values
            
            next(reader)  # Skip the first line (garbage)
            
            headers = next(reader)  # Read actual headers
            reader = csv.DictReader(csvfile, fieldnames=headers, delimiter='\t')

            for row in reader:
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
                    "UPI": row["upi"]
                }
        logging.debug(f"CSV Data: {clusters}")

        return clusters
    
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")

    return None  # Return None if there was an error

def cluster_file_exists(file):
    """
    :param file: Path to the file to check.
    :return: True if file exists, False otherwise.
    """

    if os.path.isfile(file+".csv"):
        return True
    else:
        logging.error(f"File does not exist for cluster: {file}")
        return False
    
def get_file_creation_date(clusterId):
    try:
        creation_time = os.path.getctime(clusterId+".csv")
        return datetime.datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d')
    except FileNotFoundError:
        return "File not found"

def process_cluster_data(cluster_id):
    nodes_dict = {}

    logging.info(f"Opening file: {cluster_id}.csv")
    try:
        with open(cluster_id+".csv", mode='r', newline='', encoding='utf-16') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')  # Assuming tab-separated values
            for row in reader:
                hostname = row["Host Name"]
                nodes_dict[hostname] = {
                    "Ready": row["Ready"] == "True",
                    "Node Heartbeat": row["Node Heartbeat"],
                    "Architecture": row["Architecture"],
                    "Cores": int(row["Cores"]),
                    "Memory (GB)": float(row["Memory (GB)"]),
                    "Master": row["Master"] == "True",
                    "Worker": row["Worker"] == "True",
                    "Infra": row["Infra"] == "True",
                    "Roles": eval(row["Roles"])  # Converts string list to Python list
                }
        logging.debug(f"Node Data: {nodes_dict}")

        return nodes_dict
    
    except FileNotFoundError:
        logging.error(f"File not found: {cluster_id}.csv")
    except Exception as e:
        logging.error(f"Error reading file {cluster_id}.csv: {e}")

    return None  # Return None if there was an error

def process_node_data(nodes, node_type):
    logging.debug("In: process_node_data")

    logging.info(f"Processing data for node type: {node_type}")
    if node_type == "Worker":
        node_list = {key: value for key, value in nodes.items() if value.get("Worker") and not value.get("Infra")}
    else:
        node_list = {key: value for key, value in nodes.items() if value.get(node_type)}
    logging.debug(f"Nodes: {node_list}")

    logging.debug("Leaving: process_node_data, Returning node_list")
    return (node_list)

def to_upper_camel_case(text):
    return text.title().replace(" ", "")

def table_header(doc, __cluster_name):
    with doc.div(klass="header"):
        with doc.div(klass="logo"):
            doc.img(src="ocp-logo.png", height="100px")
        with doc.div(style="display:inline-block"):
            with doc.span(klass="clusterName"):
                doc(f"{__cluster_name}")
            doc.br()

            with doc.span(klass="clusterType"):
                doc(f"OpenShift Cluster")

def node_column(doc, node_list, node_type):
    nodetype_total_cpu = 0
    nodetype_total_memory = 0

    logging.debug(node_type, node_list)
    if node_type == "Control Plane":
        div_class = "left-column"
    elif node_type == "Infrastructure":
        div_class = "center-column"
    elif node_type == "Worker":
        div_class = "right-column"

    with doc.div(klass=div_class):
        with doc.p(klass="node"):
            doc(f"{node_type}")
        if node_list:
            (nodetype_total_cpu, nodetype_total_memory) = dict_to_html_table(doc, node_list)
    
    return (nodetype_total_cpu, nodetype_total_memory)

def node_footer(doc ,total_vcpus, total_memory, node_type):
    if node_type == "Control Plane":
        div_class = "left-footer"
    elif node_type == "Infrastructure":
        div_class = "center-footer"
    elif node_type == "Worker":
        div_class = "right-footer"

    with doc.div(klass=div_class):
        with doc.span(klass="left-text"):
            doc(f"Total Memory: ")
            doc.strong(_t=f"{total_memory}") 
        with doc.span(klass="right-text"):
            doc(f"Total vCPUs: ")
            doc.strong(_t=f"{total_vcpus}") 

def dict_to_html_table(aa, data):
    """
    Convert a dictionary to an HTML table.
    :param data: Dictionary with keys as column headers and values as lists of column values
    :return: HTML string
    """
    if not data:
        return "<p>No data available</p>"

    cpu_total = 0
    mem_total = 0
    node_type_count = 1

    grouped_nodes = defaultdict(list)

    for node, specs in data.items():
        key = (specs['Cores'], math.ceil(specs['Memory (GB)']/ 0.98))
        # math.ceil(memory / 0.98) #39.17/40 -> 0.97925 (Memory calculation for above)
        grouped_nodes[key].append(node)

    for specs, node_list in grouped_nodes.items():

        if node_type_count > 1:
            aa.div(klass='spacer')
        
        with aa.div(klass='nodeHeader'):
            with aa.div(klass='top-row'):
                with aa.strong():
                    aa('Node Type ' + str(node_type_count))

            with aa.div(klass='row'):
                with aa.div(klass='left-header'):
                    with aa.div(klass='nodeTextLeft'):
                        aa('vCPU:')
                with aa.div(klass='right-header'):
                    with aa.div(klass='nodeTextRight'):
                        aa('(' + str(specs[0]) + ') vCPU')
            with aa.div(klass='row'):
                with aa.div(klass='left-header'):
                    with aa.div(klass='nodeTextLeft'):
                        aa('Memory:')
                with aa.div(klass='right-header'):
                    with aa.div(klass='nodeTextRight'):
                        aa(str(specs[1]) + ' GiB')

        for i, row in enumerate(node_list):
            if i % 2 ==0:
                divClass = "nodeRowEven"
            else:
                divClass = "nodeRowOdd"

            with aa.div(klass=divClass):
                with aa.div(klass='nodeColumnLeft'):
                    aa(row)
                with aa.div(klass='nodeColumnRight'):
                    aa("Virtual")
            
            cpu_total += specs[0]
            mem_total += specs[1]

        node_type_count += 1

    return (cpu_total, mem_total)

def get_cluster_name(words):
    # Initialize the longest common prefix to the first word
    longest_common_prefix = words[0]

    if "." in longest_common_prefix:  # Hostname-style nodes
        name = longest_common_prefix.split(".")[1]
    elif "-" in longest_common_prefix:  # Cluster-style nodes
        
        # Loop through each word in the list of words
        for word in words[1:]:
            # Loop through each character in the current longest common prefix
            for i in range(len(longest_common_prefix)):
                # If the current character is not the same as the character in the same position in the current word
                if i >= len(word) or longest_common_prefix[i] != word[i]:
                    # Update the longest common prefix and break out of the loop
                    longest_common_prefix = longest_common_prefix[:i]
                    break
        name = "-".join(longest_common_prefix.split("-")[:4])
    else:
        name = longest_common_prefix
 
    # Return the longest common prefix
    return name

def main():
    verbosity, input_file, show_counts = parse_args()
    setup_logging(verbosity)

    logging.debug("Debug mode enabled.")
    logging.info("Verbose mode enabled.")

    logging.info("Script started.")
    logging.info(f"Processing file: {input_file}")

    clusterInfo = read_cluster_csv_file(input_file)

    for cluster, value in clusterInfo.items():
        logging.debug(f"line data: {cluster}")
        cluster_version = value['Version']
        logging.info(f"Cluster Version: {cluster_version}")
        account_name =  to_upper_camel_case(value['Account'])

        if cluster_file_exists(cluster):
            print(f"Processing data for cluster: {cluster}")

            master_nodes = {}
            infrastructure_nodes = {}
            worker_nodes = {}

            logging.info(f"Determining date of data for cluster: {cluster}")
            file_date = get_file_creation_date(cluster)
            logging.info(f"Date of data for cluster is: {file_date}")

            node_info = process_cluster_data(cluster)

            master_nodes = process_node_data(node_info, "Master")
            logging.debug(f"Master Nodes returned: {master_nodes}")
            infrastructure_nodes = process_node_data(node_info, "Infra")
            logging.debug(f"Infrastructure Nodes returned: {infrastructure_nodes}")
            worker_nodes = process_node_data(node_info, "Worker")
            logging.debug(f"Worker Nodes returned: {worker_nodes}")

            cluster_name = get_cluster_name(list(node_info.keys()))
            logging.info(f"Cluster Name: {cluster_name}")

            if show_counts:
                print(f"Cluster Name: {cluster_name}")
                print(f"Master Node Count: {len(master_nodes)}")
                print(f"Infrastructure Node Count: {len(infrastructure_nodes)}")
                print(f"Worker Node Count: {len(worker_nodes)}")

            # Let's start some HTML!
            a = Airium()
            a('<!DOCTYPE html>')

            with a.html().head():
                a.meta(charset="utf-8")
                a.link(rel="stylesheet", href=css_file)

                with a.body(style="font-family:red hat text;"):
                    with a.span(klass="clusterID"):
                        a(f"Cluster ID: {cluster}")
                    with a.span(klass="clusterVersion"):
                        a(f"{cluster_version}")
            
                    table_header(a, cluster_name)
                    with a.div(klass="row"):
                        (master_total_cpu, master_total_memory) = node_column(a, master_nodes, "Control Plane")
                        (infrastructure_total_cpu, infrastructure_total_memory) = node_column(a, infrastructure_nodes, "Infrastructure")
                        (worker_total_cpu, worker_total_memory) = node_column(a, worker_nodes, "Worker")

                    node_footer(a, master_total_cpu, master_total_memory, "Control Plane")
                    node_footer(a, infrastructure_total_cpu, infrastructure_total_memory, "Infrastructure")
                    node_footer(a, worker_total_cpu, worker_total_memory,  "Worker")

                    with a.div(klass="file-date"):
                        a(f"Current as of: {file_date}")

            if show_counts:
                print(f"Worker Node vCPU Count: {worker_total_cpu}")

        output_folder = home_directory + "/Documents/" + output_dir + "/" + account_name
        create_folder(output_folder)

        html_file = output_folder + "/" + cluster_name + ".html"
        logging.info(f"Copying supporting files to: {html_file}")
        shutil.copy2(css_file, output_folder)
        shutil.copy2(openshift_logo, output_folder)

        logging.info(f"Writing outputfile: {output_folder}")
        with open(html_file, "w") as file:
            file.write(str(a))
    
    logging.info("Script finished.")

if __name__ == "__main__":
    main()
