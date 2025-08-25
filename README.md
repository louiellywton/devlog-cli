# DevLog 📓

A simple, lightweight command-line tool for developers to log their daily activities. Never forget what you worked on again.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## Features

*   **Quick Logging:** Add entries directly from your terminal.
*   **Automatic Timestamps:** Every entry is tagged with the date and time.
*   **Persistent Markdown Log:** Your log is saved to a clean Markdown file in your home directory (`~/.devlog/devlog.md`).
*   **Zero Dependencies:** Built with the Python standard library for maximum compatibility.
*   **Statistics:** View insights about your logging habits with `devlog stats`.
*   **Easy Editing:** Open your log file directly in your default editor with `devlog open`.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/devlog-cli.git
    cd devlog-cli
    ```

2.  **Install in development mode:**
    ```bash
    pip install -e .
    ```

## Usage

It's simple. Just use the `devlog` command.

**Add a new entry:**
```bash
devlog "Finally fixed that pesky bug in the authentication middleware"
# Output: ✓ Logged: Finally fixed that pesky bug...
**View your statistics:**
```bash
devlog stats