#!/usr/bin/env python3
"""
DevLog - A simple command-line tool for logging daily development activities.
"""

import argparse
from datetime import datetime
import os
import sys

# Default path for the log file in the user's home directory
LOG_FILE = os.path.join(os.path.expanduser("~"), ".devlog", "devlog.md")

def ensure_log_file():
    """Create the log directory and file if they don't exist."""
    log_dir = os.path.dirname(LOG_FILE)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.write("# Development Log\n\n")
            f.write("## Summary\n\n")
            f.write("| Date | Entry |\n")
            f.write("|------|-------|\n")

def log_entry(entry_text):
    """Append a new entry with a timestamp to the log file."""
    ensure_log_file()
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Format the entry in a Markdown table row
    formatted_entry = f"| {today} | {entry_text} |\n"
    
    with open(LOG_FILE, 'a') as f:
        f.write(formatted_entry)
    print(f"✓ Logged: {entry_text}")

def show_log():
    """Print the contents of the log file to the terminal."""
    ensure_log_file()
    try:
        with open(LOG_FILE, 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print("Log file is empty. Add an entry with 'devlog \"Your message\"'")

def main():
    """Main function to parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Log your daily development activities.")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Command for adding a new log entry
    log_parser = subparsers.add_parser('log', help='Add a new log entry')
    log_parser.add_argument('entry', type=str, help='The text of your log entry')
    
    # Command for showing the log
    show_parser = subparsers.add_parser('show', help='Show the development log')
    
    args = parser.parse_args()
    
    if args.command == 'log':
        log_entry(args.entry)
    elif args.command == 'show':
        show_log()
    else:
        parser.print_help()
        sys.exit(1)  # Exit with error code if no valid command provided

# This allows the file to be both imported AND run directly
if __name__ == '__main__':
    main()