# redhat-sa-tools

## Setting Up the Virtual Environment

To set up the virtual environment, follow these steps:

1. Ensure you have Python 3 and `venv` installed on your system.
2. Navigate to your home directory:

   ```bash
   cd ~
   ```

3. Create a virtual environment named `redhat-sa-tools`:

   ```bash
   python3 -m venv redhat-sa-tools
   ```

4. Activate the virtual environment:

   ```bash
   source redhat-sa-tools/bin/activate
   ```

5. Install the required packages:

   ```bash
   pip install -r /path/to/your/repo/ocp-visualizer/requirements.txt
   ```

## Running the Script

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
   python ocp-visualizer.py -f <input_file_path> [--counts] [-d | -v]
   ```
   - Replace `<input_file_path>` with the path to your input CSV file.
   - Use `--counts` to display node counts.
   - Use `-d` for debug logging or `-v` for verbose logging.