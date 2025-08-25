# DevLog 📓

A lightweight command-line tool for developers to track daily coding activities and progress. Never lose track of what you worked on again.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## ✨ Features

- **🚀 Instant Logging**: Add entries directly from your terminal in seconds
- **⏰ Automatic Timestamps**: Every entry gets precise date and time tracking
- **📝 Markdown Storage**: Logs saved as clean, readable Markdown files
- **📊 Activity Statistics**: Get insights into your coding habits with `devlog stats`
- **✏️ Easy Editing**: Open your log in any editor with `devlog open`
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
# ✓ Logged: Implemented user authentication system
```

View your entire log:
```bash
devlog show
```

Check your coding statistics:
```bash
devlog stats
```

Open log file for manual editing:
```bash
devlog open
```

### Examples

Daily workflow:
```bash
# Morning session
devlog log "Refactored database queries for better performance"

# Afternoon session  
devlog log "Fixed responsive layout issues on mobile devices"

# End of day check
devlog stats
```

Sample output:
```
📊 DevLog Statistics
====================
Total entries: 47
Days with entries: 15

Recent activity:
  2025-08-25: 3 entries
  2025-08-24: 2 entries
  2025-08-23: 4 entries
```

## 📁 Project Structure

```
devlog-cli/
├── src/
│   └── devlog/
│       ├── __init__.py
│       └── cli.py          # Main CLI implementation
├── tests/                  # Unit tests (future)
├── .github/               # GitHub workflows
├── pyproject.toml         # Package configuration
├── README.md              # This file
├── LICENSE               # MIT License
└── .gitignore           # Git ignore rules
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

# Run tests (when implemented)
python -m pytest
```

### File Locations

- Log file: `~/.devlog/devlog.md`
- Source code: `src/devlog/cli.py`
- Package config: `pyproject.toml`

## 🤝 Contributing

We love contributions! Here's how you can help:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Ideas for Contribution

- Add export functionality (JSON, CSV)
- Implement search/filter capabilities
- Add weekly/monthly reports
- Create GUI version
- Add plugin system

## 📝 Changelog

### v0.1.0 (Current)

✅ Basic logging functionality
✅ Statistics tracking
✅ File opening support
✅ Markdown formatting
✅ Cross-platform compatibility

## 🐛 Troubleshooting

### Common issues:

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

**File not found errors:**
```bash
# The log directory is created automatically on first use
devlog log "Test entry"  # This will create the directory
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Python's amazing standard library
- Inspired by developers who value tracking their progress
- Thanks to all contributors and users
