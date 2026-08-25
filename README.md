# XAMPP Control Panel for macOS

Fix XAMPP manager-osx white screen, blank window, and broken GUI on macOS Sonoma, Sequoia, and Apple Silicon with this lightweight Python replacement.

> **Note:** XAMPP itself is increasingly unmaintained on macOS. If you're starting fresh, consider [Laravel Herd](https://herd.laravel.com) or [Docker](https://www.docker.com) instead. This tool is for people who already have XAMPP installed and just need the GUI working again.

## Problem

XAMPP's official `manager-osx` app is built on an outdated wxWidgets framework and is notoriously broken on modern macOS. Common symptoms include:

- Blank white window on launch
- Missing or unclickable buttons
- Crash on startup
- No GUI feedback when services fail to start

## Solution

A single-file Python/Tkinter control panel that works with your existing XAMPP installation. No migration needed - keep your htdocs, databases, and configs.

## Features

- **Individual Service Control** - Start, Stop, or Restart Apache and MySQL independently
- **Real-time Status Indicators** - Live green/red indicators showing service state
- **Auto-refresh** - Status updates every 3 seconds automatically
- **Quick Actions** - Start All / Stop All / Restart All with one click
- **Browser Shortcuts** - Direct buttons for localhost, phpMyAdmin, and htdocs folder
- **Log Viewer** - Read Apache, MySQL, and PHP logs without leaving the app
- **Config Access** - One-click open of httpd.conf, php.ini, my.cnf in your default text editor
- **Native macOS Password Dialog** - Uses AppleScript `with administrator privileges` for secure sudo access

## Requirements

- macOS (tested on Sonoma, Sequoia, Apple Silicon & Intel)
- XAMPP installed at `/Applications/XAMPP` (default location)
- Python 3 (comes pre-installed on macOS)

## Installation

```bash
# Clone the repository
git clone https://github.com/kartikpathak100/xampp_gui_fixed.git
cd xampp_gui_fixed

# Run the app
python3 xampp-control.py
```

Or just download `xampp-control.py` and double-click it (may need to right-click &gt; Open the first time due to Gatekeeper).

## Why This Exists

The official XAMPP manager-osx:

- Ships with an Intel-only `osx-x86_64` binary that fails to render on Apple Silicon
- Uses an unmaintained wxWidgets UI framework
- Has a [blank buttons/white screen bug](https://stackoverflow.com/questions/52785071) that has persisted for years
- Provides no useful error messages when services fail to start

This replacement uses Python's built-in Tkinter, which is stable, native, and actively maintained.

## Related Projects

- [FlyEnv](https://github.com/xpf0000/flyenv) - Full local dev stack replacement (heavier, replaces XAMPP entirely)
- [Laravel Herd](https://herd.laravel.com) - Modern native macOS dev environment (recommended for new projects)
- [MAMP](https://www.mamp.info) - Classic GUI-based alternative to XAMPP

## License

MIT License
