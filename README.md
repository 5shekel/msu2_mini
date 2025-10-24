# MSU2 USB Screen Assistant - MG Version

A Python-based control application for the MSU2 series programmable USB screen, featuring real-time monitoring, screen mirroring, and customizable displays.

![MSU2 Display](EDTZ12640.JPG)

## Overview

MSU2 USB Screen Assistant (MG Version) is an enhanced version of the original Moli Studio MSU2 software. This application allows you to control a small USB-connected screen (160x80 pixels) to display various information including:

- System monitoring (CPU, RAM, disk, battery)
- Network speed monitoring  
- Digital clock
- Screen mirroring
- Custom images and GIF animations
- Hardware sensor data (via Libre Hardware Monitor)
- Fully customizable displays using DSL

**Original Author:** Moli Studio  
**Modified by:** geezmolycos  

The modifications by geezmolycos (excluding original implementation) are available under Unlicense-like terms.

## Features

### Display Modes

1. **GIF Animation** - Play pre-loaded 36-frame animations
2. **Digital Clock** - Display current time with customizable colors
3. **Photo Album** - Show static images from flash memory
4. **Screen Mirroring** - Real-time PC screen capture
5. **System Monitor** - CPU/RAM/Disk/Battery usage dashboard
6. **Network Speed** - Upload/download traffic monitoring with charts
7. **Custom Mode 1** - Hardware sensor data with charts (2 parameters)
8. **Custom Mode 2** - Fully customizable display using simple DSL

### Key Features

- **Pipeline architecture** for optimized screen streaming performance
- **Multi-monitor support** with region selection
- **High-DPI multi-monitor** screenshot support
- **Virtual screen driver** (usbmmidd) included
- **System tray** minimize to icon
- **Touch button** page navigation
- **Configuration save/load** capability
- **Libre Hardware Monitor** integration
- **Customizable fonts and colors**

## Hardware Requirements

- **MSU2 Mini USB Screen** (160x80 resolution)
- **Serial connection** via USB (19200 baud rate)
- **Display Types Supported:**
  - GC9107 0.99" 128x115
  - ST7789 2.25" 284x76
  - MSU2 Mini 160x80

## Software Requirements

### Python Version
- Python 3.x (with tcl/tk and IDLE support)

### Required Dependencies

Install all dependencies using pip:

```bash
pip install --upgrade pip
pip install serial
pip install pyserial
pip install psutil
pip install mss
pip install pillow
pip install numpy
pip install pystray
pip install HardwareMonitor
pip install pywin32
pip install opencv-python
pip install pycameralist
```

For Linux users, also install:
```bash
apt-get install python3-tk
pip install pythontk
```

## Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd msu2_mini
   ```

2. **Install Python dependencies**
   
   Using requirements.txt (recommended):
   ```bash
   pip install -r requirements.txt
   ```
   
   Or manually install packages:
   ```bash
   pip install --upgrade pip
   pip install pyserial psutil mss pillow numpy pystray HardwareMonitor pywin32 opencv-python pycameralist
   ```
   
   For Linux, also install:
   ```bash
   apt-get install python3-tk
   ```

3. **Connect your MSU2 USB screen** to your computer via USB

## Running the Application

### Windows

Use one of the provided batch files:

- **`MSU2_MINI_DemoV1.6_dchg.bat`** - Standard console mode
- **`MSU2_MINI_DemoV1.6_dchgw.bat`** - Windowless mode (no console)

Or run directly with Python:
```bash
python MSU2_MINI_DemoV1.6_dchg.py
```

### Linux

```bash
export DISPLAY=:0.0
python3 MSU2_MINI_DemoV1.6_dchg.py
```

### Administrator Rights

**Note:** On Windows, run with administrator privileges for full system monitoring capabilities. Otherwise, some metrics may be unavailable.

## Flashing MCU Firmware

### Required Tools

1. **Download WCH ISP Tool** from: https://www.wch.cn/downloads/WCHISPTool_Setup_exe.html
2. Or use the included `WCHISPTool_Setup.exe` in the `原版/` directory

### Firmware Files

Located in `原版/1.2/` directory:
- `MSU2_MINI_Firmware_V1.2.hex` - Main firmware
- `Flash_V1.1.bin` - Flash data
- `GC9107_0.99_128X115_V1.0.bin` - Display driver (GC9107)
- `ST7789_2.25_284X76_V1.0.bin` - Display driver (ST7789)
- `Page_Config_V1.0.bin` - Page configuration

### Flashing Instructions

1. Install WCH ISP Tool
2. Connect MSU2 device in bootloader mode
3. Open WCH ISP Tool
4. Select the appropriate `.hex` firmware file
5. Click "Download" to flash
6. Refer to `原版/固件更新指南-MSU2系列可编程USB屏幕.pdf` for detailed instructions (Chinese)

## Using the Application

### Basic Operations

1. **Device Connection**
   - Application auto-detects MSU2 devices on serial ports
   - Connection status shown in GUI
   - Heartbeat mechanism maintains connection

2. **Switching Display Modes**
   - Use GUI buttons to switch between modes
   - Use touch buttons on the device for page navigation
   - Configure auto-switching if desired

3. **Image Management**
   - Load JPG/PNG/BMP images via file dialog
   - Images automatically converted to 160x80 resolution
   - RGB565 color format (2 bytes per pixel)
   - Flash images to device memory

4. **Screen Mirroring**
   - Select monitor and region
   - Adjustable update rate
   - Optimized with pipeline architecture

5. **System Tray**
   - Minimize application to system tray
   - Right-click tray icon for options

### Configuration

- Settings automatically saved to configuration file
- Restore previous settings on startup
- Customize colors, fonts, update intervals

## API Reference

### Core Communication Functions

| Function | Parameters | Description |
|----------|-----------|-------------|
| `SER_Write(data)` | data: byte data | Send raw data to serial port |
| `SER_Read()` | - | Read from serial buffer |
| `Read_M_u8(add)` | add: 16-bit address | Read 1-byte register |
| `Write_M_u8(add, data)` | add: address, data: value | Write 1-byte register |

### Flash Operations

| Function | Parameters | Description |
|----------|-----------|-------------|
| `Write_Flash_Page(page, data, num)` | page: page address, data: 256-byte data, num: page count | Write full page |
| `Erase_Flash_page(add, size)` | add: start address, size: page count | Erase region |
| `Write_Flash_hex_fast(add, data)` | add: start address, data: byte data | Fast write arbitrary length |

### Display Control

| Function | Parameters | Description |
|----------|-----------|-------------|
| `LCD_Photo(x,y,w,h,addr)` | x,y: coordinates, w,h: size, addr: Flash address | Display image from Flash |
| `LCD_Color_set(x,y,w,h,color)` | color: RGB565 value | Fill solid color region |
| `LCD_ASCII_32X64(x,y,char,fc,bc)` | char: ASCII character, fc/bc: foreground/background | Display 32x64 character |
| `LCD_GB2312_16X16(x,y,text,fc,bc)` | text: Chinese text | Display 16x16 Chinese characters |

### High-Level Functions

| Function | Description |
|----------|-------------|
| `show_gif()` | Loop play 36-frame animation |
| `show_PC_state()` | System monitoring dashboard |
| `show_PC_Screen()` | Real-time screen mirroring |
| `show_PC_time()` | Digital clock display |

## Project Structure

```
msu2_mini/
├── MSU2_MINI_DemoV1.6_dchg.py      # Main application
├── MSU2_MINI_MG_minimark.py        # MiniMark DSL parser
├── ContinuousCapture.py            # Screen capture module
├── CHANGELOG.txt                   # Version history
├── 接口说明 by Evan.txt            # API documentation (Chinese)
├── python依赖库安装.txt            # Dependency list (Chinese)
├── 指令.txt                        # Command protocol (Chinese)
├── resource/                       # Icons and fonts
│   ├── icon.ico
│   ├── Orbitron-Bold.ttf
│   └── example_background.png
└── 原版/                           # Original version files
    ├── MSU2_DemoV1.0.py           # Original software
    ├── 固件更新指南-MSU2系列可编程USB屏幕.pdf
    └── 1.2/                       # Firmware files
        ├── MSU2_MINI_Firmware_V1.2.hex
        └── ...
```

## Color Encoding

The display uses RGB565 format (2 bytes per pixel):

```python
r = (pixel[0] >> 3) << 11  # Red: 5 bits
g = (pixel[1] >> 2) << 5   # Green: 6 bits  
b = pixel[2] >> 3          # Blue: 5 bits
color = r | g | b
```

## Troubleshooting

### Device Not Detected
- Ensure USB connection is secure
- Check if device appears in Device Manager (Windows) or `lsusb` (Linux)
- Try different USB port
- Verify serial port permissions (Linux: add user to dialout group)

### Performance Issues
- Close unnecessary applications
- Reduce screen mirror update rate
- Use pipeline mode for screen streaming
- Check CPU usage in system monitor

### Display Issues
- Verify correct firmware is flashed
- Check display type configuration
- Ensure images are correct resolution (160x80)
- Verify color format is RGB565

## Development

### Adding Custom Display Modes

1. Create new page ID constant
2. Implement display function (e.g., `show_custom_mode()`)
3. Add GUI controls in main application
4. Register mode in page switcher

### MiniMark DSL

Custom Mode 2 uses a simple DSL for layout:
- Specify text, fonts, colors, positions
- Add images from resources
- Define sensor data bindings
- Configure update intervals

See [`MSU2_MINI_MG_minimark.py`](MSU2_MINI_MG_minimark.py) for parser implementation.

## Changelog

See [CHANGELOG.txt](CHANGELOG.txt) for detailed version history.

### Recent Updates (2024-12-02)
- Fixed touch button page navigation
- Added Libre Hardware Monitor integration
- Included usbmmidd virtual screen driver
- Added system tray icon
- Fixed high-DPI multi-monitor screenshot regions

## License

The modifications by geezmolycos (excluding parts implemented by the original author) can be freely used, referenced, or adapted without attribution (similar to Unlicense), though contributors are encouraged to mention the contributions.

Original code by Moli Studio - refer to original licensing terms.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
- Check existing documentation
- Review API reference
- Consult the Chinese documentation files for detailed technical info
- Create an issue with detailed description and logs

## Acknowledgments

- **Moli Studio** - Original MSU2 software
- **geezmolycos** - MG version enhancements
- **WCH** - MCU and flashing tools
- **LibreHardwareMonitor** - Hardware monitoring integration

---

**Note:** This is a hobbyist/maker project for USB display control. Use at your own risk. Ensure proper permissions and administrator rights when running system monitoring features.