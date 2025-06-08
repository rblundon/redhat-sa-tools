# OpenShift Lifecycle Visualizer

A tool for visualizing OpenShift cluster lifecycle information from database records.

## Features

- Database connectivity with OAuth2 authentication
- VPN connection verification
- EBS account validation
- Account name verification
- Interactive command-line interface

## Prerequisites

- Python 3.8 or higher
- VPN connection to Red Hat network
- Access to the Trino database
- OAuth2 credentials

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ocp-lifecycle-visualizer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script with:
```bash
python ocp-lifecycle-visualizer.py [OPTIONS]
```

### Options

- `--debug`: Enable debug logging
- `--ebs-account`: EBS Account number
- `--username`: Username for database authentication

### Examples

1. Run with all options:
```bash
python ocp-lifecycle-visualizer.py --ebs-account 677861 --username rblundon
```

2. Run with interactive prompts:
```bash
python ocp-lifecycle-visualizer.py
```

## Project Structure

```
ocp-lifecycle-visualizer/
├── modules/
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database connection management
│   └── functions.py       # Utility functions
├── ocp-lifecycle-visualizer.py  # Main script
├── README.md
└── requirements.txt
```

## Error Handling

The script includes error handling for:
- VPN connection verification
- Database connection issues
- Invalid EBS account numbers
- Missing account names
- Database query errors

## Logging

Logging is configured to show:
- INFO level messages by default
- DEBUG level messages when --debug flag is used
- ERROR messages for all error conditions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 