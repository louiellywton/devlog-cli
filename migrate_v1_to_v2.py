#!/usr/bin/env python3
"""
Migration script from DevLog v0.1.0 (Markdown) to v0.2.0 (JSON).
This script will convert your old Markdown logs to the new JSON format.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

def parse_markdown_log(markdown_content):
    """Parse old Markdown format and extract entries."""
    entries = []
    lines = markdown_content.split('\n')
    
    # Skip header lines
    start_processing = False
    for line in lines:
        if '| Date | Entry |' in line:
            start_processing = True
            continue
        
        if start_processing and line.startswith('|') and '|------|' not in line:
            # Parse table row: | 2025-01-27 14:30 | Some entry text |
            parts = line.split('|')
            if len(parts) >= 3:
                date_time = parts[1].strip()
                entry_text = parts[2].strip()
                
                if date_time and entry_text:
                    # Parse date and time
                    try:
                        if ' ' in date_time:
                            date_part, time_part = date_time.split(' ', 1)
                            dt = datetime.strptime(f"{date_part} {time_part}", "%Y-%m-%d %H:%M")
                        else:
                            dt = datetime.strptime(date_time, "%Y-%m-%d")
                            time_part = "00:00"
                        
                        # Extract tags from entry text
                        tags = []
                        if '#' in entry_text:
                            tag_matches = re.findall(r'#(\w+)', entry_text)
                            tags = tag_matches[:5]  # Limit to 5 tags
                            # Clean entry text
                            entry_text = re.sub(r'#\w+', '', entry_text).strip()
                        
                        entry = {
                            "id": len(entries) + 1,
                            "timestamp": dt.isoformat(),
                            "text": entry_text,
                            "category": "coding",  # Default category
                            "tags": tags,
                            "date": dt.strftime("%Y-%m-%d"),
                            "time": dt.strftime("%H:%M")
                        }
                        entries.append(entry)
                    except ValueError as e:
                        print(f"Warning: Could not parse date '{date_time}': {e}")
                        continue
    
    return entries

def migrate_logs():
    """Migrate from old Markdown format to new JSON format."""
    home_dir = os.path.expanduser("~")
    old_log_file = os.path.join(home_dir, ".devlog", "devlog.md")
    new_log_file = os.path.join(home_dir, ".devlog", "devlog.json")
    backup_file = os.path.join(home_dir, ".devlog", "devlog_backup.md")
    
    print("🔄 DevLog Migration Tool v0.1.0 → v0.2.0")
    print("=" * 50)
    
    # Check if old log exists
    if not os.path.exists(old_log_file):
        print("✅ No old Markdown log found. You're already on v0.2.0!")
        return
    
    # Check if new log already exists
    if os.path.exists(new_log_file):
        print("⚠️  New JSON log already exists. Skipping migration.")
        print(f"   Old log: {old_log_file}")
        print(f"   New log: {new_log_file}")
        return
    
    print(f"📖 Found old log: {old_log_file}")
    
    try:
        # Read old log
        with open(old_log_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Parse entries
        entries = parse_markdown_log(markdown_content)
        
        if not entries:
            print("⚠️  No entries found in old log.")
            return
        
        print(f"📝 Found {len(entries)} entries to migrate")
        
        # Create new log structure
        new_log = {
            "entries": entries,
            "metadata": {
                "created": datetime.now().isoformat(),
                "migrated_from": "v0.1.0",
                "migration_date": datetime.now().isoformat(),
                "original_entries": len(entries)
            }
        }
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(new_log_file), exist_ok=True)
        
        # Save new log
        with open(new_log_file, 'w', encoding='utf-8') as f:
            json.dump(new_log, f, indent=2, ensure_ascii=False)
        
        # Create backup
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ Migration completed successfully!")
        print(f"   New log: {new_log_file}")
        print(f"   Backup: {backup_file}")
        print(f"   Entries migrated: {len(entries)}")
        
        # Show sample of migrated entries
        print(f"\n📋 Sample migrated entries:")
        for i, entry in enumerate(entries[:3]):
            tags_display = f" {' '.join(['#' + tag for tag in entry['tags']])}" if entry['tags'] else ""
            print(f"   {entry['date']} {entry['time']}: {entry['text']}{tags_display}")
        
        if len(entries) > 3:
            print(f"   ... and {len(entries) - 3} more entries")
        
        print(f"\n💡 You can now use the new v0.2.0 features:")
        print(f"   - Categories and tags")
        print(f"   - Advanced search and filtering")
        print(f"   - Export to multiple formats")
        print(f"   - Enhanced statistics")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print(f"   Your old log remains unchanged at: {old_log_file}")
        return

def main():
    """Main migration function."""
    try:
        migrate_logs()
    except KeyboardInterrupt:
        print(f"\n⚠️  Migration cancelled by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == '__main__':
    main()
