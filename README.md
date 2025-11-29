# EZ LightBurn Driver Switch

![GitHub release](https://img.shields.io/github/release/christdrivengeek/ez-lightburn-driver-switch.svg)
![License](https://img.shields.io/github/license/christdrivengeek/ez-lightburn-driver-switch.svg)
![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)

**Automatic driver switching between EZCAD2 and LightBurn for fiber lasers with one click.** Perfect for ComMarker B4 and other JCZ controllers.

## 🎯 Features

- ✅ **One-Click Driver Switching** - Switch between EZCAD2 and LightBurn drivers instantly
- ✅ **Auto-Uninstall Old Driver** - Prevents Windows from reverting driver changes
- ✅ **Force Install** - Overcomes Windows 10/11 driver stubbornness
- ✅ **Automatic Admin Elevation** - No manual "Run as Administrator" needed
- ✅ **Smart Detection** - Automatically detects which driver is currently active
- ✅ **Setup Wizard** - Easy first-time configuration with auto-detection
- ✅ **Configurable Hardware ID** - Works with different laser boards
- ✅ **Clean Modern UI** - Professional interface with clear status indicators

## 🚀 Quick Start

### For End Users

1. **Download the latest release:** [EZ LightBurn Driver Switch.exe](releases/latest)
2. **Run the executable** (double-click - no right-click needed)
3. **Complete the setup wizard** (first time only)
4. **Switch drivers with one click!**

### For Developers

1. **Clone the repository:**
   ```bash
   git clone https://github.com/christdrivengeek/ez-lightburn-driver-switch.git
   cd ez-lightburn-driver-switch
   ```

2. **Install dependencies:**
   ```bash
   pip install pyinstaller
   ```

3. **Build the executable:**
   ```bash
   pyinstaller --onefile --noconsole --name="EZ LightBurn Driver Switch" --uac-admin --clean EZ_LightBurn_Driver_Switch.py
   ```

4. **Find your executable:** `dist/EZ LightBurn Driver Switch.exe`

## 📋 System Requirements

- **Operating System:** Windows 7 or later
- **Privileges:** Administrator rights required (automatically requested)
- **Hardware:** Galvo Laser with Hardware ID VID_9588&PID_9899 (standard JCZ boards)
- **Software:** EZCAD2 and/or LightBurn installed

## 🎮 Usage Guide

### First-Time Setup

1. **Launch the application** - It will automatically request admin privileges
2. **Complete the Setup Wizard:**
   - Browse to your EZCAD2 driver .inf file
   - Browse to your LightBurn driver .inf file
   - Configure Hardware ID (default: VID_9588&PID_9899)
   - Enable "Force Install" and "Uninstall Old Driver First"
3. **Save Settings**

### Daily Use

1. **Run the application** (double-click)
2. **View Current Status:**
   - 🟢 LightBurn Driver Active
   - 🔵 EZCAD2 Driver Active
   - 🔴 Laser Not Detected
3. **Click the Switch Button:**
   - "Switch to EZCAD2" or "Switch to LightBurn"
4. **Wait for completion** (5-10 seconds)
5. **Reconnect your laser** if needed

## 📁 Driver Locations

### Default Driver Paths
- **EZCAD2:** `C:\EZCAD2\Driver\lmc1usb.inf`
- **LightBurn:** `C:\Program Files\LightBurn\EzCad2Driver\EzCad2Driver.inf` (auto-detected)

### Portable Setup (Recommended)
Create a `Drivers` folder next to the executable:
```
EZ LightBurn Driver Switch\
├── EZ LightBurn Driver Switch.exe
└── Drivers\
    ├── EZCAD\
    │   └── lmc1usb.inf
    └── LightBurn\
        └── EzCad2Driver.inf
```

## 🔧 Troubleshooting

### "Driver installation failed"
- ✅ Ensure you're running as Administrator (UAC prompt is normal)
- ✅ Check laser USB connection
- ✅ Verify driver file paths in Settings
- ✅ Try disconnecting/reconnecting laser

### "Laser Not Detected"
- ✅ Ensure laser is powered ON
- ✅ Check USB cable connection
- ✅ Verify Hardware ID in Settings
- ✅ Try a different USB port

### "Switching but reverting back"
- ✅ Ensure "Uninstall Old Driver First" is enabled in Settings
- ✅ Try manually disabling the device in Device Manager first
- ✅ Restart your computer

### UAC Prompt Issues
- ✅ This is normal and required for driver operations
- ✅ Always click "Yes" when prompted
- ✅ For convenience, set the .exe Properties → Compatibility → "Run as administrator"

## 🏗️ Build Instructions

### Prerequisites
- Python 3.6 or later
- PyInstaller 6.0 or later
- Windows 10/11 (for building)

### Build Commands
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --noconsole --name="EZ LightBurn Driver Switch" --uac-admin --clean EZ_LightBurn_Driver_Switch.py

# Alternative with custom icon
pyinstaller --onefile --noconsole --name="EZ LightBurn Driver Switch" --uac-admin --icon=icon.ico --clean EZ_LightBurn_Driver_Switch.py
```

### Build Output
```
dist/
└── EZ LightBurn Driver Switch.exe  ← Ready for distribution!
```

## 📖 Technical Details

### Driver Detection Logic
The application uses PowerShell to query Windows PnP (Plug and Play) system:
- **LightBurn:** Service contains "winusb" or "usblmc"
- **EZCAD2:** Service contains "lmc" or "bjjcz"
- **Hardware ID:** VID_9588&PID_9899 (standard JCZ boards)

### Switching Process
1. **Uninstall Old Driver** (PowerShell Uninstall-PnpDevice)
2. **Install New Driver** (pnputil /add-driver /install /force)
3. **Scan Hardware Changes** (pnputil /scan-devices)
4. **Detect New Status** (PowerShell Get-PnpDevice)

### Configuration Storage
Settings are saved in `driver_paths.json`:
```json
{
    "ezcad_driver": "C:\\EZCAD2\\Driver\\lmc1usb.inf",
    "lightburn_driver": "C:\\Program Files\\LightBurn\\EzCad2Driver\\EzCad2Driver.inf",
    "hardware_id": "VID_9588&PID_9899",
    "force_install": true,
    "uninstall_first": true
}
```

## 🎯 Supported Hardware

### Compatible Lasers
- ✅ ComMarker B4
- ✅ Cloudray Fiber Lasers
- ✅ Monport Fiber Lasers
- ✅ OMTech Fiber Lasers
- ✅ Any laser with JCZ/BJJCZ controller

### Hardware IDs
- Default: `VID_9588&PID_9899` (Standard JCZ boards)
- Configurable in Settings for different hardware

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push https://x-access-token:$GITHUB_TOKEN@github.com/christdrivengeek/ez-lightburn-driver-switch.git feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/christdrivengeek/ez-lightburn-driver-switch/issues)
- **Discussions:** [GitHub Discussions](https://github.com/christdrivengeek/ez-lightburn-driver-switch/discussions)

## 🙏 Acknowledgments

- Built for the fiber laser community
- Inspired by the struggles of switching between EZCAD2 and LightBurn
- Special thanks to all beta testers

## 📈 Version History

### v2.1 (Latest)
- ✅ Added automatic old driver uninstallation
- ✅ Enhanced error handling and recovery
- ✅ Improved UI feedback during switching
- ✅ Better hardware compatibility

### v2.0
- ✅ Added threading to prevent UI freeze
- ✅ Force install by default for Windows 10/11
- ✅ Configurable Hardware ID
- ✅ Modern UI improvements

### v1.0
- ✅ Initial release
- ✅ Basic driver switching functionality
- ✅ Setup wizard
- ✅ Admin privilege handling

---

**Made with ❤️ by William Sorensen (Christ Driven Geek)**

*For ComMarker B4 and the fiber laser community*