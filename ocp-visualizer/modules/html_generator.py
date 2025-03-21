"""
Module for generating HTML output.
"""

import os
import shutil
from airium import Airium

def create_folder(folder_path):
    """Creates a folder if it doesn't exist."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def table_header(a, cluster_name):
    """Generates the table header in the HTML."""
    with a.div(klass="header"):
        with a.div(klass="logo"):
            a.img(src="ocp-logo.png", alt="OpenShift Logo", height="100")
        with a.div(klass="cluster-info"):
            with a.div(klass="cluster-name"):
                a(cluster_name)
            with a.div(klass="node-types"):
                a("Control Plane")
                a("Infrastructure")
                a("Worker")

def node_column(a, nodes, node_type):
    """Generates a column of node information in the HTML."""
    total_cpu = 0
    total_memory = 0
    
    column_class = {
        "Control Plane": "left-column",
        "Infrastructure": "center-column",
        "Worker": "right-column"
    }.get(node_type, "column")
    
    with a.div(klass=f"node-column {column_class}"):
        with a.div(klass="node-type"):
            a(node_type)
        
        with a.div(klass="nodes-container"):
            # Group nodes by CPU and memory combination
            node_groups = {}
            for node_name, data in nodes.items():
                cpu = int(float(data.get('CPU', 0)))
                memory = float(data.get('Memory', 0))
                spec_key = f"{cpu}-{memory}"
                if spec_key not in node_groups:
                    node_groups[spec_key] = {
                        'cpu': cpu,
                        'memory': memory,
                        'nodes': []
                    }
                node_groups[spec_key]['nodes'].append(node_name)
                total_cpu += cpu
                total_memory += memory
            
            # Render each group
            for spec_key, group in sorted(node_groups.items(), key=lambda x: (x[1]['cpu'], x[1]['memory']), reverse=True):
                with a.div(klass="node-group"):
                    with a.div(klass="node-specs"):
                        with a.div(klass="spec"):
                            a(f"CPU: {group['cpu']}")
                        with a.div(klass="spec"):
                            a(f"Memory: {group['memory']:.2f} GB")
                    
                    with a.div(klass="node-list"):
                        for node_name in sorted(group['nodes']):
                            with a.div(klass="node"):
                                with a.div(klass="node-name"):
                                    a(node_name)
    
    return total_cpu, total_memory

def node_footer(a, total_cpu, total_memory, node_type):
    """Generates the footer for a node column in the HTML."""
    column_class = {
        "Control Plane": "left-column",
        "Infrastructure": "center-column",
        "Worker": "right-column"
    }.get(node_type, "column")
    
    with a.div(klass=f"node-footer {column_class}"):
        with a.div(klass="node-type"):
            a(node_type)
        with a.div(klass="total-specs"):
            with a.div(klass="total-cpu"):
                a(f"Total vCPU: {total_cpu}")
            with a.div(klass="total-memory"):
                a(f"Total Memory: {total_memory:.2f} GB")

def generate_html_report(cluster_id, cluster_name, cluster_version, master_nodes, 
                        infrastructure_nodes, worker_nodes, file_date, output_folder, 
                        css_file, openshift_logo):
    """Generates the complete HTML report for a cluster."""
    a = Airium()
    a('<!DOCTYPE html>')
    with a.html(lang="en"):
        with a.head():
            a.meta(charset="utf-8")
            a.meta(name="viewport", content="width=device-width, initial-scale=1.0")
            a.title(_t=f"Cluster Report - {cluster_name}")
            a.link(rel="stylesheet", href=css_file)
        
        with a.body():
            with a.div(klass="container"):
                with a.div(klass="cluster-header"):
                    with a.div(klass="cluster-id"):
                        a(f"Cluster ID: {cluster_id}")
                    with a.div(klass="cluster-version"):
                        a(f"Version: {cluster_version}")
                
                table_header(a, cluster_name)
                
                with a.div(klass="content"):
                    with a.div(klass="row"):
                        (master_total_cpu, master_total_memory) = node_column(a, master_nodes, "Control Plane")
                        (infrastructure_total_cpu, infrastructure_total_memory) = node_column(a, infrastructure_nodes, "Infrastructure")
                        (worker_total_cpu, worker_total_memory) = node_column(a, worker_nodes, "Worker")

                    with a.div(klass="footer-row"):
                        node_footer(a, master_total_cpu, master_total_memory, "Control Plane")
                        node_footer(a, infrastructure_total_cpu, infrastructure_total_memory, "Infrastructure")
                        node_footer(a, worker_total_cpu, worker_total_memory, "Worker")

                with a.div(klass="file-date"):
                    a(f"Current as of: {file_date}")

    # Create output folder and copy supporting files
    create_folder(output_folder)
    shutil.copy2(css_file, output_folder)
    shutil.copy2(openshift_logo, output_folder)

    # Write the HTML file
    html_file = os.path.join(output_folder, f"{cluster_name}.html")
    with open(html_file, "w") as file:
        file.write(str(a))
    
    return worker_total_cpu 