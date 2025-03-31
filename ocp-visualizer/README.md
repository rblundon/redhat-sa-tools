# redhat-sa-tools

A set of tools to quickly vlisualize OpenShift cluster data.

## Table of Contents

- [Usage](#usage)
- [License](#license)

## Usage

### Getting data for the script to process

- Log in to Support Sense | Cluster Browser
- Filter the list to the clusters you want visualizations for.
- Download Crosstab (Select "clusters" sheet and "CSV" format).
- Download Cluster Node data ("Nodes" tab) as CSV with the filename "<cluster_id>.csv"

   **(All files must reside in the same folder to be processed.)**

(Please email/slack me for access to a detailed walkthrough of data acquisition)

### Running the Script

To execute the script from the command line, use the following steps:

1. Ensure the virtual environment is activated:

   ```bash
   source ~/redhat-sa-tools/bin/activate
   ```

2. Navigate to the directory containing the script:

   ```bash
   cd /path/to/your/repo/ocp-visualizer
   ```

3. Run the script with the required arguments:

   ```bash
   usage: ocp-visualizer.py [-h] [-d | -v] [-f FILE] [--generate-images] [--html]
   ```

   - Replace `<input_file_path>` with the path to your cluster export CSV file.
   - Use `--generate-images` to to create one image per cluster.
   - Use `--html` to to create one html file per cluster.
   - Use `-d` for debug logging or `-v` for verbose logging.

\* Note output directory is currently hard coded on Line 31 of ocp-visualizer.py

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
