# xampp_gui_fixed
Fix XAMPP manager-osx white screen, blank window, and broken GUI on macOS Sonoma, Sequoia, and Apple Silicon with this lightweight Python replacement.

# XAMPP Control Panel for macOS

A modern, native Python/Tkinter replacement for the broken `manager-osx` GUI that ships with XAMPP on macOS. If you've been staring at a white/blank XAMPP Manager window, this is for you.

## Problem

XAMPP's official `manager-osx` app is built on an outdated wxWidgets framework and is notoriously broken on modern macOS versions (Sonoma, Sequoia, Apple Silicon). Common symptoms include:
- Blank white window on launch
- Missing or unclickable buttons
- Crash on startup
- No GUI feedback when services fail to start

## Solution

This Python app provides a clean, functional control panel for managing your XAMPP installation.

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
git clone https://github.com/YOUR_USERNAME/xampp-control-panel-macos.git
cd xampp-control-panel-macos

# Run the app
python3 xampp-control.py
```

Or just download `xampp-control.py` and double-click it (may need to right-click > Open the first time due to Gatekeeper).

## Usage

1. Launch the app
2. Click **Start All** to start Apache and MySQL
3. Click **localhost** to open your web root in the browser
4. Click **phpMyAdmin** to manage databases

The app will prompt for your macOS password when starting/stopping services - this is normal and required for XAMPP to bind to ports 80 and 3306.

## Why This Exists

The official XAMPP manager-osx:
- Ships with an Intel-only `osx-x86_64` binary that fails to render on Apple Silicon
- Uses an unmaintained wxWidgets UI framework
- Has a [blank buttons/white screen bug](https://stackoverflow.com/questions/52785071) that has persisted for years across multiple XAMPP versions
- Provides no useful error messages when services fail to start

This replacement uses Python's built-in Tkinter, which is stable, native, and actively maintained.

## Related Projects

- [FlyEnv](https://github.com/xpf0000/flyenv) - A full local dev stack replacement. 
  Much heavier; replaces XAMPP entirely rather than fixing its GUI.
- [lokcalDev](https://github.com/unkownpr/lokcalDev) - Modern Tauri-based dev manager.
  Again, a stack replacement, not a drop-in GUI fix.
- [MAMP](https://www.mamp.info) / [Laravel Herd](https://herd.laravel.com) - 
  Commercial alternatives that require migrating your entire setup.

This project is different: it's a **zero-migration fix**. Keep your existing XAMPP 
installation, htdocs folder, databases, and configs. Just replace the broken GUI.

## License

MIT License

## Disclaimer

This is an unofficial community project. Not affiliated with Apache Friends or the official XAMPP project.

xampp, macos, control-panel, gui, manager-osx, apache, mysql, php, apple-silicon, sequoia, white-screen-fix, tkinter, python3
