Moli Studio MSU2 USB Screen Assistant MG Version
Original Author: Moli Studio
Modified by: geezmolycos
The modifications by geezmolycos (excluding parts implemented by the original author) can be freely used, referenced, or adapted without attribution (similar to the Unlicense), though I hope contributors will mention my contributions

Changelog

## 2025-10-25
Author: yair

- Improved port scanning functionality with better device detection
- Translated all comments and documentation to English across the codebase
- Added Linux executable script for easier deployment on Linux systems
- Limited Python version requirement to 3.10 for better compatibility
- Added modern package management using `uv` (pyproject.toml and uv.lock)
- Simplified installation process with `uv sync` command
- Fixed font path issues in LCD display utilities
- Refactored and translated ContinuousCapture.py module

## 2025-10-24
Author: yair

- Comprehensive English translation of main application files
- Created comprehensive README.md with installation and usage instructions
- Added requirements.txt for traditional pip-based installation
- Created MSU2_MINI.json configuration file
- Updated .gitignore for better project hygiene
- Translated CHANGELOG.txt to English

## 2024-12-02
Auther: dchg43 <75658553@qq.com>
- Fixed issue where screen touch buttons couldn't turn pages
- Attempted to fix overly aggressive device connection policy that affected Bluetooth and related devices
- Added Libre Hardware Monitor integration with two modes:
  - Mode 1: Similar to previous network speed interface, allows selecting two parameters to display with charts
  - Mode 2: Fully customizable mode using a simple DSL to describe the screen, allowing specification of fonts, images, etc.
- Included usbmmidd virtual screen driver with convenient usage methods
- Added hide to system tray icon
- Fixed screenshot region errors on high-DPI multi-monitor setups

## 2024-11-21

- Optimized screen streaming performance using pipeline architecture
- Optimized screenshot performance using mss library
- Optimized image processing performance for serial port transmission preparation
- Switched to tkinter.ttk interface elements for more modern control styling
- Used grid layout for element arrangement, making interface more beautiful and stable
- Screen streaming can select multiple monitors and specify regions
- Can save interface configuration
- Clock font color is adjustable

## 2024-11-20

- Implemented upload/download traffic monitoring page
- Implemented charting for upload/download page
- Fixed bug where program couldn't exit due to threads not ending
- Moved all GUI operations to main thread to prevent issues

## 2024-11-19

- Learned USB serial port direct image transmission protocol
