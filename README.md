# redhat-sa-tools
A set of tools to quickly vlisualize OpenShift cluster data. 

## Table of Contents
- [Installation](#installation)
- [Tools](#Tools)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Contributors](#contributors)
- [License](#license)

## Installation

### Setting Up the Virtual Environment

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
   pip install -r </path/to/your/repo>/ocp-visualizer/requirements.txt
   ```
## Tools

- [OpenShift Cluster Visualizer](ocp-visualizer/README.md)

### Roadmap
List of enhancements/new products planned for the Red Hat SA Toolkit.

- Specify output directory (flag or prompt)
- Direct SQL query
- Google docs integration

### Contributing
We welcome pull requests from the community! 
<!-- Please read our contribution guidelines before submitting your pull request. -->

### Contributors
Thank you to all who have contributed to this project! Your name will be added to the list when your PR has been approved.

- Ryan Blundon, Sr. Solutions Architect

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.