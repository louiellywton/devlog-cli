#!/usr/bin/env python3
"""
DevLog - An advanced command-line tool for logging daily development activities.
"""

import argparse
import json
from datetime import datetime, timedelta
import os
import sys
import subprocess
from pathlib import Path
from collections import defaultdict
import re

# Default paths
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".devlog")
LOG_FILE = os.path.join(CONFIG_DIR, "devlog.json")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# Default configuration
DEFAULT_CONFIG = {
    "categories": ["coding", "debugging", "planning", "research", "meeting", "other"],
    "default_category": "coding",
    "tags_enabled": True,
    "max_tags": 5,
    "export_formats": ["json", "csv", "markdown"]
}

def ensure_directory():
    """Create the config directory if it doesn't exist."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

def load_config():
    """Load configuration from file or create default."""
    ensure_directory()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                return config
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    
    # Create default config
    with open(CONFIG_FILE, 'w') as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    return DEFAULT_CONFIG

def load_logs():
    """Load logs from JSON file."""
    ensure_directory()
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
    return {"entries": [], "metadata": {"created": datetime.now().isoformat()}}

def save_logs(logs):
    """Save logs to JSON file."""
    ensure_directory()
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

def log_entry(entry_text, category=None, tags=None):
    """Add a new log entry with enhanced metadata."""
    config = load_config()
    logs = load_logs()
    
    # Parse tags from entry text if not provided
    if tags is None and config["tags_enabled"]:
        # Extract tags from text (words starting with #)
        tag_matches = re.findall(r'#(\w+)', entry_text)
        tags = tag_matches[:config["max_tags"]] if tag_matches else []
        # Remove tags from entry text
        entry_text = re.sub(r'#\w+', '', entry_text).strip()
    
    # Use default category if none specified
    if category is None:
        category = config["default_category"]
    
    entry = {
        "id": len(logs["entries"]) + 1,
        "timestamp": datetime.now().isoformat(),
        "text": entry_text,
        "category": category,
        "tags": tags or [],
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M")
    }
    
    logs["entries"].append(entry)
    save_logs(logs)
    
    # Display confirmation
    tag_display = f" [{' '.join(['#' + tag for tag in tags])}]" if tags else ""
    category_display = f" ({category})" if category else ""
    print(f"✓ Logged: {entry_text}{tag_display}{category_display}")

def show_log(limit=None, category=None, tags=None, search=None):
    """Display logs with filtering options."""
    logs = load_logs()
    entries = logs["entries"]
    
    # Apply filters
    if category:
        entries = [e for e in entries if e.get("category") == category]
    if tags:
        entries = [e for e in entries if any(tag in e.get("tags", []) for tag in tags)]
    if search:
        search_lower = search.lower()
        entries = [e for e in entries if search_lower in e.get("text", "").lower()]
    
    # Apply limit
    if limit:
        entries = entries[-limit:]
    
    if not entries:
        print("No entries found matching your criteria.")
        return
    
    print(f"📓 DevLog Entries ({len(entries)} found)")
    print("=" * 50)
    
    for entry in entries:
        date = entry.get("date", "Unknown")
        time = entry.get("time", "Unknown")
        text = entry.get("text", "")
        category = entry.get("category", "")
        tags = entry.get("tags", [])
        
        tag_display = f" {' '.join(['#' + tag for tag in tags])}" if tags else ""
        category_display = f" [{category}]" if category else ""
        
        print(f"{date} {time}{category_display}: {text}{tag_display}")

def show_stats():
    """Show enhanced statistics with categories and trends."""
    logs = load_logs()
    entries = logs["entries"]
    
    if not entries:
        print("📊 No entries found. Start logging to see statistics!")
        return
    
    # Basic counts
    total_entries = len(entries)
    
    # Category breakdown
    categories = defaultdict(int)
    for entry in entries:
        cat = entry.get("category", "uncategorized")
        categories[cat] += 1
    
    # Tag analysis
    all_tags = []
    for entry in entries:
        all_tags.extend(entry.get("tags", []))
    tag_counts = defaultdict(int)
    for tag in all_tags:
        tag_counts[tag] += 1
    
    # Date analysis
    dates = defaultdict(int)
    for entry in entries:
        date = entry.get("date", "unknown")
        dates[date] += 1
    
    # Recent activity (last 7 days)
    recent_dates = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        recent_dates.append((date, dates.get(date, 0)))
    
    print("📊 DevLog Statistics")
    print("=" * 50)
    print(f"Total entries: {total_entries}")
    print(f"Days with entries: {len(dates)}")
    print(f"Categories used: {len(categories)}")
    print(f"Unique tags: {len(tag_counts)}")
    
    print(f"\n📈 Recent Activity (Last 7 days):")
    for date, count in recent_dates:
        if count > 0:
            print(f"  {date}: {count} entries")
    
    if categories:
        print(f"\n🏷️  Categories:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_entries) * 100
            print(f"  {cat}: {count} ({percentage:.1f}%)")
    
    if tag_counts:
        print(f"\n🔖 Top Tags:")
        top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        for tag, count in top_tags:
            print(f"  #{tag}: {count} times")

def search_logs(query, limit=20):
    """Search through log entries."""
    logs = load_logs()
    entries = logs["entries"]
    
    # Simple text search
    matching_entries = []
    query_lower = query.lower()
    
    for entry in entries:
        text = entry.get("text", "").lower()
        category = entry.get("category", "").lower()
        tags = [tag.lower() for tag in entry.get("tags", [])]
        
        if (query_lower in text or 
            query_lower in category or 
            any(query_lower in tag for tag in tags)):
            matching_entries.append(entry)
    
    if not matching_entries:
        print(f"🔍 No entries found matching '{query}'")
        return
    
    print(f"🔍 Search Results for '{query}' ({len(matching_entries)} found)")
    print("=" * 60)
    
    for entry in matching_entries[:limit]:
        date = entry.get("date", "Unknown")
        time = entry.get("time", "Unknown")
        text = entry.get("text", "")
        category = entry.get("category", "")
        tags = entry.get("tags", [])
        
        tag_display = f" {' '.join(['#' + tag for tag in tags])}" if tags else ""
        category_display = f" [{category}]" if category else ""
        
        print(f"{date} {time}{category_display}: {text}{tag_display}")

def export_logs(format_type="json"):
    """Export logs in various formats."""
    logs = load_logs()
    entries = logs["entries"]
    
    if not entries:
        print("No entries to export.")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format_type == "json":
        filename = f"devlog_export_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(logs, f, indent=2)
        print(f"📤 Exported {len(entries)} entries to {filename}")
    
    elif format_type == "csv":
        filename = f"devlog_export_{timestamp}.csv"
        import csv
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Time", "Category", "Tags", "Entry"])
            for entry in entries:
                writer.writerow([
                    entry.get("date", ""),
                    entry.get("time", ""),
                    entry.get("category", ""),
                    ", ".join(entry.get("tags", [])),
                    entry.get("text", "")
                ])
        print(f"📤 Exported {len(entries)} entries to {filename}")
    
    elif format_type == "markdown":
        filename = f"devlog_export_{timestamp}.md"
        with open(filename, 'w') as f:
            f.write("# DevLog Export\n\n")
            f.write("| Date | Time | Category | Tags | Entry |\n")
            f.write("|------|------|----------|------|-------|\n")
            for entry in entries:
                tags_str = ", ".join(entry.get("tags", []))
                f.write(f"| {entry.get('date', '')} | {entry.get('time', '')} | {entry.get('category', '')} | {tags_str} | {entry.get('text', '')} |\n")
        print(f"📤 Exported {len(entries)} entries to {filename}")
    
    else:
        print(f"❌ Unsupported format: {format_type}")
        print(f"Supported formats: {', '.join(DEFAULT_CONFIG['export_formats'])}")

def open_log():
    """Open the log file in the default editor."""
    ensure_directory()
    try:
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

def show_categories():
    """Show available categories."""
    config = load_config()
    print("🏷️  Available Categories:")
    for i, category in enumerate(config["categories"], 1):
        print(f"  {i}. {category}")

def main():
    """Main function to parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="DevLog - An advanced command-line tool for logging daily development activities.",
        epilog="Examples:\n  devlog log \"Fixed authentication bug\"\n  devlog log \"Team meeting\" --category meeting\n  devlog search \"bug\"\n  devlog export csv"
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Command for adding a new log entry
    log_parser = subparsers.add_parser('log', help='Add a new log entry')
    log_parser.add_argument('entry', type=str, help='The text of your log entry')
    log_parser.add_argument('--category', '-c', choices=load_config()["categories"], 
                           help='Category for the entry')
    log_parser.add_argument('--tags', '-t', nargs='+', help='Tags for the entry')
    
    # Command for showing the log
    show_parser = subparsers.add_parser('show', help='Show the development log')
    show_parser.add_argument('--limit', '-l', type=int, help='Limit number of entries shown')
    show_parser.add_argument('--category', '-c', help='Filter by category')
    show_parser.add_argument('--tags', '-t', nargs='+', help='Filter by tags')
    show_parser.add_argument('--search', '-s', help='Search in entry text')
    
    # Command for statistics
    stats_parser = subparsers.add_parser('stats', help='Show statistics about your entries')
    
    # Command for searching
    search_parser = subparsers.add_parser('search', help='Search through log entries')
    search_parser.add_argument('query', type=str, help='Search query')
    search_parser.add_argument('--limit', '-l', type=int, default=20, help='Limit results')
    
    # Command for export
    export_parser = subparsers.add_parser('export', help='Export logs to various formats')
    export_parser.add_argument('format', choices=['json', 'csv', 'markdown'], 
                              default='json', help='Export format')
    
    # Command for opening the log file
    open_parser = subparsers.add_parser('open', help='Open the log file in your default editor')
    
    # Command for showing categories
    categories_parser = subparsers.add_parser('categories', help='Show available categories')
    
    args = parser.parse_args()
    
    if args.command == 'log':
        log_entry(args.entry, args.category, args.tags)
    elif args.command == 'show':
        show_log(args.limit, args.category, args.tags, args.search)
    elif args.command == 'stats':
        show_stats()
    elif args.command == 'search':
        search_logs(args.query, args.limit)
    elif args.command == 'export':
        export_logs(args.format)
    elif args.command == 'open':
        open_log()
    elif args.command == 'categories':
        show_categories()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()