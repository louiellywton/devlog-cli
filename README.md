# DevLog 📓

An advanced command-line tool for developers to track daily coding activities and progress with categories, tags, search, and export capabilities. Never lose track of what you worked on again.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Version](https://img.shields.io/badge/version-0.2.0-orange.svg)

## ✨ Features

- **🚀 Instant Logging**: Add entries directly from your terminal in seconds
- **🏷️ Categories & Tags**: Organize work by type and add hashtags for easy categorization
- **🔍 Smart Search**: Find entries quickly with text, category, or tag-based search
- **📊 Rich Statistics**: Get detailed insights into your coding habits and patterns
- **📤 Export Options**: Export logs in JSON, CSV, or Markdown formats
- **⚙️ Configurable**: Customize categories, tags, and settings via config file
- **⏰ Automatic Timestamps**: Every entry gets precise date and time tracking
- **💾 JSON Storage**: Fast, efficient data storage for better performance
- **🌐 Zero Dependencies**: Built entirely with Python standard library
- **💻 Cross-Platform**: Works on macOS, Linux, and Windows

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- Git

### Quick Install
```bash
# Clone the repository
git clone https://github.com/louiellywton/devlog-cli.git
cd devlog-cli

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .
```

## 💡 Usage

### Basic Commands

Add a new log entry:
```bash
devlog log "Implemented user authentication system"
# ✓ Logged: Implemented user authentication system (coding)
```

Add entry with category:
```bash
devlog log "Fixed authentication bug" --category debugging
# ✓ Logged: Fixed authentication bug (debugging)
```

Add entry with tags:
```bash
devlog log "Implemented user dashboard #frontend #react #feature"
# ✓ Logged: Implemented user dashboard (coding) [#frontend #react #feature]
```

View your entire log:
```bash
devlog show
```

Show recent entries:
```bash
devlog show --limit 10
```

Filter by category:
```bash
devlog show --category coding
```

Filter by tags:
```bash
devlog show --tags bug frontend
```

Search through entries:
```bash
devlog search "authentication"
devlog search "bug" --limit 5
```

Check your coding statistics:
```bash
devlog stats
```

Export your logs:
```bash
devlog export csv
devlog export markdown
devlog export json
```

View available categories:
```bash
devlog categories
```

Open log file for manual editing:
```bash
devlog open
```

### Advanced Examples

**Daily workflow with categories:**
```bash
# Morning coding session
devlog log "Refactored database queries for better performance" --category coding

# Afternoon debugging
devlog log "Fixed responsive layout issues on mobile devices" --category debugging

# Team meeting
devlog log "Weekly standup - discussed sprint planning" --category meeting

# End of day check
devlog stats
```

**Using tags for organization:**
```bash
# Frontend work
devlog log "Built React component library #react #frontend #components"

# Backend development
devlog log "Implemented REST API endpoints #python #fastapi #backend"

# Bug fixes
devlog log "Fixed authentication token expiration #bug #security #auth"
```

**Filtering and searching:**
```bash
# Show all frontend work
devlog show --tags frontend

# Search for security-related entries
devlog search "security"

# Show recent debugging work
devlog show --category debugging --limit 5

# Export this week's work
devlog show --limit 20 | devlog export csv
```

### Sample Output

**Statistics:**
```
📊 DevLog Statistics
==================================================
Total entries: 47
Days with entries: 15
Categories used: 6
Unique tags: 12

📈 Recent Activity (Last 7 days):
  2025-01-27: 3 entries
  2025-01-26: 2 entries
  2025-01-25: 4 entries

🏷️  Categories:
  coding: 25 (53.2%)
  debugging: 12 (25.5%)
  planning: 6 (12.8%)
  meeting: 4 (8.5%)

🔖 Top Tags:
  #frontend: 15 times
  #bug: 12 times
  #feature: 8 times
  #react: 7 times
  #python: 6 times
```

**Search Results:**
```
🔍 Search Results for 'bug' (8 found)
============================================================
2025-01-27 14:30 [debugging]: Fixed authentication bug #bug #security
2025-01-26 16:45 [coding]: Resolved memory leak bug #bug #performance
2025-01-25 11:20 [debugging]: Fixed UI rendering bug #bug #frontend
```

## ⚙️ Configuration

DevLog creates a configuration file at `~/.devlog/config.json` on first run. You can customize:

- **Categories**: Organize your work by type
- **Tags**: Enable/disable and set maximum tags per entry
- **Export Formats**: Choose which formats to support
- **Date/Time Formatting**: Customize how dates are displayed

**Example configuration:**
```json
{
  "categories": [
    "coding", "debugging", "planning", "research", 
    "meeting", "documentation", "testing", "deployment"
  ],
  "default_category": "coding",
  "tags_enabled": true,
  "max_tags": 5,
  "export_formats": ["json", "csv", "markdown"]
}
```

## 📁 Project Structure

```
devlog-cli/
├── src/
│   └── devlog/
│       ├── __init__.py
│       └── cli.py          # Main CLI implementation
├── tests/                  # Comprehensive test suite
│   ├── __init__.py
│   └── test_cli.py
├── config_template.json    # Configuration template
├── CHANGELOG.md           # Detailed change history
├── pyproject.toml         # Package configuration
├── README.md              # This file
└── LICENSE                # MIT License
```

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone and setup
git clone https://github.com/louiellywton/devlog-cli.git
cd devlog-cli
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Run tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_cli.py -v
```

### File Locations

- **Log file**: `~/.devlog/devlog.json`
- **Configuration**: `~/.devlog/config.json`
- **Source code**: `src/devlog/cli.py`
- **Package config**: `pyproject.toml`

### Testing

The project includes a comprehensive test suite with:
- **Unit tests** for all functions
- **Mock testing** for file system operations
- **Edge case coverage** for error conditions
- **100% test coverage** of core functionality

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=devlog

# Run specific test
python -m pytest tests/test_cli.py::TestDevLogCLI::test_log_entry_basic
```

## 🚀 What's New in v0.2.0

### Major Features
- **Categories System**: Organize entries by work type
- **Tags Support**: Automatic hashtag extraction and organization
- **Advanced Search**: Find entries quickly with multiple search options
- **Export Functionality**: Multiple export formats for sharing and backup
- **Configuration System**: Customizable settings and preferences

### Performance Improvements
- **JSON Storage**: Faster than Markdown parsing
- **Efficient Search**: Direct data structure access
- **Memory Optimization**: Better handling of large log files
- **Reduced I/O**: Single file operations

### Enhanced CLI
- **New Commands**: `search`, `export`, `categories`
- **Filtering Options**: Category, tag, and search-based filtering
- **Rich Output**: Better formatting and emoji support
- **Help System**: Comprehensive command documentation

## 🤝 Contributing

We love contributions! Here's how you can help:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Ideas for Contribution

- **Data Visualization**: Add charts and graphs to statistics
- **Backup & Sync**: Cloud storage integration
- **Plugin System**: Extensible architecture for custom features
- **Web Dashboard**: Browser-based log viewer
- **Team Features**: Collaborative logging and sharing
- **Time Tracking**: Integration with time management tools

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of all changes.

### Recent Versions

- **v0.2.0** (Current): Categories, tags, search, export, configuration
- **v0.1.0**: Basic logging functionality

## 🐛 Troubleshooting

### Common Issues

**Command not found:**
```bash
# Make sure you installed with -e flag
pip install -e .
```

**Permission errors:**
```bash
# On Linux/macOS, you might need:
chmod +x src/devlog/cli.py
```

**Configuration issues:**
```bash
# Reset to default configuration
rm ~/.devlog/config.json
devlog log "test"  # This will recreate the config
```

**Migration from v0.1.0:**
- Old Markdown logs are automatically preserved
- New JSON format is created on first run
- No data loss during upgrade

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python's amazing standard library
- Inspired by developers who value tracking their progress
- Thanks to all contributors and users
- Special thanks to the open source community

## 🔮 Future Roadmap

### v0.3.0 (Planned)
- Weekly/monthly reports
- Data visualization
- Backup and sync
- Plugin system

### v0.4.0 (Planned)
- Team collaboration
- Time tracking integration
- Project management integration
- API for external tools
