#!/usr/bin/env python3
"""
DevLog - A simple command-line tool for logging daily development activities.
"""

import argparse
from datetime import datetime
import os
import sys
import subprocess
from pathlib import Path

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
            content = f.read()
            if len(content.strip()) <= len("# Development Log\n\n## Summary\n\n| Date | Entry |\n|------|-------|\n"):
                print("Your log is empty. Add an entry with: devlog log \"Your message\"")
            else:
                print(content)
    except FileNotFoundError:
        print("Log file not found. Add an entry with: devlog log \"Your message\"")

def show_stats():
    """Show statistics about log entries."""
    ensure_log_file()
    try:
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()
        
        # Count actual log entries (skip header lines)
        entries = [line for line in lines if line.startswith('|') and not line.startswith('| Date')]
        total_entries = len(entries)
        
        # Count entries by date
        from collections import defaultdict
        dates = defaultdict(int)
        for entry in entries:
            date_part = entry.split('|')[1].strip().split(' ')[0]  # Extract YYYY-MM-DD
            dates[date_part] += 1
        
        print(f"📊 DevLog Statistics")
        print(f"====================")
        print(f"Total entries: {total_entries}")
        print(f"Days with entries: {len(dates)}")
        print(f"\nRecent activity:")
        for date, count in sorted(dates.items(), reverse=True)[:5]:  # Show last 5 days
            print(f"  {date}: {count} entries")
            
        if total_entries == 0:
            print(f"\n💡 Tip: Start logging with: devlog log \"What I worked on today\"")
            
    except FileNotFoundError:
        print("No log file found. Start by adding your first entry!")

def open_log():
    """Open the log file in the default editor."""
    ensure_log_file()
    try:
        # Try to open with default editor
        if sys.platform == "darwin":  # macOS
            subprocess.run(["open", LOG_FILE])
        elif sys.platform == "win32":  # Windows
            os.startfile(LOG_FILE)
        else:  # Linux and others
            subprocess.run(["xdg-open", LOG_FILE])
        print(f"📝 Opened log file in editor: {LOG_FILE}")
    except Exception as e:
        print(f"❌ Could not open file automatically: {e}")
        print(f"📁 You can find your log at: {LOG_FILE}")

def main():
    """Main function to parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="DevLog - A simple command-line tool for logging daily development activities.",
        epilog="Example: devlog log \"Fixed authentication bug\""
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Command for adding a new log entry
    log_parser = subparsers.add_parser('log', help='Add a new log entry')
    log_parser.add_argument('entry', type=str, help='The text of your log entry')
    
    # Command for showing the log
    show_parser = subparsers.add_parser('show', help='Show the development log')
    
    # Command for statistics
    stats_parser = subparsers.add_parser('stats', help='Show statistics about your entries')
    
    # Command for opening the log file
    open_parser = subparsers.add_parser('open', help='Open the log file in your default editor')
    
    args = parser.parse_args()
    
    if args.command == 'log':
        log_entry(args.entry)
    elif args.command == 'show':
        show_log()
    elif args.command == 'stats':
        show_stats()
    elif args.command == 'open':
        open_log()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()