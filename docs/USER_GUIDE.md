# EZ LightBurn Driver Switch - User Guide

## Table of Contents
1. [Installation](#installation)
2. [First-Time Setup](#first-time-setup)
3. [Daily Usage](#daily-usage)
4. [Advanced Configuration](#advanced-configuration)
5. [Troubleshooting](#troubleshooting)
6. [Frequently Asked Questions](#frequently-asked-questions)

## Installation

### System Requirements
- **Operating System:** Windows 7, 8, 10, or 11
- **Privileges:** Administrator rights required (automatically requested)
- **Hardware:** Galvo Laser with Hardware ID VID_9588&PID_9899
- **Software:** EZCAD2 and/or LightBurn installed

### Getting the Software

#### Option 1: Download Release (Recommended)
1. Go to the [GitHub Releases page](https://github.com/christdrivengeek/ez-lightburn-driver-switch/releases)
2. Download the latest `ez-lightburn-driver-switch-v2.1.zip`
3. Extract the ZIP file to a folder of your choice

#### Option 2: Build from Source
1. Clone the repository
2. Run `python build.py` (Windows only)

## First-Time Setup

### Running the Application
1. **Double-click** `EZ LightBurn Driver Switch.exe`
2. **Click "Yes"** when Windows asks for permission (UAC prompt)
3. The **Setup Wizard** will appear automatically

### Setup Wizard Configuration

#### Step 1: EZCAD2 Driver Location
1. Click the **"Browse..."** button
2. Navigate to your EZCAD2 installation folder
3. Look for a folder named `Driver` inside your EZCAD2 directory
4. Select the `.inf` file (usually named `lmc1usb.inf` or similar)
5. Click **"Open"**

**Common EZCAD2 Locations:**
- `C:\EZCAD2\Driver\`
- `C:\Program Files\EZCAD2\Driver\`
- `C:\Program Files (x86)\EZCAD2\Driver\`

#### Step 2: LightBurn Driver Location
1. The application will **auto-detect** the LightBurn driver (you'll see a green checkmark)
2. If not detected, click **"Browse..."**
3. Navigate to: `C:\Program Files\LightBurn\EzCad2Driver\`
4. Select `EzCad2Driver.inf`
5. Click **"Open"**

#### Step 3: Advanced Options

##### Hardware ID
- **Default:** `VID_9588&PID_9899` (Standard JCZ boards)
- **When to change:** If your laser uses a different controller
- **How to find:** Device Manager → Your laser device → Properties → Details → Hardware Ids

##### Force Install
- **Recommended:** Keep this **enabled**
- **Purpose:** Overcomes Windows 10/11 driver stubbornness
- **When to disable:** Only if you experience issues

##### Uninstall Old Driver First
- **Recommended:** Keep this **enabled**
- **Purpose:** Prevents Windows from reverting the driver change
- **When to disable:** Only if uninstalling causes problems

#### Step 4: Save Settings
Click **"Save Settings"** to complete the setup.

## Daily Usage

### Main Interface Overview

```
┌─────────────────────────────────────────┐
│  EZ LightBurn Driver Switch             │
│  Automatic Driver Switching             │
├─────────────────────────────────────────┤
│                                         │
│  [Current Status Display]               │
│  🟢 LightBurn Driver Active             │
│  (WinUSB Protocol - Ready for LightBurn)│
│                                         │
│  [Hardware ID: VID_9588&PID_9899]       │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │   Switch to EZCAD2              │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Auto-uninstall • Force Install         │
│                                         │
│           [⚙ Settings]                  │
│                                         │
└─────────────────────────────────────────┘
```

### Status Indicators

| Status | Color | Meaning | Action |
|--------|-------|---------|--------|
| 🟢 LightBurn Driver Active | Green | LightBurn driver is installed | Switch to EZCAD2 |
| 🔵 EZCAD2 Driver Active | Blue | EZCAD2 driver is installed | Switch to LightBurn |
| 🔴 Laser Not Detected | Red | No laser found | Check connection |
| 🟡 Detection Timeout | Orange | Detection took too long | Retry detection |

### Switching Drivers

#### To Switch from LightBurn to EZCAD2:
1. **Ensure laser is disconnected** (recommended)
2. The status will show "🟢 LightBurn Driver Active"
3. Click **"Switch to EZCAD2"**
4. Wait for the process to complete (5-10 seconds)
5. **Reconnect your laser**
6. Launch EZCAD2

#### To Switch from EZCAD2 to LightBurn:
1. **Ensure laser is disconnected** (recommended)
2. The status will show "🔵 EZCAD2 Driver Active"
3. Click **"Switch to LightBurn"**
4. Wait for the process to complete (5-10 seconds)
5. **Reconnect your laser**
6. Launch LightBurn

### What Happens During Switching

The application performs these steps automatically:
1. **"Uninstalling old driver..."** - Removes the current driver
2. **"Installing [new] driver..."** - Installs the target driver
3. **"Scanning for hardware changes..."** - Updates Windows device manager
4. **Status update** - Shows the new driver status

## Advanced Configuration

### Portable Driver Setup

For maximum portability, create a local `Drivers` folder:

```
EZ LightBurn Driver Switch\
├── EZ LightBurn Driver Switch.exe
└── Drivers\
    ├── EZCAD\
    │   ├── lmc1usb.inf
    │   ├── lmc1usb.sys
    │   └── lmc1usb.cat
    └── LightBurn\
        ├── EzCad2Driver.inf
        ├── WinUSBCoInstaller2.dll
        └── WdfCoInstaller01009.dll
```

**Benefits:**
- Works without EZCAD2/LightBurn installed
- Easy backup and transfer
- Works on multiple computers

### Changing Configuration

1. Click the **"⚙ Settings"** button
2. Modify any setting in the setup wizard
3. Click **"Save Settings"**

### Configuration File

Settings are stored in `driver_paths.json`:
```json
{
    "ezcad_driver": "C:\\EZCAD2\\Driver\\lmc1usb.inf",
    "lightburn_driver": "C:\\Program Files\\LightBurn\\EzCad2Driver\\EzCad2Driver.inf",
    "hardware_id": "VID_9588&PID_9899",
    "force_install": true,
    "uninstall_first": true
}
```

## Troubleshooting

### Common Issues and Solutions

#### "Driver installation failed"

**Symptoms:** Error message after clicking switch button

**Solutions:**
1. ✅ **Check Admin Rights** - Always click "Yes" on UAC prompt
2. ✅ **Verify Driver Paths** - Use Settings to browse to correct .inf files
3. ✅ **Check USB Connection** - Ensure laser is properly connected
4. ✅ **Try Different USB Port** - Some ports have power issues
5. ✅ **Restart Computer** - Sometimes Windows needs a fresh start

#### "Laser Not Detected"

**Symptoms:** Status shows "🔴 Laser Not Detected"

**Solutions:**
1. ✅ **Power On Laser** - Ensure laser has power and is turned on
2. ✅ **Check USB Cable** - Try a different USB cable
3. ✅ **Try Different Port** - Use USB 2.0 port if available
4. ✅ **Check Device Manager** - Look for your laser under USB devices
5. ✅ **Update Hardware ID** - Use Settings to change if different

#### "Switching but reverting back"

**Symptoms:** Switch appears successful but status doesn't change

**Solutions:**
1. ✅ **Enable "Uninstall Old Driver First"** - This is usually the cause
2. ✅ **Use Device Manager** - Manually uninstall old driver first
3. ✅ **Restart Computer** - Sometimes needed for changes to take effect
4. ✅ **Disable/Enable Device** - In Device Manager, disable then enable

#### UAC Prompt Issues

**Symptoms:** No UAC prompt or access denied

**Solutions:**
1. ✅ **This is Normal** - UAC prompt is required and expected
2. ✅ **Always Click "Yes"** - Never deny the UAC prompt
3. ✅ **Set Properties** - Right-click .exe → Properties → Compatibility → "Run as administrator"
4. ✅ **Check Antivirus** - Some antivirus software interferes

#### Application Won't Start

**Symptoms:** Double-clicking does nothing

**Solutions:**
1. ✅ **Run as Administrator** - Right-click → "Run as administrator"
2. ✅ **Check Windows Version** - Requires Windows 7 or later
3. ✅ **Install .NET Framework** - Some Windows systems need it
4. ✅ **Disable Antivirus** - Temporarily disable to test

### Advanced Troubleshooting

#### Device Manager Investigation

1. **Open Device Manager** (`Windows Key + X` → Device Manager)
2. **Find your laser** under:
   - Universal Serial Bus devices
   - Ports (COM & LPT)
   - Other devices
3. **Right-click** → Properties → Driver tab
4. **Check "Driver Details"** to see current .inf file
5. **Check "Driver Date"** to see which is newer

#### PowerShell Commands

For manual checking (run as Administrator in PowerShell):

```powershell
# Find your device
Get-PnpDevice | Where-Object {$_.HardwareID -like "*VID_9588*"}

# Get current driver service
Get-PnpDevice | Where-Object {$_.HardwareID -like "*VID_9588*"} | Select-Object -ExpandProperty Service

# Uninstall driver (replace with your device InstanceId)
Get-PnpDevice -InstanceId "USB\VID_9588&PID_9899\..." | Uninstall-PnpDevice -Confirm:$false

# Install driver manually
pnputil /add-driver "C:\path\to\driver.inf" /install /force
```

## Frequently Asked Questions

### Q: Do I need to run as Administrator every time?
**A:** Yes, driver installation requires administrator privileges. The UAC prompt is normal and required. You can set the .exe Properties → Compatibility → "Run as administrator" to make it automatic.

### Q: Can I use this with any fiber laser?
**A:** It works with JCZ/BJJCZ controllers (most common). If your laser has a different Hardware ID, you can change it in Settings.

### Q: Why does it take 5-10 seconds to switch?
**A:** The application needs to:
- Uninstall the old driver
- Install the new driver
- Scan for hardware changes
- Detect the new status

### Q: What if I don't have EZCAD2 or LightBurn installed?
**A:** You can use the portable setup by copying driver files to a local folder. The application doesn't need the full software installed, just the driver files.

### Q: Can I automate this further?
**A:** The source code is available, so you could modify it for automation, but the current version is designed for manual control with maximum safety.

### Q: Is this safe for my laser?
**A:** Yes, it only changes Windows drivers. It doesn't modify your laser hardware or firmware. The same process is used by Windows Device Manager.

### Q: What if Windows Update interferes?
**A:** Windows Update might occasionally reinstall drivers. Simply run the switcher again to restore your preferred driver.

### Q: Can I use this on multiple computers?
**A:** Yes, as long as each computer has the appropriate driver files installed.

### Q: Do I need to keep the laser disconnected?
**A:** It's recommended but not always necessary. Disconnecting ensures a clean driver installation without interference.

### Q: What's the difference between "Force Install" and regular install?
**A:** Force install overrides Windows' decision about which driver is "better" and ensures your selected driver is installed.

---

## Need More Help?

- **GitHub Issues:** [Report problems](https://github.com/christdrivengeek/ez-lightburn-driver-switch/issues)
- **Documentation:** [README.md](../README.md)
- **Community:** [GitHub Discussions](https://github.com/christdrivengeek/ez-lightburn-driver-switch/discussions)

---

*Made with ❤️ by William Sorensen (Christ Driven Geek)*