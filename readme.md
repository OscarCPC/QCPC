# QCPC - Quantum Computer Program Catalog

A PyQt5-based desktop application for managing computer programs and games.

## Features
- Display program list with details
- Image slideshow for screenshots and box art
- Export data to Excel
- Edit program information
- File management system
- Database integration

## Requirements
- Python 3.x
- PyQt5
- pandas
- openpyxl
- sqlite3

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/qcpc.git

# Change directory
cd qcpc

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Project Structure
```
QCPC/
├── db/
│   └── qcpc.db
├── files/
│   ├── downloads/
│   │   ├── boxart/
│   │   └── screenshot/
│   └── images/
│       ├── boxart/
│       └── screenshot/
└── frames/
    ├── common.py
    ├── qcpc_form.py
    └── qcpc_list.py
```

## Usage
Run the application:
```bash
python main.py
```

## License
[Your chosen license]