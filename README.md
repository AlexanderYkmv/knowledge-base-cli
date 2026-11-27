Knowledge Base CLI application built with Python. It allows users to add, list, view, search and delete knowledge items

Each knowledge item contains:
Unique ID
Title
Content

Features:
Add: Create a new knowledge item
List: Display all saved items
Find by ID: Display the full details of an item by ID
Search by word: Find items by searching a specific word
Delete: Delete an item by ID
Persistence: Knowledge items are stored in an SQLite database and remain available after restarting the application

Requirements:
Python 3.10 or newer
pytest (for running tests)
SQLite is included in Python's standard library, so no additional database installation is required

Setup
Commands for creating a virtual env: 
python -m venv venv
Then activate: (Windows:venv\Scripts\activate), (macOS/Linux:source venv/bin/activate)
Install pytest: pip install pytest

Running the Application: The application can be run using Python's module execution 
python -m knowledge <command>

Commands:
Add item: python -m knowledge add "Example" "Example"
List all: python -m knowledge list
Show by ID: python -m knowledge show ID
Search by word: python -m knowledge search "example"
Delete by ID: python -m knowledge delete ID
Running tests: pytest -v

Technical Decisions: 
I chose SQLite for persistence as it is lightweight, built into Python and does not require a seperate database server. It is suitable as this application won't deal with big amounts of data
The application is divided into three main layers:
CLI (cli.py): Handles user commands and displays output.
Service (service.py): Contains business logic and input validation.
Database (db.py): Handles database operations.
I used Python's built-in argparse library to handle command-line arguments. This avoids adding an external dependency for a simple CLI.